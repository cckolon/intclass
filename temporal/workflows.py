import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from settings import (
    DATA_GENERATION_BATCH_SIZE,
    FUNCTION_COMPLEXITY,
    INTEGRATION_TIMEOUT,
)

with workflow.unsafe.imports_passed_through():
    from .activities import (
        generate_function_with_timeout,
        integrate_function_with_timeout,
        write_training_data,
    )


@workflow.defn
class GenerateAndIntegrateFunctionsWF:
    @workflow.run
    async def run(self):
        functions = await asyncio.gather(
            *(
                workflow.execute_activity(
                    generate_function_with_timeout,
                    FUNCTION_COMPLEXITY,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                for _ in range(DATA_GENERATION_BATCH_SIZE)
            )
        )
        results = await asyncio.gather(
            *(self.integrate_or_timeout(f) for f in functions if f is not None)
        )
        workflow.logger.debug(f"Results: {results}")
        await workflow.execute_activity(
            write_training_data,
            results,
            start_to_close_timeout=timedelta(seconds=10),
        )
        workflow.continue_as_new()

    async def integrate_or_timeout(self, integrand: str) -> tuple:
        once_only = RetryPolicy(maximum_attempts=1)
        return await workflow.execute_activity(
            integrate_function_with_timeout,
            integrand,
            start_to_close_timeout=timedelta(seconds=INTEGRATION_TIMEOUT + 1),
            retry_policy=once_only,
        )
