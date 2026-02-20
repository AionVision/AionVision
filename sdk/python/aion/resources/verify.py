from __future__ import annotations
import base64
import mimetypes
import warnings
from pathlib import Path
from typing import Any, Callable, Optional, Union
import aiofiles
from ..config import ClientConfig, InsecureTransportWarning
from ..exceptions import ValidationError
from ..types.batch import BatchImageInput, BatchItemStatus, BatchResults, BatchStatus, BatchStatusResult, BatchSubmissionResult, BatchVerifyInput
from ..types.verify import VerificationIssue, VerificationResult


class VerifyResource:
    """

        Verification operations for the Aionvision SDK.

        .. deprecated::
            This class is deprecated. Verification functionality is being removed
            as a standalone operation. Use :meth:`AionVision.upload` for image processing.
            This class will be removed in a future version.

        Verify content accuracy and detect hallucinations.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the verify resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def verify(self, image: Optional[Union[str, Path, bytes]] = None, content: str = '', *, images: Optional[list[Union[str, Path, bytes]]] = None, contents: Optional[list[str]] = None, object_key: Optional[str] = None, object_keys: Optional[list[str]] = None, mode: str = 'response', verification_level: str = 'standard', use_consensus: bool = True, providers: Optional[list[str]] = None, rule_set_id: Optional[str] = None, rules: Optional[list[dict[str, Any]]] = None, max_parallel: int = 5, timeout_per_item: int = 30, on_progress: Optional[Callable[[BatchStatusResult], None]] = None) -> Union[VerificationResult, list[VerificationResult]]:
        """

                Verify if content accurately describes one or more images.

                For single images, uses synchronous API. For multiple images,
                uses batch API with automatic polling.

                Single mode:
                    verify(image="img.jpg", content="A red car")

                Batch mode:
                    verify(images=["img1.jpg", "img2.jpg"], contents=["A red car", "A blue truck"])

                Args:
                    image: Single image (URL, file path, or bytes)
                    content: Text content to verify against single image
                    images: List of images for batch verification
                    contents: List of contents to verify (must match images length)
                    object_key: S3/Spaces object key for single previously uploaded image
                    object_keys: List of S3/Spaces object keys for batch verification
                    mode: "response" (full VLM response) or "claim" (specific claim)
                    verification_level: quick | standard | thorough | critical
                    use_consensus: Use multi-provider consensus
                    providers: Specific VLM providers to use for verification
                    rule_set_id: UUID of rule set to apply during verification
                    rules: Inline rules to apply during verification
                    max_parallel: Maximum concurrent processing for batch (1-20, default: 5)
                    timeout_per_item: Seconds per item for batch (5-300, default: 30)
                    on_progress: Optional callback for batch progress updates

                Returns:
                    VerificationResult for single image
                    List[VerificationResult] for multiple images

                Raises:
                    ValidationError: If image format is invalid or input is ambiguous

                Example:
                    ```python
                    # Single verification
                    result = await client.verify("photo.jpg", "A red sports car")
                    print(f"Verified: {result.is_verified}")

                    # Batch verification
                    results = await client.verify(
                        images=["img1.jpg", "img2.jpg"],
                        contents=["A red car", "A blue truck"]
                    )
                    for r in results:
                        print(f"Verified: {r.is_verified}, Risk: {r.risk_level}")
                    ```
        """
        ...
