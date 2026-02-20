from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class S3ConfigStatus:
    """Status of custom S3 configuration."""
    configured: bool
    bucket_name: Optional[str] = None
    region: Optional[str] = None
    configured_at: Optional[str] = None
    is_validated: Optional[bool] = None
    error: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> S3ConfigStatus:
        """Create S3ConfigStatus from API response."""
        ...


@dataclass(frozen=True)
class S3ValidationResult:
    """Result of S3 configuration validation."""
    valid: bool
    bucket_name: Optional[str] = None
    region: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> S3ValidationResult:
        """Create S3ValidationResult from API response."""
        ...
