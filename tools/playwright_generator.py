class PlaywrightGenerator:

    def generate(
        self,
        url,
        page_data,
        test_cases
    ):

        elements = page_data.get(
            "elements",
            []
        )

        locator_information = []

        for element in elements:

            locator_information.append(
                {
                    "tag": element.get("tag"),
                    "id": element.get("id"),
                    "name": element.get("name"),
                    "placeholder": element.get("placeholder"),
                    "aria_label": element.get("aria_label"),
                    "text": element.get("text"),
                    "selector": element.get("selector"),
                    "xpath": element.get("xpath")
                }
            )

        code = f'''
from playwright.sync_api import sync_playwright


def test_generated():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={{
                "width": 1440,
                "height": 900
            }}
        )

        page.goto(
            "{url}",
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(2000)

'''

        for case in test_cases:

            code += f'''
        # ------------------------------------------------
        # {case}
        # ------------------------------------------------

'''

        code += '''
        browser.close()


if __name__ == "__main__":
    test_generated()
'''

        return code