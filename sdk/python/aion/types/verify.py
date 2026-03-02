from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class VerificationIssue:
    """

        A single issue found during verification.

        Attributes:
            type: Type of issue (e.g., "hallucination", "inaccuracy", "missing")
            description: Description of the issue
            severity: Severity level (low, medium, high, critical)
            claim: The specific claim that was flagged
            confidence: Confidence in this issue detection
    """
    type: str
    description: str
    severity: str = 'medium'
    claim: Optional[str] = None
    confidence: Optional[float] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VerificationIssue:
        """Create VerificationIssue from API response data."""
        ...


@dataclass(frozen=True)
class VerificationResult:
    """

        Result from content verification.

        Attributes:
            operation_id: Unique operation identifier
            is_verified: Whether the content is verified as accurate
            confidence_score: Overall confidence score (0-1)
            risk_level: Risk level (low, medium, high, critical)
            hallucination_probability: Probability of hallucination (0-1)
            verified_claims: List of claims that were verified
            issues: List of issues found
            summary: Summary of verification results
            processing_time_ms: Time to process verification
            providers_used: AI providers used for verification
    """
    operation_id: str
    is_verified: bool
    confidence_score: float
    risk_level: str
    hallucination_probability: float = 0.0
    verified_claims: Optional[list[str]] = None
    issues: Optional[list[VerificationIssue]] = None
    summary: Optional[str] = None
    processing_time_ms: int = 0
    providers_used: Optional[list[str]] = None

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> VerificationResult:
        """Create VerificationResult from API response data."""
        ...
