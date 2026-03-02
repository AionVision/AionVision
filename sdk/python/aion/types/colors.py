from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional

def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float, handling None and invalid values."""
    ...


class ColorFamily(str, Enum):
    """

        Semantic color family categories.

        Color families are groupings useful for color-based searches.
    """
    NEUTRAL = 'neutral'
    EARTH_TONE = 'earth_tone'
    WARM = 'warm'
    COOL = 'cool'
    METALLIC = 'metallic'
    PASTEL = 'pastel'
    VIBRANT = 'vibrant'


class ColorExtractionStatus(str, Enum):
    """Status of color extraction for an image."""
    PENDING = 'pending'
    QUEUED = 'queued'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass(frozen=True)
class RGB:
    """

        RGB color values.

        Attributes:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
    """
    r: int
    g: int
    b: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> RGB:
        """Create RGB from API response data."""
        ...


@dataclass(frozen=True)
class HSL:
    """

        HSL color values.

        Attributes:
            h: Hue (0-360 degrees)
            s: Saturation (0-100 percent)
            l: Lightness (0-100 percent)
    """
    h: float
    s: float
    l: float

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> HSL:
        """Create HSL from API response data."""
        ...


@dataclass(frozen=True)
class LAB:
    """

        CIE LAB color values.

        LAB is perceptually uniform and used for Delta-E color
        difference calculations.

        Attributes:
            l: Lightness (0-100)
            a: Green-Red axis (-128 to 127)
            b: Blue-Yellow axis (-128 to 127)
    """
    l: float
    a: float
    b: float

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> LAB:
        """Create LAB from API response data."""
        ...


@dataclass(frozen=True)
class DominantColor:
    """

        A dominant color extracted from an image.

        Contains the color in multiple color spaces along with
        semantic naming and classification.

        Attributes:
            rank: Rank by dominance (1 = most dominant)
            percentage: Percentage of image covered by this color
            rgb: RGB color values
            hsl: HSL color values
            lab: LAB color values (for color matching)
            hex: Hex color code (e.g., "#C4A87C")
            name: Semantic color name (e.g., "Walnut", "Brass")
            family: Color family classification
    """
    rank: int
    percentage: float
    rgb: RGB
    hsl: HSL
    lab: LAB
    hex: str
    name: str
    family: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> DominantColor:
        """Create DominantColor from API response data."""
        ...

    @property
    def family_enum(self) -> Optional[ColorFamily]:
        """Get family as enum, or None if not a known family."""
        ...


@dataclass(frozen=True)
class ColorTemperature:
    """

        Color temperature analysis.

        Attributes:
            value: Temperature category ("warm", "cool", "neutral")
            score: Confidence score (0-1)
    """
    value: str
    score: float

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorTemperature:
        """Create ColorTemperature from API response data."""
        ...


@dataclass(frozen=True)
class ColorBrightness:
    """

        Brightness analysis.

        Attributes:
            average: Average brightness value (0-100)
            category: Brightness category ("dark", "medium", "light")
    """
    average: float
    category: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorBrightness:
        """Create ColorBrightness from API response data."""
        ...


@dataclass(frozen=True)
class ColorSaturation:
    """

        Saturation analysis.

        Attributes:
            average: Average saturation value (0-100)
            category: Saturation category ("muted", "medium", "vivid")
    """
    average: float
    category: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorSaturation:
        """Create ColorSaturation from API response data."""
        ...


@dataclass(frozen=True)
class ColorAnalytics:
    """

        Overall color analytics for an image.

        Attributes:
            temperature: Color temperature analysis
            brightness: Brightness analysis
            saturation: Saturation analysis
    """
    temperature: ColorTemperature
    brightness: ColorBrightness
    saturation: ColorSaturation

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorAnalytics:
        """Create ColorAnalytics from API response data."""
        ...


@dataclass(frozen=True)
class ColorAnalysis:
    """

        Complete color analysis for an image.

        Contains extracted dominant colors and overall analytics.

        Attributes:
            version: Analysis algorithm version
            dominant_colors: List of dominant colors ordered by percentage
            analytics: Overall color analytics
            extracted_at: When the analysis was performed
    """
    version: str
    dominant_colors: list[DominantColor]
    analytics: ColorAnalytics
    extracted_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorAnalysis:
        """Create ColorAnalysis from API response data."""
        ...


@dataclass(frozen=True)
class ColorExtractionResult:
    """

        Result of color extraction operation.

        Returned by extract_colors() and get_colors() methods.

        Attributes:
            image_id: ID of the image
            status: Extraction status (pending, queued, processing, completed, failed)
            color_analysis: Full color analysis (if completed)
            extracted_at: When extraction completed
    """
    image_id: str
    status: str
    color_analysis: Optional[ColorAnalysis] = None
    extracted_at: Optional[datetime] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorExtractionResult:
        """Create ColorExtractionResult from API response data."""
        ...

    @property
    def status_enum(self) -> Optional[ColorExtractionStatus]:
        """Get status as enum, or None if not a known status."""
        ...

    @property
    def is_completed(self) -> bool:
        """Check if extraction is completed."""
        ...

    @property
    def is_pending(self) -> bool:
        """Check if extraction is pending or queued."""
        ...


@dataclass(frozen=True)
class ColorSearchResult:
    """

        A single color search result.

        Attributes:
            image_id: ID of the matching image
            match_score: How well the image matches the search (lower = better for Delta-E)
            thumbnail_url: URL to image thumbnail
            color_analysis: Color analysis of the image
    """
    image_id: str
    match_score: float
    thumbnail_url: Optional[str] = None
    color_analysis: Optional[ColorAnalysis] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorSearchResult:
        """Create ColorSearchResult from API response data."""
        ...


@dataclass(frozen=True)
class ColorSearchResponse:
    """

        Paginated color search results.

        Attributes:
            results: List of matching images
            total_count: Total number of matching images
            limit: Number of results requested
            offset: Offset for pagination
    """
    results: list[ColorSearchResult]
    total_count: int
    limit: int
    offset: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorSearchResponse:
        """Create ColorSearchResponse from API response data."""
        ...

    @property
    def has_more(self) -> bool:
        """Check if more results are available."""
        ...


@dataclass(frozen=True)
class ColorFamilyInfo:
    """

        Information about a color family.

        Attributes:
            name: Internal name (e.g., "earth_tone")
            display_name: Human-readable name (e.g., "Earth Tones")
            description: Description of the color family
            example_colors: List of example hex colors
    """
    name: str
    display_name: str
    description: str
    example_colors: list[str]

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> ColorFamilyInfo:
        """Create ColorFamilyInfo from API response data."""
        ...

    @property
    def family_enum(self) -> Optional[ColorFamily]:
        """Get family as enum, or None if not a known family."""
        ...


@dataclass(frozen=True)
class BatchColorExtractionResult:
    """

        Result of batch color extraction request.

        Attributes:
            queued_count: Number of images queued for extraction
            message: Status message
    """
    queued_count: int
    message: str

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> BatchColorExtractionResult:
        """Create BatchColorExtractionResult from API response data."""
        ...
