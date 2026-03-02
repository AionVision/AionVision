from __future__ import annotations
import os
import re
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse
ENV_API_KEY = 'AIONVISION_API_KEY'
ENV_BASE_URL = 'AIONVISION_BASE_URL'
ENV_TIMEOUT = 'AIONVISION_TIMEOUT'
ENV_MAX_RETRIES = 'AIONVISION_MAX_RETRIES'
ENV_TENANT_ID = 'AIONVISION_TENANT_ID'
ENV_PROXY_URL = 'AIONVISION_PROXY_URL'
ENV_ENABLE_TRACING = 'AIONVISION_ENABLE_TRACING'
ENV_RETRY_DELAY = 'AIONVISION_RETRY_DELAY'
ENV_POLLING_INTERVAL = 'AIONVISION_POLLING_INTERVAL'
ENV_POLLING_TIMEOUT = 'AIONVISION_POLLING_TIMEOUT'

def _get_env_float(name: str, default: float) -> float:
    """Get a float value from environment variable with fallback."""
    ...

def _get_env_int(name: str, default: int) -> int:
    """Get an integer value from environment variable with fallback."""
    ...

def _get_env_bool(name: str, default: bool) -> bool:
    """Get a boolean value from environment variable with fallback."""
    ...

def load_dotenv(dotenv_path: Optional[Union[str, Path]] = None, *, override: bool = False) -> bool:
    """

        Load environment variables from a .env file.

        This is a convenience wrapper that requires python-dotenv to be installed.
        If python-dotenv is not installed, this function returns False silently.

        Args:
            dotenv_path: Path to .env file (str or Path). If None, searches for
                        .env in current directory and parent directories.
            override: If True, override existing environment variables.

        Returns:
            True if .env file was loaded, False otherwise.

        Example:
            ```python
            from aion import load_dotenv, AionVision

            # Load .env file before creating client
            load_dotenv()

            # Now use from_env() - it will pick up values from .env
            async with AionVision.from_env() as client:
                result = await client.upload_one("photo.jpg")
            ```

        Note:
            Install python-dotenv with: pip install python-dotenv
            Or install SDK with dotenv extra: pip install aion[dotenv]
    """
    ...
API_KEY_PATTERN = re.compile('^[a-z]+_[A-Za-z0-9_-]{20,}$')


class InsecureTransportWarning(UserWarning):
    """Warning for insecure HTTP transport usage."""


@dataclass
class ClientConfig:
    """

        Configuration for the Aionvision client.

        Attributes:
            api_key: Your Aionvision API key (e.g., aion_AbCd1234...)
            base_url: API base URL (default: production)
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts for transient failures
            retry_delay: Initial delay between retries (exponential backoff)
            polling_interval: Interval for polling operations (auto-describe)
            polling_timeout: Maximum time to wait for polling operations
            tenant_id: Optional tenant ID for multi-tenant deployments
            proxy_url: Optional proxy URL for network requests
            circuit_breaker_enabled: Enable circuit breaker for resilience
            circuit_breaker_failure_threshold: Failures before opening circuit
            circuit_breaker_success_threshold: Successes to close circuit
            circuit_breaker_timeout: Seconds before attempting recovery
            enable_logging: Enable structured logging for HTTP requests
            enable_tracing: Enable OpenTelemetry tracing (requires tracing extra)
            tracing_service_name: Service name for tracing spans
            propagate_trace_context: Send W3C traceparent/tracestate headers
            send_correlation_id: Send X-Correlation-ID header with requests
            send_request_id: Send X-Request-ID header with requests
    """
    api_key: str
    base_url: str = 'https://api.aionvision.tech/api/v2'
    timeout: float = 300.0
    max_retries: int = 3
    retry_delay: float = 1.0
    polling_interval: float = 2.0
    polling_timeout: float = 360.0
    tenant_id: Optional[str] = field(default_factory=lambda: os.environ.get(ENV_TENANT_ID))
    proxy_url: Optional[str] = field(default_factory=lambda: os.environ.get(ENV_PROXY_URL))
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_success_threshold: int = 2
    circuit_breaker_timeout: float = 30.0
    enable_logging: bool = True
    enable_tracing: bool = False
    tracing_service_name: str = 'aionvision-sdk'
    propagate_trace_context: bool = True
    send_correlation_id: bool = True
    send_request_id: bool = True

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        ...

    @property
    def auth_header(self) -> dict[str, str]:
        """Get the authorization header for API requests."""
        ...

    @property
    def default_headers(self) -> dict[str, str]:
        """Get default headers including authorization and tenant ID."""
        ...

    @classmethod
    def from_env(cls, *, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: Optional[float] = None, max_retries: Optional[int] = None, retry_delay: Optional[float] = None, polling_interval: Optional[float] = None, polling_timeout: Optional[float] = None, tenant_id: Optional[str] = None, proxy_url: Optional[str] = None, enable_tracing: Optional[bool] = None, **kwargs) -> ClientConfig:
        """

                Create configuration from environment variables with optional overrides.

                Environment variables:
                    AIONVISION_API_KEY: API key (required if not provided)
                    AIONVISION_BASE_URL: Base URL (optional)
                    AIONVISION_TIMEOUT: Request timeout in seconds (optional)
                    AIONVISION_MAX_RETRIES: Maximum retry attempts (optional)
                    AIONVISION_RETRY_DELAY: Initial retry delay in seconds (optional)
                    AIONVISION_POLLING_INTERVAL: Polling interval in seconds (optional)
                    AIONVISION_POLLING_TIMEOUT: Polling timeout in seconds (optional)
                    AIONVISION_TENANT_ID: Tenant ID for multi-tenant (optional)
                    AIONVISION_PROXY_URL: Proxy URL (optional)
                    AIONVISION_ENABLE_TRACING: Enable OpenTelemetry tracing (optional)

                Args:
                    api_key: Override for API key
                    base_url: Override for base URL
                    timeout: Override for timeout
                    max_retries: Override for max retries
                    retry_delay: Override for retry delay
                    polling_interval: Override for polling interval
                    polling_timeout: Override for polling timeout
                    tenant_id: Override for tenant ID
                    proxy_url: Override for proxy URL
                    enable_tracing: Override for enable_tracing
                    **kwargs: Additional configuration options

                Returns:
                    ClientConfig instance

                Raises:
                    ValueError: If API key not provided and not in environment
        """
        ...
