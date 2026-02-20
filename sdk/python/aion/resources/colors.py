from __future__ import annotations
import re
from collections.abc import AsyncIterator
from typing import Any, Optional
from ..config import ClientConfig
from ..exceptions import ValidationError
from ..types.colors import BatchColorExtractionResult, ColorExtractionResult, ColorFamilyInfo, ColorSearchResponse, ColorSearchResult


class ColorsResource:
    """

        Color analysis and search operations for the Aionvision SDK.

        Colors are extracted automatically when images are uploaded.
        Use these methods to retrieve color data, search by color, or
        re-run extraction with custom settings. Useful for interior
        design, material matching, and visual organization applications.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the colors resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def extract(self, image_id: str, *, force: bool = False, n_colors: int = 16) -> ColorExtractionResult:
        """

                Re-run color extraction with custom settings.

                Colors are extracted automatically on upload (16 colors by default).
                Use this method only to re-extract with a different number of colors
                or to force a refresh. Returns existing results unless force=True.

                Args:
                    image_id: Unique image identifier (UUID)
                    force: Force re-extraction even if colors exist (default: False)
                    n_colors: Number of dominant colors to extract (3-16, default: 16)

                Returns:
                    ColorExtractionResult with status and analysis (if completed)

                Raises:
                    ValidationError: If n_colors is not between 3 and 16
                    ResourceNotFoundError: If image not found

                Example:
                    ```python
                    # Re-extract with fewer colors
                    result = await client.colors.extract(image_id, n_colors=6)

                    # Force re-extraction (refresh cached results)
                    result = await client.colors.extract(
                        image_id,
                        force=True,
                        n_colors=8,
                    )
                    ```
        """
        ...

    async def get(self, image_id: str) -> ColorExtractionResult:
        """

                Get extracted colors for an image.

                Colors are extracted automatically on upload. Use this to retrieve
                the results. Returns the color analysis if extraction is completed,
                or the current status if still processing.

                Args:
                    image_id: Unique image identifier (UUID)

                Returns:
                    ColorExtractionResult with status and analysis (if available)

                Raises:
                    ResourceNotFoundError: If image not found

                Example:
                    ```python
                    result = await client.colors.get(image_id)

                    if result.is_completed:
                        analysis = result.color_analysis

                        # Get dominant color
                        dominant = analysis.dominant_colors[0]
                        print(f"Main color: {dominant.name} ({dominant.family})")

                        # Check temperature
                        temp = analysis.analytics.temperature
                        print(f"Temperature: {temp.value} (score: {temp.score:.2f})")
                    elif result.is_pending:
                        # Still processing — colors are extracted automatically on upload
                        print("Color extraction is still in progress...")
                    ```
        """
        ...

    async def search(self, *, hex_code: Optional[str] = None, color_name: Optional[str] = None, color_family: Optional[str] = None, delta_e_threshold: float = 15.0, min_percentage: float = 5.0, limit: int = 50, offset: int = 0) -> ColorSearchResponse:
        """

                Search images by color properties.

                Search by exact hex code with perceptual tolerance (Delta-E),
                semantic color name, or color family. At least one search
                criterion must be provided.

                Args:
                    hex_code: Hex color code to search for (e.g., "#C4A87C")
                    color_name: Semantic color name (e.g., "walnut", "brass")
                    color_family: Color family (e.g., "wood", "metallic", "earth_tone")
                    delta_e_threshold: Color tolerance using Delta-E (0-100, default: 15)
                        Lower values = more exact match, higher = more tolerant
                    min_percentage: Minimum percentage the color must cover (0-100, default: 5)
                    limit: Maximum results to return (1-200, default: 50)
                    offset: Pagination offset (default: 0)

                Returns:
                    ColorSearchResponse with matching images and pagination info

                Raises:
                    ValidationError: If no search criteria provided or params out of range

                Example:
                    ```python
                    # Search by hex code with tolerance
                    results = await client.colors.search(
                        hex_code="#8B4513",  # Saddle brown
                        delta_e_threshold=20.0,  # Allow similar colors
                        min_percentage=10.0,  # At least 10% coverage
                    )

                    for r in results.results:
                        print(f"Image {r.image_id}: score {r.match_score:.2f}")

                    # Search by color family
                    earth_images = await client.colors.search(
                        color_family="earth_tone",
                        limit=100,
                    )

                    # Search by color name
                    brass_images = await client.colors.search(
                        color_name="brass",
                    )

                    # Paginate through results
                    offset = 0
                    all_results = []
                    while True:
                        page = await client.colors.search(
                            color_family="neutral",
                            limit=50,
                            offset=offset,
                        )
                        all_results.extend(page.results)
                        if not page.has_more:
                            break
                        offset += len(page.results)
                    ```
        """
        ...

    async def search_all(self, *, hex_code: Optional[str] = None, color_name: Optional[str] = None, color_family: Optional[str] = None, delta_e_threshold: float = 15.0, min_percentage: float = 5.0, page_size: int = 50) -> AsyncIterator[ColorSearchResult]:
        """

                Iterate through all color search results with automatic pagination.

                This is a convenience method that handles pagination automatically.
                For manual pagination control, use search() instead.

                Args:
                    hex_code: Hex color code to search for (e.g., "#C4A87C")
                    color_name: Semantic color name (e.g., "walnut", "brass")
                    color_family: Color family (e.g., "wood", "metallic", "earth_tone")
                    delta_e_threshold: Color tolerance using Delta-E (0-100, default: 15)
                    min_percentage: Minimum percentage the color must cover (0-100, default: 5)
                    page_size: Results per page (1-200, default: 50)

                Yields:
                    ColorSearchResult objects one at a time

                Example:
                    ```python
                    # Find all images with earth tone colors
                    async for result in client.colors.search_all(color_family="earth_tone"):
                        print(f"Image {result.image_id}: {result.matched_color.name}")

                    # Collect all matching images
                    all_earth = [r async for r in client.colors.search_all(color_family="earth_tone")]
                    ```
        """
        ...

    async def list_families(self) -> list[ColorFamilyInfo]:
        """

                List available color families.

                Returns all supported color families with their descriptions
                and example colors. Color families are semantic groupings
                useful for interior design and material searches.

                Returns:
                    List of ColorFamilyInfo objects

                Example:
                    ```python
                    families = await client.colors.list_families()

                    for family in families:
                        print(f"{family.display_name}")
                        print(f"  {family.description}")
                        print(f"  Examples: {', '.join(family.example_colors[:3])}")

                    # Available families:
                    # - neutral: Blacks, whites, grays
                    # - earth_tone: Warm, natural colors
                    # - warm: Reds, oranges, yellows
                    # - cool: Blues, greens, purples
                    # - wood: Wood material colors
                    # - stone: Stone and marble colors
                    # - metallic: Metal finishes
                    # - pastel: Soft, muted colors
                    # - vibrant: Bold, saturated colors
                    ```
        """
        ...

    async def batch_extract(self, image_ids: list[str], *, force: bool = False, n_colors: int = 16) -> BatchColorExtractionResult:
        """

                Re-run color extraction for multiple images with custom settings.

                Colors are extracted automatically on upload. Use this only to
                re-extract with different settings (e.g., fewer colors or force refresh).
                Processing happens asynchronously — use get() to check individual results.

                Args:
                    image_ids: List of image IDs to process
                    force: Force re-extraction even if colors exist (default: False)
                    n_colors: Number of dominant colors to extract (3-16, default: 16)

                Returns:
                    BatchColorExtractionResult with queued count and message

                Raises:
                    ValidationError: If image_ids is empty, exceeds limit, or n_colors invalid

                Example:
                    ```python
                    # Re-extract with fewer colors for multiple images
                    image_ids = ["id1", "id2", "id3", "id4", "id5"]
                    result = await client.colors.batch_extract(image_ids, force=True, n_colors=6)
                    print(f"Queued {result.queued_count} images")

                    # Check status of individual images later
                    for image_id in image_ids:
                        status = await client.colors.get(image_id)
                        print(f"{image_id}: {status.status}")
                    ```
        """
        ...
