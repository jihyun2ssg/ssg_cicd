import asyncio
from playwright.async_api import async_playwright

async def capture_full_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.ssg.com", wait_until="networkidle")

        # 스크롤을 끝까지 내려서 모든 콘텐츠 로딩
        previous_height = None
        while True:
            current_height = await page.evaluate("document.body.scrollHeight")
            if previous_height == current_height:
                break
            previous_height = current_height
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)  # 1초 대기

        # 전체 페이지 캡처
        await page.screenshot(path="ssg_fullpage.png", full_page=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_full_page())