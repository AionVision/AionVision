"""
Pipelines: Multi-step agent workflows with typed data flow.

Demonstrates:
- Building pipelines with fluent API
- Chaining search, analysis, and synthesis steps
- Using seed data (image IDs, document IDs)
- DAG patterns with depends_on
- Cross-referencing documents and images
"""

import asyncio

from aion import AionVision


async def basic_pipeline():
    """Chain search and analysis in a pipeline."""

    async with AionVision.from_env() as client:

        # Search images, then organize results
        result = await (
            client.pipeline()
            .search_images("damaged utility poles")
            .organize("Sort by damage severity")
            .run()
        )
        print(f"Pipeline completed in {result.execution_time_ms}ms")
        print(f"Final result: {result.final.summary}")


async def multi_step_pipeline():
    """Multi-step pipeline with analysis and synthesis."""

    async with AionVision.from_env() as client:

        result = await (
            client.pipeline()
            .search_images("infrastructure damage")
            .analyze("Categorize damage types and severity")
            .synthesize("Write an executive summary of findings")
            .run()
        )

        # Access per-step results
        for i, step_result in enumerate(result.steps):
            print(f"Step {i}: {step_result.agent}")
            print(f"  Status: {step_result.status}")


async def document_pipeline():
    """Pipeline with document search and analysis."""

    async with AionVision.from_env() as client:

        result = await (
            client.pipeline()
            .search_documents("safety inspection reports")
            .analyze_documents("Summarize key findings")
            .synthesize("Create a compliance report")
            .run()
        )
        print(result.final.summary)


async def seed_data_pipeline():
    """Pipeline with pre-selected files."""

    async with AionVision.from_env() as client:

        # Start with known image IDs (skip search step)
        result = await (
            client.pipeline()
            .with_images(["img-1", "img-2", "img-3"])
            .analyze("Compare damage patterns")
            .synthesize("Write a comparison report")
            .run()
        )
        print(result.final.summary)

        # Start with known document IDs
        result = await (
            client.pipeline()
            .with_documents(["doc-1", "doc-2"])
            .analyze_documents("Extract key metrics")
            .run()
        )


async def dag_pipeline():
    """Pipeline with parallel steps using depends_on."""

    async with AionVision.from_env() as client:

        # Steps 0 and 1 run in parallel, step 2 depends on both
        result = await (
            client.pipeline()
            .search_images("utility poles")          # step 0
            .search_documents("maintenance records")  # step 1
            .cross_reference(                         # step 2
                "Cross-reference images with maintenance records",
                depends_on=[0, 1],
            )
            .run()
        )
        print(result.final.summary)


if __name__ == "__main__":
    asyncio.run(basic_pipeline())
