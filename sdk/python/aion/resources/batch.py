from __future__ import annotations
import warnings
from collections.abc import AsyncIterator
from typing import Any, Callable, Optional
from ..config import ClientConfig
from ..types.batch import BatchImageInput, BatchItemResult, BatchResults, BatchStatus, BatchStatusResult, BatchSubmissionResult, BatchVerifyInput


class BatchResource:
    """

        Batch operation management for the Aionvision SDK.

        Provides methods to check batch status, retrieve results,
        cancel operations, and wait for completion.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the batch resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def get_status(self, batch_id: str) -> BatchStatusResult:
        """

                Get the current status of a batch operation.

                Args:
                    batch_id: Unique batch identifier (UUID)

                Returns:
                    BatchStatusResult with current progress and status

                Example:
                    ```python
                    status = await client.batch.get_status(batch_id="abc123...")
                    print(f"Status: {status.status}")
                    print(f"Progress: {status.progress_percentage}%")
                    print(f"Processed: {status.processed_items}/{status.total_items}")
                    ```
        """
        ...

    async def get_results(self, batch_id: str, *, include_failed: bool = True, offset: int = 0, limit: int = 100) -> BatchResults:
        """

                Get results of a batch operation.

                Retrieves the processed results with pagination support.

                Args:
                    batch_id: Unique batch identifier (UUID)
                    include_failed: Whether to include failed items (default: True)
                    offset: Pagination offset (default: 0)
                    limit: Results per page (default: 100)

                Returns:
                    BatchResults with items, pagination, and summary

                Example:
                    ```python
                    results = await client.batch.get_results(batch_id="abc123...")

                    for item in results.results:
                        if item.status == BatchItemStatus.SUCCESS:
                            print(f"Item {item.item_index}: {item.description}")
                        else:
                            print(f"Item {item.item_index} failed: {item.error_message}")

                    # Use helper methods
                    successful = results.successful_results()
                    failed = results.failed_results()
                    ```
        """
        ...

    async def get_all_results(self, batch_id: str, *, include_failed: bool = True, page_size: int = 100) -> AsyncIterator[BatchItemResult]:
        """

                Iterate through all batch results with automatic pagination.

                This is a convenience method that handles pagination automatically.
                For manual pagination control, use get_results() instead.

                Args:
                    batch_id: Unique batch identifier (UUID)
                    include_failed: Whether to include failed items (default: True)
                    page_size: Results per page (default: 100)

                Yields:
                    BatchItemResult objects one at a time

                Example:
                    ```python
                    async for item in client.batch.get_all_results(batch_id):
                        if item.status == BatchItemStatus.SUCCESS:
                            print(f"Item {item.item_index}: {item.description}")
                        else:
                            print(f"Item {item.item_index} failed: {item.error_message}")
                    ```
        """
        ...

    async def cancel(self, batch_id: str) -> None:
        """

                Cancel a pending or processing batch operation.

                Only batches in PENDING or PROCESSING status can be cancelled.
                Already completed, failed, or cancelled batches cannot be cancelled.

                Args:
                    batch_id: Unique batch identifier (UUID)

                Raises:
                    ValidationError: If batch cannot be cancelled (wrong status)

                Example:
                    ```python
                    await client.batch.cancel(batch_id="abc123...")
                    print("Batch cancelled successfully")
                    ```
        """
        ...

    async def wait_for_completion(self, batch_id: str, *, timeout: Optional[float] = None, poll_interval: Optional[float] = None, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> BatchStatusResult:
        """

                Poll until batch reaches a terminal state.

                Waits for the batch to complete, fail, or be cancelled.

                Args:
                    batch_id: Unique batch identifier (UUID)
                    timeout: Maximum time to wait in seconds (default: from config)
                    poll_interval: Interval between status checks (default: from config)
                    on_progress: Optional callback called with each status update

                Returns:
                    Final BatchStatusResult when batch completes

                Raises:
                    TimeoutError: If timeout is exceeded before completion
                    BatchError: If batch fails

                Example:
                    ```python
                    # Simple wait
                    final = await client.batch.wait_for_completion(batch_id="abc123...")
                    print(f"Completed with status: {final.status}")

                    # With progress callback
                    def show_progress(status):
                        print(f"Progress: {status.progress_percentage}%")

                    final = await client.batch.wait_for_completion(
                        batch_id="abc123...",
                        timeout=300,
                        on_progress=show_progress
                    )
                    ```
        """
        ...

    async def submit_describe(self, images: list[BatchImageInput], *, verification_level: str = 'standard', providers: Optional[list[str]] = None, prompt: Optional[str] = None, max_parallel: int = 5, timeout_per_item: int = 30, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None) -> BatchSubmissionResult:
        """

                Submit a batch of images for description processing.

                .. deprecated::
                    This method is deprecated. Use :meth:`AionVision.upload` instead,
                    which handles file upload and description in a single operation.
                    The standalone batch describe functionality will be removed in a future version.

                This submits an asynchronous batch job. Use get_status() or
                wait_for_completion() to monitor progress, then get_results()
                to retrieve the descriptions.

                Args:
                    images: List of BatchImageInput (image_url, image_base64, or object_key)
                    verification_level: quick | standard | thorough | critical
                    providers: Specific VLM providers to use
                    prompt: Custom prompt for description focus
                    max_parallel: Maximum concurrent processing (1-20, default: 5)
                    timeout_per_item: Seconds per item (5-300, default: 30)
                    rule_set_id: UUID of rule set to apply
                    rules: Inline rules to apply

                Returns:
                    BatchSubmissionResult with batch_id for tracking

                Example:
                    ```python
                    # Submit batch
                    submission = await client.batch.submit_describe([
                        BatchImageInput(image_url="https://example.com/img1.jpg"),
                        BatchImageInput(image_url="https://example.com/img2.jpg"),
                    ])

                    # Wait for completion
                    final = await client.batch.wait_for_completion(submission.batch_id)

                    # Get results
                    results = await client.batch.get_results(submission.batch_id)
                    for item in results.results:
                        print(f"{item.item_index}: {item.description}")
                    ```
        """
        ...

    async def submit_verify(self, pairs: list[BatchVerifyInput], *, verification_level: str = 'standard', providers: Optional[list[str]] = None, max_parallel: int = 5, timeout_per_item: int = 30, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None) -> BatchSubmissionResult:
        """

                Submit a batch of image-text pairs for verification.

                .. deprecated::
                    This method is deprecated. Verification functionality is being removed
                    as a standalone operation. Use :meth:`AionVision.upload` for image processing.
                    This method will be removed in a future version.

                This submits an asynchronous batch job. Use get_status() or
                wait_for_completion() to monitor progress, then get_results()
                to retrieve the verification results.

                Args:
                    pairs: List of BatchVerifyInput (image + content to verify)
                    verification_level: quick | standard | thorough | critical
                    providers: Specific VLM providers to use
                    max_parallel: Maximum concurrent processing (1-20, default: 5)
                    timeout_per_item: Seconds per item (5-300, default: 30)
                    rule_set_id: UUID of rule set to apply
                    rules: Inline rules to apply

                Returns:
                    BatchSubmissionResult with batch_id for tracking

                Example:
                    ```python
                    # Submit batch
                    submission = await client.batch.submit_verify([
                        BatchVerifyInput(
                            image=BatchImageInput(image_url="https://example.com/img1.jpg"),
                            content="A red sports car"
                        ),
                        BatchVerifyInput(
                            image=BatchImageInput(image_url="https://example.com/img2.jpg"),
                            content="A blue truck"
                        ),
                    ])

                    # Wait for completion
                    final = await client.batch.wait_for_completion(submission.batch_id)

                    # Get results
                    results = await client.batch.get_results(submission.batch_id)
                    for item in results.results:
                        print(f"{item.item_index}: verified={item.is_verified}")
                    ```
        """
        ...
