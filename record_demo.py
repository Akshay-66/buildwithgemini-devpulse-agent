import asyncio
import os
from playwright.async_api import async_playwright

ARTIFACTS_DIR = "/config/.gemini/antigravity/brain/d365f53a-8e45-4a8f-aa9e-36056d504a27"
VIDEO_DIR = os.path.join(ARTIFACTS_DIR, "demo_videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

async def record():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        print("Navigating to http://localhost:8080...")
        await page.goto("http://localhost:8080")
        await page.wait_for_timeout(2000)

        # Prompt 1: Core app function
        prompt_1 = "What are the active support tickets and system status for DevPulse?"
        print(f"Typing Prompt 1: {prompt_1}")
        await page.fill("#input", prompt_1)
        await page.wait_for_timeout(1000)
        await page.click("button")
        
        # Wait for reply
        print("Waiting for response to Prompt 1...")
        await page.wait_for_timeout(15000)

        # Prompt 2: Richer prompt showing off tool call / database lookup / image generation
        prompt_2 = "Generate a short architecture diagram video for our server status monitor."
        print(f"Typing Prompt 2: {prompt_2}")
        await page.fill("#input", prompt_2)
        await page.wait_for_timeout(1000)
        await page.click("button")

        # Wait for reply and video rendering
        print("Waiting for response to Prompt 2...")
        await page.wait_for_selector("video", timeout=90000)
        await page.wait_for_timeout(5000) # Give video a few seconds to play

        video_path = await page.video.path()
        print("Video recorded to:", video_path)

        await context.close()
        await browser.close()
        return video_path

if __name__ == "__main__":
    path = asyncio.run(record())
    print("Final recorded demo video path:", path)
