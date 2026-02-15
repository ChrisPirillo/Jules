from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/quicktools/index.html")
        page.wait_for_selector(".tool-card")

        # 1. Screenshot Dashboard with 200+ Badge
        page.screenshot(path="verification/dashboard_200.png")
        print("Dashboard screenshot saved.")

        # 2. Check Title
        title = page.title()
        if "Tooltimate" in title:
            print("PASS: Title updated.")
        else:
            print(f"FAIL: Title mismatch ({title}).")

        # 3. Check Category Badge in Tool
        page.click(".tool-card[data-tool='mortgage-calc']")
        page.wait_for_selector("#tool-category-badge")
        cat = page.locator("#tool-category-badge").text_content()
        print(f"Category Badge: {cat}")
        if cat == "Finance":
            print("PASS: Category Badge correct.")

        page.screenshot(path="verification/tool_badge.png")
        browser.close()

run()
