import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse

def clean_snapchat_url(full_url: str) -> str:
    parsed = urlparse(full_url)
    return f"https://www.snapchat.com{parsed.path}"

async def resolve_and_extract(link: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(link)
        await page.wait_for_timeout(3000)
        final_url = page.url
        clean_url = clean_snapchat_url(final_url)

        title = await page.title()
        name = title.split("(@")[0].strip()

        await browser.close()
        return {"name": name, "url": clean_url}

async def main():
    with open("input_links.txt") as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        data = await resolve_and_extract(link)
        # 👇 Instead of saving, just print
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
