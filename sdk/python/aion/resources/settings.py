from __future__ import annotations
from typing import Any, Optional
from ..config import ClientConfig
from ..types.settings import S3ConfigStatus, S3ValidationResult


class SettingsResource:
    """

        Settings operations for the Aionvision SDK.

        Provides methods to configure custom S3 storage for your organization.
        Once configured, you can use storage_target='custom' in upload calls
        to store files directly in your bucket.
    """

    def __init__(self, http: HTTPClient, config: ClientConfig) -> None:
        """

                Initialize the settings resource.

                Args:
                    http: HTTP client for API communication
                    config: Client configuration
        """
        ...

    async def configure_custom_s3(self, access_key_id: str, secret_access_key: str, bucket_name: str, region: str) -> S3ConfigStatus:
        """

                Configure your organization's S3 bucket for custom storage.

                After configuration, you can use storage_target='custom' in upload calls
                to store files directly in your bucket instead of Aionvision's bucket.

                The provided credentials are validated by testing bucket access,
                then encrypted and stored securely on Aionvision's servers.

                Args:
                    access_key_id: AWS access key ID (must have s3:PutObject permission)
                    secret_access_key: AWS secret access key
                    bucket_name: S3 bucket name (must already exist)
                    region: AWS region (e.g., 'us-east-1', 'eu-west-2')

                Returns:
                    S3ConfigStatus with configuration details

                Raises:
                    ValidationError: If credentials are invalid or bucket is inaccessible
                    PermissionError: If you don't have admin permission on the organization

                Example:
                    ```python
                    status = await client.settings.configure_custom_s3(
                        access_key_id="AKIAIOSFODNN7EXAMPLE",
                        secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                        bucket_name="my-company-uploads",
                        region="us-east-1"
                    )
                    print(f"Configured: {status.bucket_name}")
                    ```
        """
        ...

    async def get_custom_s3_status(self) -> S3ConfigStatus:
        """

                Check if custom S3 is configured for your organization.

                Returns configuration status without exposing sensitive credentials.

                Returns:
                    S3ConfigStatus with current configuration status

                Example:
                    ```python
                    status = await client.settings.get_custom_s3_status()
                    if status.configured:
                        print(f"Using bucket: {status.bucket_name} in {status.region}")
                    else:
                        print("Custom S3 not configured")
                    ```
        """
        ...

    async def remove_custom_s3(self) -> dict[str, Any]:
        """

                Remove custom S3 configuration.

                After removal, all uploads will use the default Aionvision bucket.
                Existing files in your bucket are not affected.

                Returns:
                    Dictionary with removal status

                Raises:
                    PermissionError: If you don't have admin permission

                Example:
                    ```python
                    result = await client.settings.remove_custom_s3()
                    print(result["message"])
                    ```
        """
        ...

    async def validate_custom_s3(self) -> S3ValidationResult:
        """

                Validate that custom S3 configuration is still working.

                Tests bucket access using stored credentials. Useful for health
                checks and debugging access issues.

                Returns:
                    S3ValidationResult with validation status

                Example:
                    ```python
                    result = await client.settings.validate_custom_s3()
                    if result.valid:
                        print("S3 configuration is valid")
                    else:
                        print(f"S3 validation failed: {result.error}")
                    ```
        """
        ...
