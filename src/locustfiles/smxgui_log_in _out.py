from locust import run_single_user, task
from locust_plugins.users.playwright import PlaywrightUser, PageWithRetry, pw, event
import time
import re

# ------ Variables -----
# This section should be moved to a config file
SMX_URL = "https://10.243.241.224:3443"
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "test123"  # nosec
VISIBLE_TIMEOUT = 60 * 1000  # in milliseconds
SCREENSHOT_PATH = "tests/results/screenhots"
STATE_PATH = "tests/results/state"
DEVICE_NAME = "gayles-sandbox"


def get_route(page_route: str) -> str:
    """Get the route for the page"""
    return f"{SMX_URL}{page_route}"


class LogInOutUser(PlaywrightUser):
    browser_type = (
        "chromium"  # Only loading chromium for prototype - consider parameterizing
    )
    headless = True  # parameterize this thing
    multiplier = 1  # controls the number of browers open per user - that is NUTS
    error_screenshot_made = False

    @task
    @pw
    async def login_logout(self, page: PageWithRetry):
        """Log into and then log out of SMx"""
        try:
            async with event(self, "LogInOutUser: SMx Login"):
                await page.goto(get_route("/smx"))
                await page.get_by_placeholder("Username").click()
                await page.get_by_placeholder("Username").fill(LOGIN_USERNAME)
                await page.get_by_placeholder("Password").click()
                await page.get_by_placeholder("Password").fill(LOGIN_PASSWORD)
                await page.get_by_role("button", name="Login").click()

                # Wait for the next page to load waiting for last objects to be visible
                await page.get_by_role("link", name="Export").wait_for(
                    timeout=VISIBLE_TIMEOUT
                )
                await page.get_by_role("link", name="Action").wait_for(
                    timeout=VISIBLE_TIMEOUT
                )
                await page.get_by_role("button", name="Column Visibility ").wait_for(
                    timeout=VISIBLE_TIMEOUT
                )
                await page.wait_for_url(
                    re.compile(".*/smx/network"), timeout=VISIBLE_TIMEOUT
                )

            async with event(self, "LogInOutUser: SMx Logout"):
                await page.get_by_title(LOGIN_USERNAME).click()
                await page.get_by_role("link", name="Log out").wait_for(
                    timeout=VISIBLE_TIMEOUT
                )
                await page.get_by_role("link", name="Log out").click()
                await page.get_by_role("button", name="Login").wait_for(
                    timeout=VISIBLE_TIMEOUT
                )
                await page.wait_for_url(re.compile(".*/smx"), timeout=VISIBLE_TIMEOUT)
        except:
            # found that tracebacks do not bubble up to help with debugging - need to be claravoiant
            pass  # nosec


if __name__ == "__main__":
    run_single_user(LogInOutUser)
