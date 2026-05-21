"""
Interactive behavior tests for the Tailwind CSS + Alpine.js
professional-site assignment.

These tests drive a real Chrome browser and check that the assignment's
two pieces of Alpine-powered interactivity actually work:

  - The hamburger button toggles the visibility of the nav link group
    when the viewport is narrower than the md breakpoint.
  - The image carousel advances to a different image when the user
    clicks a "next" control, and all carousel images are no wider
    than 1536 pixels (Tailwind's 2xl breakpoint).

Structural tests live in test_index.py.

Requires:
  - Selenium 4+
  - Google Chrome
"""

import json
import re
import time
import pytest
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


MAIN_PAGE = "professional_site.html"
MAX_IMAGE_WIDTH_PX = 1536  # Tailwind's 2xl breakpoint
HIDE_AT_MD_RE = re.compile(r"\b(md|lg|xl|2xl):hidden\b")


def _build_url(site_url, page):
    return site_url.rstrip("/") + "/" + page


def _discover_all_pages(driver, main_url):
    """Visit the home page and return [main_url] plus the other linked pages."""
    driver.get(main_url)
    nav = driver.find_element(By.TAG_NAME, "nav")
    pages = [main_url]
    for a in nav.find_elements(By.TAG_NAME, "a"):
        href = a.get_attribute("href") or ""
        abs_href = urljoin(main_url, href).split("#")[0]
        if (
            abs_href.lower().endswith(".html")
            and abs_href not in pages
        ):
            pages.append(abs_href)
    return pages


def _find_carousel_root(driver):
    """
    Return the first element on the current page that looks like an Alpine
    carousel: it has an `x-data` attribute mentioning both an images list
    and a current-index variable, AND contains an <img> with an Alpine
    `:src` or `x-bind:src` binding.
    """
    candidates = driver.find_elements(By.CSS_SELECTOR, "[x-data]")
    for c in candidates:
        data = c.get_attribute("x-data") or ""
        if "images" not in data and "slides" not in data:
            continue
        if not any(k in data for k in ("current", "index", "active", "slide")):
            continue
        imgs = c.find_elements(
            By.CSS_SELECTOR, "img[\\:src], img[x-bind\\:src]"
        )
        if imgs:
            return c
    return None


