import asyncio
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from temporalio.client import Client
from temporalio.worker import SharedStateManager, Worker

from settings import (
    LOG_LEVEL,
    MAX_WORKERS,
    TEMPORAL_PORT,
    TEMPORAL_SERVER,
)
from temporal.activities import (
    generate_function_with_timeout,
    integrate_function_with_timeout,
    write_training_data,
)
from temporal.workflows import GenerateAndIntegrateFunctionsWF


async def main():
    client = await Client.connect(f"{TEMPORAL_SERVER}:{TEMPORAL_PORT}")

    worker = Worker(
        client=client,
        task_queue="default",
        workflows=[GenerateAndIntegrateFunctionsWF],
        activities=[
            generate_function_with_timeout,
            integrate_function_with_timeout,
            write_training_data,
        ],
        activity_executor=ProcessPoolExecutor(max_workers=MAX_WORKERS),
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
        max_concurrent_activities=MAX_WORKERS,
    )
    await worker.run()


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.run(main())
