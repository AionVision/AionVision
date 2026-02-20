"""
Color Analysis and Search: Retrieve and search by color properties.

Colors are extracted automatically when images are uploaded — no extra call needed.

Demonstrates:
- Retrieving automatically extracted colors
- Re-extracting with custom settings (optional)
- Searching images by hex color
- Searching by color family (earth tones, blue, etc.)
"""

import asyncio

from aion import AionVision


async def get_colors():
    """Get automatically extracted colors for an image."""

    async with AionVision.from_env() as client:

        # Colors are extracted automatically on upload — just retrieve them
        result = await client.colors.get("image-id")

        if result.is_completed:
            analysis = result.color_analysis
            print(f"Dominant colors ({len(analysis.dominant_colors)}):")
            for color in analysis.dominant_colors:
                print(f"  {color.name}: {color.hex} ({color.percentage:.1f}%)")
                print(f"    RGB({color.rgb.r}, {color.rgb.g}, {color.rgb.b})")

            print(f"Temperature: {analysis.analytics.temperature}")
            print(f"Brightness: {analysis.analytics.brightness}")
            print(f"Saturation: {analysis.analytics.saturation}")

        # Optional: re-extract with fewer colors
        result = await client.colors.extract("image-id", n_colors=6, force=True)


async def search_by_color():
    """Search images by color properties."""

    async with AionVision.from_env() as client:

        # Search by hex color
        results = await client.colors.search(hex_code="#C4A87C")
        print(f"Found {results.total_count} images with similar colors")
        for r in results.results:
            print(f"  {r.image_id}: match_score={r.match_score:.2f}")

        # Search by color family
        results = await client.colors.search(color_family="earth_tone")
        print(f"Found {results.total_count} earth-tone images")

        # List available color families
        families = await client.colors.list_families()
        for family in families:
            print(f"  {family.name}: {family.description}")


async def batch_re_extract():
    """Re-extract colors with custom settings for multiple images."""

    async with AionVision.from_env() as client:

        # Colors are already extracted on upload — use batch_extract only
        # to re-run with different settings
        result = await client.colors.batch_extract(
            image_ids=["img-1", "img-2", "img-3"],
            force=True,
            n_colors=6,
        )
        print(f"Queued {result.queued_count} images for re-extraction")


if __name__ == "__main__":
    asyncio.run(get_colors())
