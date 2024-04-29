"""
Notes:
* playwritght installed using at the terminal: pipenv install playwright
* Install dependencies and browsers: playwright install --with-deps chromium
* Install asynchio: pipenv install pytest-asyncio
* To get pytest reports in html format: pipenv install pytest-html
* To get pytest reports in csv format: pipenv install pytest-csv
* On MacOS install Xserver: brew install xquartz
* Before running test that open a browser window start Xserver on host: xhost +localhost
* Use IP addr of server when testing from remote MacOS machine due to 
    IT not allowing access to DNS
* Use --ignore-https-errors to ignore cert errors
* Example of starting codegen: playwright codegen --ignore-https-errors https://10.243.241.224:3443/smx/
* VSCode extension not working

TODO List:
* Consider reusing the login fixture for all tests - log in once
"""

import re
import pytest
import time
from playwright.sync_api import Page, expect

# ------ Variables -----
# This section should be moved to a config file
SMX_URL = "https://10.243.241.224:3443"
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "test123"  # nosec
VISIBLE_TIMEOUT = 60 * 1000  # in milliseconds
SCREENSHOT_PATH = "tests/results/screenhots"
STATE_PATH = "tests/results/state"
DEVICE_NAME = "gayles-sandbox"

# ----- Fixtures -----


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    """Run insecure mode to ignore cert errors"""
    return {
        "ignore_https_errors": True,
    }


@pytest.fixture(name="login")
def fixture_login(page: Page) -> Page:
    """Log into SMx and return the page object"""
    page.goto(get_route("/smx"))
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill(LOGIN_USERNAME)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(LOGIN_PASSWORD)
    page.get_by_role("button", name="Login").click()

    # Wait for the next page to load checking last objects to be visible
    page.get_by_role("link", name="Export").wait_for(timeout=VISIBLE_TIMEOUT)
    page.get_by_role("link", name="Action").wait_for(timeout=VISIBLE_TIMEOUT)
    page.get_by_role("button", name="Column Visibility ").wait_for(
        timeout=VISIBLE_TIMEOUT
    )
    page.wait_for_url(re.compile(".*/smx/network"), timeout=VISIBLE_TIMEOUT)

    # return page
    yield page


@pytest.fixture(name="network_page")
def fixture_network_page(login) -> Page:
    """Navigate to the network page and return the page object"""
    page = login
    if get_route("/smx/network") not in page.url:
        page.goto(get_route("/smx/network"))
        page.get_by_role("link", name="Export").wait_for(timeout=VISIBLE_TIMEOUT)
        page.get_by_role("link", name="Action").wait_for(timeout=VISIBLE_TIMEOUT)
        page.get_by_role("button", name="Column Visibility ").wait_for(
            timeout=VISIBLE_TIMEOUT
        )
        # page.get_by_role("button", name="Create").wait_for(timeout=VISIBLE_TIMEOUT)
        page.wait_for_url(re.compile(".*/smx/network"), timeout=VISIBLE_TIMEOUT)
    # return page
    yield page


# ----- Utilities -----
def get_route(page_route: str) -> str:
    """Get the route for the page"""
    return f"{SMX_URL}{page_route}"


def page_screenshot(page: Page, name: str) -> None:
    """Take a screenshot of the page"""
    page.screenshot(path=f"{SCREENSHOT_PATH}/{name}.png")


# ----- Tests -----


def test_network_device_page_by_name_sort(network_page) -> None:
    """Validate a device can be found and displayed
    when entry table sorted by name.
    """
    page = network_page
    page.locator(".datatable-search-input-cls").first.click()
    page.locator(".datatable-search-input-cls").first.fill(DEVICE_NAME)
    page.get_by_role("link", name="gayles-sandbox").wait_for(timeout=VISIBLE_TIMEOUT)
    expect(page.get_by_role("link", name="gayles-sandbox")).to_be_visible()
    page.get_by_role("link", name="gayles-sandbox").click()

    # Wait for animation to stop
    screenshotA = page.screenshot()
    screenshotB = page.screenshot()
    while screenshotA != screenshotB:
        time.sleep(0.1)
        screenshotA = screenshotB
        screenshotB = page.screenshot()

    rexp = re.compile(f".*/smx/network/node/.*currentNetwork={DEVICE_NAME}")
    # page.wait_for_url(rexp, timeout=VISIBLE_TIMEOUT)
    expect(page).to_have_url(re.compile(".*/smx"))


def test_logout_from_network_page(network_page) -> None:
    """Logout from the network page."""
    page = network_page
    page.get_by_title(LOGIN_USERNAME).click()
    page.get_by_role("link", name="Log out").wait_for(timeout=VISIBLE_TIMEOUT)
    page.get_by_role("link", name="Log out").click()
    page.get_by_role("button", name="Login").wait_for(timeout=VISIBLE_TIMEOUT)
    expect(page).to_have_url(re.compile(".*/smx"))


# ----- Deprecated Tests -----


# @pytest.mark.skip(reason="Deprecated")
# def test_login(page: Page) -> None:
#     """Login.  Used mouse clicks for simplicity.
#     Deprecate in favor of login always performed by fixture.
#     """
#     page.goto(get_route("/smx"))
#     page.get_by_placeholder("Username").click()
#     page.get_by_placeholder("Username").fill(LOGIN_USERNAME)
#     page.get_by_placeholder("Password").click()
#     page.get_by_placeholder("Password").fill(LOGIN_PASSWORD)
#     page.get_by_role("button", name="Login").click()

#     # Page load check by last few object to appear - checking load state does not work
#     # page.get_by_role("link", name="MakeMeFail").wait_for() # used to test failure
#     page.get_by_role("link", name="Export").wait_for(timeout=VISIBLE_TIMEOUT)
#     page.get_by_role("link", name="Action").wait_for(timeout=VISIBLE_TIMEOUT)
#     page.get_by_role("button", name="Column Visibility ").wait_for(
#         timeout=VISIBLE_TIMEOUT
#     )
#     page.get_by_role("button", name="Create").wait_for(timeout=VISIBLE_TIMEOUT)

#     # Verify the expected url route
#     expect(page).to_have_url(re.compile(".*/smx/network"))
#     # page_screenshot(page, __name__ + " network_page") # not needed for test


# @pytest.mark.skip(reason="Deprecated")
# def test_network_page_first_page_after_long(login) -> None:
#     """Validate network page is the first page seen after login.
#     Deprecate in favor of login always checks initial url.
#     """
#     expect(login).to_have_url(re.compile(".*/smx/network"))