class Tests:

    @pytest.fixture(scope="class")
    def settings(self):
        with open("./settings.json", "r") as f:
            yield json.load(f)

    @pytest.fixture(scope="class")
    def main_url(self, settings):
        return _build_url(settings["site_url"], MAIN_PAGE)

    @pytest.fixture(scope="class")
    def driver(self, settings, main_url):
        options = Options()
        options.add_argument("--window-size=1400,1000")
        driver = webdriver.Chrome(options=options)
        driver.get(main_url)
        yield driver
        driver.quit()

    @pytest.fixture(scope="class")
    def all_pages(self, driver, main_url):
        return _discover_all_pages(driver, main_url)

    # ------------------------------------------------------------------
    # Requirement 2 (behavior): hamburger toggle on every page
    # ------------------------------------------------------------------

    def test_hamburger_toggles_menu(self, driver, all_pages):
        """
        Resize narrower than the md breakpoint and confirm that clicking
        the hamburger button changes the visible state of at least one
        element inside the <nav>.
        """
        for url in all_pages:
            driver.get(url)
            # narrow the viewport below the md breakpoint (768px) so the
            # mobile menu is in scope
            driver.set_window_size(400, 900)
            time.sleep(0.3)  # give the layout a moment to settle

            nav = driver.find_element(By.TAG_NAME, "nav")

            # find the hamburger button (the one with @click and md:hidden)
            hamburger = None
            for b in nav.find_elements(By.TAG_NAME, "button"):
                cls = b.get_attribute("class") or ""
                click_attr = (
                    b.get_attribute("@click")
                    or b.get_attribute("x-on:click")
                    or ""
                )
                if click_attr and HIDE_AT_MD_RE.search(cls):
                    hamburger = b
                    break
            assert hamburger is not None, (
                "Page {} has no hamburger button to click.".format(url)
            )

            # snapshot visibility of every nav anchor before the click
            before_visible = [
                a.is_displayed()
                for a in nav.find_elements(By.TAG_NAME, "a")
            ]

            hamburger.click()
            time.sleep(0.3)

            after_visible = [
                a.is_displayed()
                for a in nav.find_elements(By.TAG_NAME, "a")
            ]

            # at least one anchor must have changed visibility
            assert before_visible != after_visible, (
                "Page {} : clicking the hamburger button did not change the "
                "visibility of any nav link. Make sure the link group is "
                "wired to the Alpine state via `x-show` or a bound `class` "
                "with `hidden`/`block`.".format(url)
            )

            # restore the default window size for downstream tests
            driver.set_window_size(1400, 1000)

    # ------------------------------------------------------------------
    # Requirement 4: Alpine.js image carousel
    # ------------------------------------------------------------------

    @pytest.fixture(scope="class")
    def carousel_root(self, driver, all_pages):
        """The carousel container element, found on one of the 3 pages."""
        for url in all_pages:
            driver.get(url)
            time.sleep(0.3)
            root = _find_carousel_root(driver)
            if root is not None:
                return root
        return None

    def test_carousel_exists(self, carousel_root):
        assert carousel_root is not None, (
            "No Alpine.js image carousel was found on any of the three "
            "pages. The carousel must be a single element with an `x-data` "
            "attribute mentioning both an images list and a current-index "
            "variable, containing an <img> with `:src` (or `x-bind:src`) "
            "and at least two <button> controls."
        )

    def test_carousel_has_three_images(self, carousel_root):
        # count distinct image sources in the carousel's data, AND/OR
        # the static <img> elements inside the container
        data = carousel_root.get_attribute("x-data") or ""
        url_like = re.findall(r"['\"]([^'\"]+\.(?:png|jpg|jpeg|gif|webp))['\"]", data)
        if len(url_like) >= 3:
            return  # found enough via x-data
        # fall back: count <img> elements with src or :src
        img_srcs = set()
        for img in carousel_root.find_elements(By.TAG_NAME, "img"):
            for attr in ("src", ":src", "x-bind:src"):
                v = img.get_attribute(attr)
                if v:
                    img_srcs.add(v)
        assert len(url_like) + len(img_srcs) >= 3, (
            "The carousel must reference at least 3 distinct images. "
            "Found {} in x-data and {} on <img> tags."
            .format(len(url_like), len(img_srcs))
        )

    def test_carousel_advances_on_click(self, driver, carousel_root):
        """Clicking the carousel's next control must change the image src."""
        # find the bound <img> inside the carousel
        imgs = carousel_root.find_elements(
            By.CSS_SELECTOR, "img[\\:src], img[x-bind\\:src]"
        )
        assert imgs, (
            "The carousel container has no <img> with `:src` or "
            "`x-bind:src`. The image source must be bound to Alpine state."
        )
        img = imgs[0]
        original_src = img.get_attribute("src")

        # find the buttons inside the carousel
        buttons = [
            b for b in carousel_root.find_elements(By.TAG_NAME, "button")
            if (b.get_attribute("@click") or b.get_attribute("x-on:click"))
        ]
        assert len(buttons) >= 2, (
            "The carousel must have at least 2 clickable controls "
            "(<button> with `@click` or `x-on:click`). Found {}."
            .format(len(buttons))
        )

        # click each one until the src changes
        changed = False
        for b in buttons:
            try:
                b.click()
            except Exception:
                continue
            time.sleep(0.3)
            new_src = img.get_attribute("src")
            if new_src != original_src:
                changed = True
                break

        assert changed, (
            "Clicking the carousel's controls did not change the displayed "
            "image's `src` attribute. Make sure the <img> uses `:src` and "
            "that the button's `@click` updates the current-index state."
        )

    def test_carousel_images_within_max_width(self, driver, carousel_root):
        """
        Every distinct image used by the carousel must be no wider than
        1536 pixels (Tailwind's 2xl breakpoint).
        """
        # collect every src we've ever seen on the bound <img> by clicking
        # each control once and snapshotting
        imgs = carousel_root.find_elements(By.TAG_NAME, "img")
        seen_srcs = set()
        for img in imgs:
            src = img.get_attribute("src")
            if src:
                seen_srcs.add(src)
        # also walk the carousel by clicking buttons to surface other srcs
        buttons = [
            b for b in carousel_root.find_elements(By.TAG_NAME, "button")
            if (b.get_attribute("@click") or b.get_attribute("x-on:click"))
        ]
        for b in buttons:
            try:
                b.click()
            except Exception:
                continue
            time.sleep(0.25)
            for img in carousel_root.find_elements(By.TAG_NAME, "img"):
                src = img.get_attribute("src")
                if src:
                    seen_srcs.add(src)

        assert seen_srcs, "Carousel exposed no image sources to inspect."

        oversized = []
        for src in seen_srcs:
            # ask the browser to load each image off-screen and report
            # its natural width
            natural_width = driver.execute_async_script(
                """
                var src = arguments[0];
                var done = arguments[1];
                var img = new Image();
                img.onload = function () { done(img.naturalWidth); };
                img.onerror = function () { done(-1); };
                img.src = src;
                """,
                src,
            )
            if isinstance(natural_width, (int, float)) and natural_width > MAX_IMAGE_WIDTH_PX:
                oversized.append((src, natural_width))

        assert not oversized, (
            "The following carousel images are wider than {} pixels "
            "(Tailwind's 2xl breakpoint): {}".format(
                MAX_IMAGE_WIDTH_PX, oversized
            )
        )
