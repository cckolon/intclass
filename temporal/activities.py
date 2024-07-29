import logging
import multiprocessing

import sympy as sp
from temporalio import activity

from data_generation.generate_functions import get_function_string
from data_generation.make_training_data import write_training_data_batch
from settings import (
    GENERATION_TIMEOUT,
    INTEGRATION_TIMEOUT,
    INTEGRATION_VARIABLE_NAME,
)


class IncompleteIntegralException(Exception):
    pass


def generate_function(
    num_internal_nodes: int, return_queue: multiprocessing.Queue
):
    return_queue.put(get_function_string(num_internal_nodes))


@activity.defn
def generate_function_with_timeout(num_internal_nodes: int) -> str:
    return_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=generate_function, args=(num_internal_nodes, return_queue)
    )
    process.start()
    process.join(timeout=GENERATION_TIMEOUT)
    if process.is_alive():
        logging.warning(
            "Function generation timed out for %s", num_internal_nodes
        )
        process.terminate()
        logging.warning("Terminated process for %s", num_internal_nodes)
        process.join()
        return None
    return return_queue.get()


def integrate_function(f: str, return_queue: multiprocessing.Queue) -> tuple:
    # integrand, integral, success
    try:
        integral = sp.integrate(f, sp.symbols(INTEGRATION_VARIABLE_NAME))
        if integral.has(sp.Integral):

            raise IncompleteIntegralException(f"Could not fully integrate {f}")
        return_queue.put((f, str(integral), True))
    except Exception as e:  # pylint: disable=broad-except
        return_queue.put((f, None, False))
        logging.error("Integration failed: %s", e)


@activity.defn
def integrate_function_with_timeout(f: str) -> tuple:
    return_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=integrate_function, args=(f, return_queue)
    )
    process.start()
    process.join(timeout=INTEGRATION_TIMEOUT)
    if process.is_alive():
        logging.warning("Integration timed out for %s", f)
        process.terminate()
        logging.warning("Terminated process for %s", f)
        process.join()
        return (f, None, False)
    return return_queue.get()


@activity.defn
def write_training_data(results: list[tuple]):
    write_training_data_batch(results)
    return len(results)
