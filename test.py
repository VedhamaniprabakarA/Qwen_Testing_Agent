from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to the test page
    page.goto("https://example.com")
    
    # Test case 1: Fill username and password
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "test_user")
    page.fill('input[name="password"]', "test_password")
    page.click('button[type="submit"]')
    
    # Test case 2: Verify login success
    assert page.title() == "Dashboard", "Login failed - Expected dashboard title"
    
    # Test case 3: Click profile link
    page.click('a[href="/profile"]')
    
    # Test case 4: Verify profile page
    assert page.title() == "Profile", "Profile page not loaded"
    
    # Test case 5: Click settings link
    page.click('a[href="/settings"]')
    
    # Test case 6: Verify settings page
    assert page.title() == "Settings", "Settings page not loaded"
    
    # Test case 7: Change password
    page.fill('input[name="new_password"]', "new_password_123")
    page.click('button[type="submit"]')
    
    # Test case 8: Verify password change
    assert page.title() == "Password updated", "Password change failed"
    
    # Test case 9: Click LinkedIn link
    page.click('a[href="https://www.linkedin.com/company/orange"]')
    
    # Test case 10: Verify LinkedIn page
    assert page.title() == "LinkedIn", "LinkedIn page not loaded"
    
    # Test case 11: Click Google link
    page.click('a[href="https://www.google.com"]')
    
    # Test case 12: Verify Google page
    assert page.title() == "Google", "Google page not loaded"
    
    # Test case 13: Click Facebook link
    page.click('a[href="https://www.facebook.com"]')
    
    # Test case 14: Verify Facebook page
    assert page.title() == "Facebook", "Facebook page not loaded"
    
    # Close browser
    browser.close()