from __future__ import annotations
import base64
import mimetypes
import warnings
from pathlib import Path
from typing import Any, Callable, Optional, Union
import aiofiles
from ..config import ClientConfig, InsecureTransportWarning
from ..exceptions import ValidationError
from ..types.batch import BatchImageInput, BatchItemStatus, BatchResults, BatchStatus, BatchStatusResult, BatchSubmissionResult
from ..types.describe import DescriptionResult


class DescribeResource:
    """

        Description operations for the Aionvision SDK.

        .. deprecated::
            This class is deprecated. Use :meth:`AionVision.upload` instead,
            which handles file upload and description in a single operation.
            The standalone describe functionality will be removed in a future version.

        Generate AI descriptions for images from URLs, file paths, or bytes.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the describe resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def describe(self, image: Optional[Union[str, Path, bytes, list[Union[str, Path, bytes]]]] = None, *, object_key: Optional[str] = None, object_keys: Optional[list[str]] = None, verification_level: str = 'standard', include_metadata: bool = True, include_tags: bool = True, providers: Optional[list[str]] = None, prompt: Optional[str] = None, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None, max_parallel: int = 5, timeout_per_item: int = 30, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> Union[DescriptionResult, list[DescriptionResult]]:
        """

                Generate AI description for one or more images.

                For single images, uses synchronous API. For multiple images,
                uses batch API with automatic polling.

                Args:
                    image: Single image (URL, file path, or bytes) or list of images
                    object_key: S3/Spaces object key for single previously uploaded image
                    object_keys: List of S3/Spaces object keys for batch processing
                    verification_level: quick | standard | thorough | critical
                    include_metadata: Include image metadata in response
                    include_tags: Whether to generate tags along with the description
                    providers: Specific VLM providers to use
                    prompt: Custom prompt for description focus
                    rule_set_id: UUID of rule set to apply during description
                    rules: Inline rules to apply during description
                    max_parallel: Maximum concurrent processing for batch (1-20, default: 5)
                    timeout_per_item: Seconds per item for batch (5-300, default: 30)
                    on_progress: Optional callback for batch progress updates

                Returns:
                    DescriptionResult for single image
                    List[DescriptionResult] for multiple images

                Raises:
                    ValidationError: If image format is invalid or input is ambiguous

                Example:
                    ```python
                    # Single image
                    result = await client.describe("photo.jpg")
                    print(result.description)

                    # Multiple images (batch)
                    results = await client.describe(["img1.jpg", "img2.jpg"])
                    for r in results:
                        print(r.description)

                    # Batch by object keys
                    results = await client.describe(object_keys=["key1", "key2"])
                    ```
        """
        ...
