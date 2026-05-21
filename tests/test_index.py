"""
Structural tests for the Tailwind CSS + Alpine.js professional-site assignment.

These tests load the student's deployed site in a real browser and check
that each of the assignment's structural requirements has been satisfied:

  - the home page (professional_site.html) loads
  - every page has a <nav> with the required brand link, hamburger
    button, link group, and Alpine state
  - the navigation links to two additional pages, which also exist
  - the home page uses responsive breakpoint prefixes at least three times
  - the site contains at least three customizations (arbitrary-value
    classes or rules in css/custom.css)

Behavior tests (hamburger toggle, carousel) live in test_behavior.py.

Requires:
  - Selenium 4+ (uses the modern By API and built-in driver management)
  - Google Chrome
"""

import json
import re
import pytest
from urllib.parse import urljoin
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


MAIN_PAGE = "professional_site.html"
RESPONSIVE_PREFIX_RE = re.compile(r"\b(sm|md|lg|xl|2xl):[A-Za-z0-9_\-\[\]\#\./%]+")
HIDE_AT_MD_RE = re.compile(r"\b(md|lg|xl|2xl):hidden\b")
SHOW_AT_MD_RE = re.compile(r"\b(md|lg|xl|2xl):(flex|grid|block|inline|inline-block|inline-flex|!block|!flex|!grid)\b")
ARBITRARY_VALUE_RE = re.compile(r"class\s*=\s*\"[^\"]*\b[A-Za-z][\w\-]*-\[[^\]]+\][^\"]*\"")


def _build_url(site_url, page):
    return site_url.rstrip("/") + "/" + page


def _discover_other_pages(driver, main_url):
    """
    Find the two other assignment pages by inspecting the home page's nav.

    Returns a list of absolute URLs (excluding the main page itself).
    """
    nav = driver.find_element(By.TAG_NAME, "nav")
    seen = []
    for a in nav.find_elements(By.TAG_NAME, "a"):
        href = a.get_attribute("href") or ""
        abs_href = urljoin(main_url, href).split("#")[0]
        if not abs_href.lower().endswith(".html"):
            continue
        if abs_href == main_url:
            continue
        if abs_href in seen:
            continue
        seen.append(abs_href)
    return seen


