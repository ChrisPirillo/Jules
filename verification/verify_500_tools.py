import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs and errors
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda msg: print(f"PAGE ERROR: {msg}"))

        # Load the local file
        file_path = os.path.abspath("quicktools/index.html")
        page.goto(f"file://{file_path}")

        # Wait for tools to appear
        try:
            page.wait_for_selector(".tool-card", timeout=5000)
        except:
            print("Timeout waiting for .tool-card")

        # 1. Verify Tool Count
        tools = page.query_selector_all(".tool-card")
        count = len(tools)
        print(f"Total Tools Found: {count}")

        if count < 500:
            print("FAILED: Expected ~500 tools, found less.")
        else:
            print("PASSED: Tool count meets target.")

        if count > 0:
            # 2. Verify UI Fix (Center Alignment)
            # Click on a tool (e.g., first one)
            tools[0].click()
            try:
                page.wait_for_selector("#tool-view", state="visible", timeout=2000)

                # Check alignment style
                tool_content = page.query_selector("#tool-content")
                style = tool_content.evaluate("el => getComputedStyle(el).justifyContent")
                print(f"Tool Content Justify: {style}")

                # Check Panel Width
                panel = page.query_selector(".glass-panel")
                if panel:
                    width = panel.evaluate("el => getComputedStyle(el).maxWidth")
                    print(f"Panel Max Width: {width}")
                else:
                    print("Panel not found")

                # Screenshot
                page.screenshot(path="verification/tool_ui_fixed.png")
                print("Screenshot saved to verification/tool_ui_fixed.png")
            except Exception as e:
                print(f"Error checking UI: {e}")

        browser.close()

if __name__ == "__main__":
    run()
