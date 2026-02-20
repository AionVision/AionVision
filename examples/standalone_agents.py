"""
Standalone Agents: Synthesize, analyze, and organize without chat.

Demonstrates:
- Synthesis agent for generating reports
- Document analysis agent
- Folder organization agent
- Direct programmatic access to agent operations
"""

import asyncio

from aion import AionVision


async def synthesize_report():
    """Generate a synthesis report from documents."""

    async with AionVision.from_env() as client:

        # Synthesize a report from specific documents
        result = await client.agent_operations.synthesize(
            "Write a summary report on spending patterns",
            document_ids=["doc-1", "doc-2", "doc-3"],
        )
        print(f"Report:\n{result.report}")


async def analyze_documents():
    """Run document analysis agent."""

    async with AionVision.from_env() as client:

        result = await client.agent_operations.analyze_documents(
            "Identify key safety issues mentioned in these reports",
            document_ids=["doc-1", "doc-2"],
        )
        print(f"Analysis:\n{result.analysis}")


async def organize_files():
    """Organize files into folders using AI."""

    async with AionVision.from_env() as client:

        result = await client.agent_operations.organize(
            "Sort these images by damage severity",
            image_ids=["img-1", "img-2", "img-3"],
        )
        print(f"Summary: {result.summary}")
        for action in result.actions:
            print(f"  [{action.action}] {action.folder_name} ({action.file_count} files)")


if __name__ == "__main__":
    asyncio.run(synthesize_report())
