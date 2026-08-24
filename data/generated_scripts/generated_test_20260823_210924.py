from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.facebook.com/")
    page.click("a:has-text('Log In')")
    page.click("a:has-text('Create new account')")
    browser.close()