"""Take full-page PNG screenshots of the timeline and checklist HTML files."""

from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"C:\Users\Ty\Desktop\ArcQuests"

pages = [
    ("http://localhost:8080/timeline.html", f"{OUTPUT_DIR}\\timeline.png"),
    ("http://localhost:8080/checklist.html", f"{OUTPUT_DIR}\\checklist.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for url, out_path in pages:
        page = browser.new_page(viewport={"width": 900, "height": 800})
        page.goto(url, wait_until="networkidle")
        # Wait for fonts to load
        page.wait_for_timeout(1500)
        page.screenshot(path=out_path, full_page=True)
        print(f"Saved: {out_path}")

    browser.close()

print("Done!")
