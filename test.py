from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to LinkedIn login page
    page.goto("https://www.linkedin.com/login")

    # Enter username and password
    page.fill('input[name="session_key"]', 'rahulsamantcoc119@gmail.com')
    page.fill('input[name="session_password"]', '7248048085R@s')

    # Click the login button
    page.click('button[type="submit"]')

    # Wait for navigation to ensure login is successful
    page.wait_for_navigation()

    # Perform post-login actions here

    # Close browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
