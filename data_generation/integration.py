import logging
from concurrent.futures import ProcessPoolExecutor
from time import time

import sympy as sp
from wrapt_timeout_decorator import timeout

from settings import INTEGRATION_TIMEOUT, INTEGRATION_VARIABLE_NAME

logger = logging.getLogger(__name__)


class IncompleteIntegralException(Exception):
    pass


@timeout(INTEGRATION_TIMEOUT, use_signals=False)
def integrate_with_timeout(f: str) -> str:
    integral = sp.integrate(f, sp.symbols(INTEGRATION_VARIABLE_NAME))
    if integral.has(sp.Integral):
        raise IncompleteIntegralException(
            f"Could not fully integrate {f}"
        )
    return str(integral)


def integrate_function_with_timeout(f: str, timeout: int) -> tuple:
    # integrand, integral, success
    start_time = time()
    try:
        integral = integrate_with_timeout(f)
        logger.debug(
            f"Integrated {f} in {time()-start_time:.2f} seconds."
        )
        return (f, integral, True)
    except Exception as e:
        logger.debug(
            f"Failed to integrate {f} in "
            f"{time()-start_time:.2f} seconds: {e}"
        )
        return (f, None, False)


def integrate_functions_with_timeout(
    functions: list, timeout: int
) -> list:
    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(
                integrate_function_with_timeout,
                functions,
                [timeout for _ in functions],
            )
        )
        return results
