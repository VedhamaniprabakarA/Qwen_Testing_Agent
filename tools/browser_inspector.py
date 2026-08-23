from playwright.sync_api import sync_playwright


class BrowserInspector:

    def __init__(self, headless=False):

        self.headless = headless

    # ==========================================================
    # MAIN INSPECTION METHOD
    # ==========================================================

    def inspect(self, url):

        result = {
            "url": url,
            "title": "",
            "page_text": "",
            "elements": [],
            "error": None
        }

        with sync_playwright() as p:

            browser = None

            try:

                # --------------------------------------------------
                # Launch Chromium
                # --------------------------------------------------

                browser = p.chromium.launch(
                    headless=self.headless
                )

                context = browser.new_context(
                    viewport={
                        "width": 1440,
                        "height": 900
                    }
                )

                page = context.new_page()

                print("\nOpening browser...")
                print(f"URL: {url}")

                # --------------------------------------------------
                # Navigate
                # --------------------------------------------------

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                # Give JavaScript time to render
                page.wait_for_timeout(3000)

                # --------------------------------------------------
                # Page information
                # --------------------------------------------------

                result["url"] = page.url

                result["title"] = page.title()

                # --------------------------------------------------
                # Page visible text
                # --------------------------------------------------

                try:

                    result["page_text"] = (
                        page.locator("body")
                        .inner_text(
                            timeout=5000
                        )
                        .strip()
                    )

                except Exception:

                    result["page_text"] = ""

                # --------------------------------------------------
                # Discover all relevant elements
                # --------------------------------------------------

                self._inspect_inputs(
                    page,
                    result
                )

                self._inspect_buttons(
                    page,
                    result
                )

                self._inspect_links(
                    page,
                    result
                )

                self._inspect_textareas(
                    page,
                    result
                )

                self._inspect_selects(
                    page,
                    result
                )

                self._inspect_checkboxes(
                    page,
                    result
                )

                self._inspect_radios(
                    page,
                    result
                )

                # --------------------------------------------------
                # Inspect forms
                # --------------------------------------------------

                self._inspect_forms(
                    page,
                    result
                )

                # --------------------------------------------------
                # Screenshot
                # --------------------------------------------------

                page.screenshot(
                    path="page_inspection.png",
                    full_page=True
                )

                print(
                    f"\nFound "
                    f"{len(result['elements'])} "
                    f"elements."
                )

                print(
                    "\nScreenshot saved as:"
                    "\npage_inspection.png"
                )

            except Exception as e:

                result["error"] = str(e)

                print(
                    "\nBrowser inspection error:"
                )

                print(e)

            finally:

                if browser:

                    browser.close()

        return result

    # ==========================================================
    # INPUTS
    # ==========================================================

    def _inspect_inputs(
        self,
        page,
        result
    ):

        elements = page.locator(
            "input"
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "input",
                i + 1
            )

            # --------------------------------------------------
            # Keep hidden inputs for technical information,
            # but mark them clearly.
            # --------------------------------------------------

            result["elements"].append(
                data
            )

    # ==========================================================
    # BUTTONS
    # ==========================================================

    def _inspect_buttons(
        self,
        page,
        result
    ):

        elements = page.locator(
            "button"
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "button",
                i + 1
            )

            result["elements"].append(
                data
            )

    # ==========================================================
    # LINKS
    # ==========================================================

    def _inspect_links(
        self,
        page,
        result
    ):

        elements = page.locator(
            "a"
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "a",
                i + 1
            )

            result["elements"].append(
                data
            )

    # ==========================================================
    # TEXTAREA
    # ==========================================================

    def _inspect_textareas(
        self,
        page,
        result
    ):

        elements = page.locator(
            "textarea"
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "textarea",
                i + 1
            )

            result["elements"].append(
                data
            )

    # ==========================================================
    # SELECT
    # ==========================================================

    def _inspect_selects(
        self,
        page,
        result
    ):

        elements = page.locator(
            "select"
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "select",
                i + 1
            )

            # --------------------------------------------------
            # Capture options
            # --------------------------------------------------

            try:

                options = element.locator(
                    "option"
                )

                option_values = []

                for j in range(
                    options.count()
                ):

                    option = options.nth(j)

                    option_values.append(
                        {
                            "text": (
                                option.inner_text()
                                .strip()
                            ),
                            "value": (
                                option.get_attribute(
                                    "value"
                                )
                            )
                        }
                    )

                data["options"] = (
                    option_values
                )

            except Exception:

                data["options"] = []

            result["elements"].append(
                data
            )

    # ==========================================================
    # CHECKBOXES
    # ==========================================================

    def _inspect_checkboxes(
        self,
        page,
        result
    ):

        elements = page.locator(
            'input[type="checkbox"]'
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "checkbox",
                i + 1
            )

            result["elements"].append(
                data
            )

    # ==========================================================
    # RADIO BUTTONS
    # ==========================================================

    def _inspect_radios(
        self,
        page,
        result
    ):

        elements = page.locator(
            'input[type="radio"]'
        )

        count = elements.count()

        for i in range(count):

            element = elements.nth(i)

            data = self.extract_element(
                element,
                "radio",
                i + 1
            )

            result["elements"].append(
                data
            )

    # ==========================================================
    # FORMS
    # ==========================================================

    def _inspect_forms(
        self,
        page,
        result
    ):

        forms = page.locator(
            "form"
        )

        form_count = forms.count()

        for i in range(form_count):

            form = forms.nth(i)

            try:

                form_data = {
                    "tag": "form",
                    "index": i + 1,
                    "action": (
                        form.get_attribute(
                            "action"
                        )
                    ),
                    "method": (
                        form.get_attribute(
                            "method"
                        )
                    ),
                    "id": (
                        form.get_attribute(
                            "id"
                        )
                    ),
                    "name": (
                        form.get_attribute(
                            "name"
                        )
                    )
                }

                result["elements"].append(
                    form_data
                )

            except Exception:

                pass

    # ==========================================================
    # EXTRACT ELEMENT INFORMATION
    # ==========================================================

    def extract_element(
        self,
        element,
        tag,
        index
    ):

        data = {

            "index": index,

            "tag": tag,

            "id": element.get_attribute(
                "id"
            ),

            "name": element.get_attribute(
                "name"
            ),

            "type": element.get_attribute(
                "type"
            ),

            "placeholder": element.get_attribute(
                "placeholder"
            ),

            "aria_label": element.get_attribute(
                "aria-label"
            ),

            "role": element.get_attribute(
                "role"
            ),

            "class": element.get_attribute(
                "class"
            ),

            "href": element.get_attribute(
                "href"
            ),

            "title": element.get_attribute(
                "title"
            ),

            "value": (
                None
                if element.get_attribute("type") == "hidden"
                else element.get_attribute("value")
            ),

            "text": "",

            "visible": False,

            "enabled": False,

            "checked": False,

            "css_selector": "",

            "xpath": "",

            "playwright_locator": "",

            "outer_html": ""
        }

        # ======================================================
        # TEXT
        # ======================================================

        try:

            data["text"] = (
                element.inner_text(
                    timeout=1000
                )
                .strip()
            )

        except Exception:

            pass

        # ======================================================
        # VISIBLE
        # ======================================================

        try:

            data["visible"] = (
                element.is_visible()
            )

        except Exception:

            pass

        # ======================================================
        # ENABLED
        # ======================================================

        try:

            data["enabled"] = (
                element.is_enabled()
            )

        except Exception:

            pass

        # ======================================================
        # CHECKED
        # ======================================================

        try:

            if tag in [
                "checkbox",
                "radio"
            ]:

                data["checked"] = (
                    element.is_checked()
                )

        except Exception:

            pass

        # ======================================================
        # OUTER HTML
        # ======================================================

        try:

            data["outer_html"] = (
                element.evaluate(
                    "(el) => el.outerHTML"
                )
            )

        except Exception:

            pass

        # ======================================================
        # CSS SELECTOR
        # ======================================================

        data["css_selector"] = (
            self.create_css_selector(
                data
            )
        )

        # ======================================================
        # XPATH
        # ======================================================

        data["xpath"] = (
            self.create_xpath(
                data
            )
        )

        # ======================================================
        # PLAYWRIGHT LOCATOR
        # ======================================================

        data["playwright_locator"] = (
            self.create_playwright_locator(
                data
            )
        )

        return data

    # ==========================================================
    # CSS SELECTOR
    # ==========================================================

    def create_css_selector(
        self,
        data
    ):

        tag = data.get(
            "tag",
            ""
        )

        # --------------------------------------------------
        # ID
        # --------------------------------------------------

        element_id = data.get(
            "id"
        )

        if element_id:

            return (
                f'#{element_id}'
            )

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        name = data.get(
            "name"
        )

        if name:

            return (
                f'{tag}'
                f'[name="{name}"]'
            )

        # --------------------------------------------------
        # PLACEHOLDER
        # --------------------------------------------------

        placeholder = data.get(
            "placeholder"
        )

        if placeholder:

            return (
                f'{tag}'
                f'[placeholder="{placeholder}"]'
            )

        # --------------------------------------------------
        # ARIA LABEL
        # --------------------------------------------------

        aria_label = data.get(
            "aria_label"
        )

        if aria_label:

            return (
                f'{tag}'
                f'[aria-label="{aria_label}"]'
            )

        # --------------------------------------------------
        # TYPE
        # --------------------------------------------------

        element_type = data.get(
            "type"
        )

        if element_type:

            if tag in [
                "input",
                "checkbox",
                "radio"
            ]:

                actual_tag = "input"

                return (
                    f'{actual_tag}'
                    f'[type="{element_type}"]'
                )

        # --------------------------------------------------
        # HREF
        # --------------------------------------------------

        href = data.get(
            "href"
        )

        if href:

            return (
                f'a[href="{href}"]'
            )

        # --------------------------------------------------
        # CLASS
        # --------------------------------------------------

        class_name = data.get(
            "class"
        )

        if class_name:

            classes = (
                class_name.split()
            )

            # Only use first two classes
            # to avoid extremely fragile selectors.

            if classes:

                return (
                    tag +
                    "".join(
                        f".{cls}"
                        for cls in classes[:2]
                    )
                )

        # --------------------------------------------------
        # FALLBACK
        # --------------------------------------------------

        return tag

    # ==========================================================
    # XPATH
    # ==========================================================

    def create_xpath(
        self,
        data
    ):

        tag = data.get(
            "tag",
            ""
        )

        # --------------------------------------------------
        # ID
        # --------------------------------------------------

        element_id = data.get(
            "id"
        )

        if element_id:

            return (
                f'//*[@id="{element_id}"]'
            )

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        name = data.get(
            "name"
        )

        if name:

            return (
                f'//{tag}'
                f'[@name="{name}"]'
            )

        # --------------------------------------------------
        # PLACEHOLDER
        # --------------------------------------------------

        placeholder = data.get(
            "placeholder"
        )

        if placeholder:

            return (
                f'//{tag}'
                f'[@placeholder="{placeholder}"]'
            )

        # --------------------------------------------------
        # ARIA LABEL
        # --------------------------------------------------

        aria_label = data.get(
            "aria_label"
        )

        if aria_label:

            return (
                f'//{tag}'
                f'[@aria-label="{aria_label}"]'
            )

        # --------------------------------------------------
        # HREF
        # --------------------------------------------------

        href = data.get(
            "href"
        )

        if href:

            return (
                f'//a[@href="{href}"]'
            )

        # --------------------------------------------------
        # TEXT
        # --------------------------------------------------

        text = data.get(
            "text"
        )

        if text:

            text = (
                text
                .replace(
                    '"',
                    "'"
                )
                .strip()
            )

            if text:

                return (
                    f'//{tag}'
                    f'[normalize-space()="{text}"]'
                )

        # --------------------------------------------------
        # FALLBACK
        # --------------------------------------------------

        return (
            f'//{tag}'
        )

    # ==========================================================
    # PLAYWRIGHT LOCATOR
    # ==========================================================

    def create_playwright_locator(
        self,
        data
    ):

        tag = data.get(
            "tag"
        )

        # --------------------------------------------------
        # BUTTON
        # --------------------------------------------------

        if tag == "button":

            text = data.get(
                "text"
            )

            if text:

                escaped_text = (
                    text
                    .replace(
                        '"',
                        '\\"'
                    )
                )

                return (
                    "page.get_by_role("
                    f'"button", '
                    f'name="{escaped_text}"'
                    ")"
                )

        # --------------------------------------------------
        # LINK
        # --------------------------------------------------

        if tag == "a":

            text = data.get(
                "text"
            )

            if text:

                escaped_text = (
                    text
                    .replace(
                        '"',
                        '\\"'
                    )
                )

                return (
                    "page.get_by_role("
                    f'"link", '
                    f'name="{escaped_text}"'
                    ")"
                )

        # --------------------------------------------------
        # INPUT WITH PLACEHOLDER
        # --------------------------------------------------

        placeholder = data.get(
            "placeholder"
        )

        if placeholder:

            escaped_placeholder = (
                placeholder
                .replace(
                    '"',
                    '\\"'
                )
            )

            return (
                "page.get_by_placeholder("
                f'"{escaped_placeholder}"'
                ")"
            )

        # --------------------------------------------------
        # ARIA LABEL
        # --------------------------------------------------

        aria_label = data.get(
            "aria_label"
        )

        if aria_label:

            escaped_label = (
                aria_label
                .replace(
                    '"',
                    '\\"'
                )
            )

            return (
                "page.get_by_label("
                f'"{escaped_label}"'
                ")"
            )

        # --------------------------------------------------
        # ID
        # --------------------------------------------------

        element_id = data.get(
            "id"
        )

        if element_id:

            return (
                f'page.locator('
                f'"#{element_id}"'
                f')'
            )

        # --------------------------------------------------
        # NAME
        # --------------------------------------------------

        name = data.get(
            "name"
        )

        if name:

            return (
                f'page.locator('
                f'"[name=\\"{name}\\"]"'
                f')'
            )

        # --------------------------------------------------
        # CSS FALLBACK
        # --------------------------------------------------

        css = data.get(
            "css_selector"
        )

        if css:

            escaped_css = (
                css
                .replace(
                    '"',
                    '\\"'
                )
            )

            return (
                "page.locator("
                f'"{escaped_css}"'
                ")"
            )

        return ""