class Tests:

    @pytest.fixture(scope="class")
    def settings(self):
        with open("./settings.json", "r") as f:
            yield json.load(f)

    @pytest.fixture(scope="class")
    def driver(self, settings):
        options = Options()
        options.add_argument("--window-size=1400,1000")
        driver = webdriver.Chrome(options=options)
        driver.get(_build_url(settings["site_url"], MAIN_PAGE))
        yield driver
        driver.quit()

    @pytest.fixture(scope="class")
    def main_url(self, settings):
        return _build_url(settings["site_url"], MAIN_PAGE)

    @pytest.fixture(scope="class")
    def other_pages(self, driver, main_url):
        """The two additional assignment pages, discovered from the nav."""
        driver.get(main_url)
        urls = _discover_other_pages(driver, main_url)
        return urls

    @pytest.fixture(scope="class")
    def all_pages(self, main_url, other_pages):
        return [main_url] + list(other_pages)

    # ------------------------------------------------------------------
    # Requirement 1: three pages exist and are linked from the home nav
    # ------------------------------------------------------------------

    def test_main_page_loads(self, driver, main_url):
        driver.get(main_url)
        assert driver.find_element(By.TAG_NAME, "body") is not None

    def test_two_additional_pages_linked(self, other_pages):
        assert len(other_pages) >= 2, (
            "The home page's <nav> must link to at least two additional "
            "HTML pages (in addition to the brand link back to "
            "professional_site.html). Found: {}".format(other_pages)
        )

    def test_additional_pages_exist(self, other_pages):
        for url in other_pages[:2]:
            try:
                with urlopen(url, timeout=10) as response:
                    assert response.status == 200, (
                        "Expected page {} to return HTTP 200 but got {}"
                        .format(url, response.status)
                    )
            except Exception as e:
                raise AssertionError(
                    "Could not load linked page {}: {}".format(url, e)
                )

    # ------------------------------------------------------------------
    # Requirement 2: navigation bar on every page
    # ------------------------------------------------------------------

    def test_nav_on_every_page(self, driver, all_pages):
        for url in all_pages:
            driver.get(url)
            navs = driver.find_elements(By.TAG_NAME, "nav")
            assert len(navs) >= 1, (
                "Page {} has no <nav> element.".format(url)
            )

    def test_brand_link_on_every_page(self, driver, all_pages):
        for url in all_pages:
            driver.get(url)
            nav = driver.find_element(By.TAG_NAME, "nav")
            brand_anchors = nav.find_elements(
                By.CSS_SELECTOR,
                'a[href="{}"], a[href$="/{}"]'.format(MAIN_PAGE, MAIN_PAGE),
            )
            assert len(brand_anchors) >= 1, (
                'Page {} has no nav anchor pointing to "{}".'
                .format(url, MAIN_PAGE)
            )

    def test_nav_has_alpine_state(self, driver, all_pages):
        for url in all_pages:
            driver.get(url)
            nav = driver.find_element(By.TAG_NAME, "nav")
            has_data = nav.get_attribute("x-data") is not None
            if not has_data:
                inner = nav.find_elements(By.CSS_SELECTOR, "[x-data]")
                has_data = len(inner) >= 1
            assert has_data, (
                "Page {} has a <nav> but no element with `x-data` declaring "
                "the menu state.".format(url)
            )

    def test_hamburger_button_present(self, driver, all_pages):
        for url in all_pages:
            driver.get(url)
            nav = driver.find_element(By.TAG_NAME, "nav")
            buttons = nav.find_elements(By.TAG_NAME, "button")
            ok = False
            for b in buttons:
                cls = b.get_attribute("class") or ""
                click_attr = (
                    b.get_attribute("@click")
                    or b.get_attribute("x-on:click")
                    or ""
                )
                if click_attr and HIDE_AT_MD_RE.search(cls):
                    ok = True
                    break
            assert ok, (
                "Page {} has no hamburger <button> with both an @click "
                "(or x-on:click) attribute and a `md:hidden` (or larger) "
                "class.".format(url)
            )

    def test_link_group_visible_at_md(self, driver, all_pages):
        for url in all_pages:
            driver.get(url)
            nav = driver.find_element(By.TAG_NAME, "nav")
            html = nav.get_attribute("innerHTML") or ""
            assert SHOW_AT_MD_RE.search(html), (
                "Page {} has no element inside <nav> with a class like "
                "`md:flex` / `md:block` / `md:!block` to make the link group "
                "visible at the md breakpoint or larger.".format(url)
            )

    # ------------------------------------------------------------------
    # Requirement 3: responsive layout (at least 3 breakpoint usages)
    # ------------------------------------------------------------------

    def test_responsive_prefixes_used(self, driver, main_url):
        driver.get(main_url)
        elems = driver.find_elements(By.CSS_SELECTOR, "[class]")
        joined = " ".join(e.get_attribute("class") or "" for e in elems)
        hits = RESPONSIVE_PREFIX_RE.findall(joined)
        assert len(hits) >= 3, (
            "The home page must use at least 3 responsive breakpoint "
            "prefixes (sm:/md:/lg:/xl:/2xl:) to change layout between "
            "small and larger screens. Found {} usage(s).".format(len(hits))
        )

    # ------------------------------------------------------------------
    # Requirement 5: customization (arbitrary values or custom CSS)
    # ------------------------------------------------------------------

    def test_three_customizations(self, driver, settings, all_pages):
        """
        Counts arbitrary-value class usages across every page PLUS rules
        in css/custom.css. The student must reach 3 in total.
        """
        arbitrary_count = 0
        for url in all_pages:
            driver.get(url)
            html = driver.page_source
            arbitrary_count += len(ARBITRARY_VALUE_RE.findall(html))

        custom_rule_count = 0
        custom_css_url = _build_url(settings["site_url"], "css/custom.css")
        try:
            with urlopen(custom_css_url, timeout=10) as response:
                if response.status == 200:
                    body = response.read().decode("utf-8", errors="ignore")
                    custom_rule_count = body.count("{")
        except Exception:
            pass

        total = arbitrary_count + custom_rule_count
        assert total >= 3, (
            "Expected at least 3 customizations across the site. Found {} "
            "arbitrary-value Tailwind class(es) and {} CSS rule(s) in "
            "css/custom.css (total: {}). Add more arbitrary-value classes "
            "(e.g. `bg-[#abcdef]`) or write more rules in css/custom.css."
            .format(arbitrary_count, custom_rule_count, total)
        )
