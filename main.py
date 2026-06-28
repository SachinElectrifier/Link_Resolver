import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
import json

def clean_snapchat_url(full_url: str) -> str:
    """Strip query parameters, keep only the base profile URL."""
    parsed = urlparse(full_url)
    return f"https://www.snapchat.com{parsed.path}"

async def resolve_and_extract(link: str) -> dict:
    """Open shortened Snapchat link, resolve to full URL, and extract name + clean URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(link)
        await page.wait_for_timeout(3000)  # wait for redirect
        final_url = page.url
        clean_url = clean_snapchat_url(final_url)

        # Extract display name from page title
        title = await page.title()
        # Example: "Pavithra Naidu (@pavithra261432) | Snapchat Stories..."
        name = title.split("(@")[0].strip()

        await browser.close()
        return {"name": name, "url": clean_url}

async def main():
    results = []
    # Read multiple links from input file
    with open("input_links.txt") as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        data = await resolve_and_extract(link)
        results.append(data)

    # Write each result on its own line with a comma at the end
    with open("output.json", "w") as f:
        for item in results:
            f.write(json.dumps(item) + ",\n")

if __name__ == "__main__":
    asyncio.run(main())
