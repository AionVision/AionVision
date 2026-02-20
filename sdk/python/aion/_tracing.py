"""OpenTelemetry tracing integration for the Aion SDK.

This module provides optional distributed tracing support using OpenTelemetry.
Tracing is opt-in and requires installing the 'tracing' extra:

    pip install aion[tracing]

The module also provides correlation ID support that works WITHOUT OpenTelemetry
installed, enabling request tracking and log correlation even without full tracing.

Usage:
    from aion import AionVision, configure_tracing

    # Configure tracing before creating client (optional)
    configure_tracing(service_name="my-app", endpoint="http://jaeger:4317")

    async with AionVision(api_key="...", enable_tracing=True) as client:
        result = await client.upload("photo.jpg")  # Creates client-side span
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import TracerProvider

# Context variables for correlation (work without OTel) — internal, not part of public API
correlation_id_var: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)  # internal
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)  # internal


def is_tracing_available() -> bool:
    """
    Check if OpenTelemetry is installed and available.

    Returns:
        True if OpenTelemetry packages are installed, False otherwise.
    """
    try:
        import opentelemetry  # noqa: F401
        return True
    except ImportError:
        return False


def configure_tracing(
    *,
    service_name: str = "aionvision-sdk",
    service_version: Optional[str] = None,
    endpoint: Optional[str] = None,
    tracer_provider: Optional[TracerProvider] = None,
) -> bool:
    """
    Configure OpenTelemetry tracing for the SDK.

    This should be called once at application startup, before creating
    any AionVision client instances.

    Args:
        service_name: Name of this service in traces
        service_version: Service version (defaults to SDK version)
        endpoint: OTLP exporter endpoint (if not using existing provider)
        tracer_provider: Existing TracerProvider to use

    Returns:
        True if tracing was configured, False if OTel not available

    Example:
        >>> configure_tracing(
        ...     service_name="my-app",
        ...     endpoint="http://jaeger:4317"
        ... )
        True
    """
    ...


def set_correlation_id(correlation_id: str) -> None:
    """
    Set the correlation ID for the current context.

    Use this to propagate an incoming correlation ID from an upstream service.

    Args:
        correlation_id: The correlation ID to set.
    """
    ...
