from playwright.sync_api import sync_playwright


def test_login_page_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        page = browser.new_page()

        page.goto(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )

        page.wait_for_load_state("networkidle")

        assert page.locator("input[name='username']").is_visible()
        assert page.locator("input[name='password']").is_visible()

        login_button = page.locator("button[type='submit']")
        assert login_button.is_visible()
        assert login_button.inner_text() == "Login"

        input("Press Enter to close...")
        browser.close()


if __name__ == "__main__":
    test_login_page_ui()