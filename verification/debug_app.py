from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

        # Proper error handling
        def log_error(err):
             print(f"Browser Error: {err}")
             print(f"Stack: {err.stack}")

        page.on("pageerror", log_error)

        page.goto("http://localhost:8080/index.html")
        page.wait_for_timeout(2000) # Wait a bit for JS to run

        # Check if .tool-card exists
        count = page.locator(".tool-card").count()
        print(f"Tool cards found: {count}")

        browser.close()

if __name__ == "__main__":
    run()
