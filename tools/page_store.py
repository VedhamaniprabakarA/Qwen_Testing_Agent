import copy
import hashlib
import json
import os
from datetime import datetime


class PageStore:

    def __init__(
        self,
        storage_dir="data/page_snapshots"
    ):

        self.storage_dir = storage_dir

        os.makedirs(
            self.storage_dir,
            exist_ok=True
        )

    # ======================================================
    # CREATE UNIQUE FILE NAME
    # ======================================================

    def create_filename(
        self,
        url
    ):

        url_hash = hashlib.sha256(
            url.encode("utf-8")
        ).hexdigest()[:16]

        return (
            f"page_{url_hash}.json"
        )

    # ======================================================
    # SAVE PAGE
    # ======================================================

    def save(
        self,
        page_data
    ):

        url = page_data.get(
            "url",
            ""
        )

        if not url:

            raise ValueError(
                "Cannot store page without URL."
            )

        filename = (
            self.create_filename(
                url
            )
        )

        filepath = os.path.join(
            self.storage_dir,
            filename
        )

        # Make a copy so the original
        # page_data is not modified.

        clean_data = copy.deepcopy(
            page_data
        )

        # Remove sensitive values.

        clean_data = (
            self.remove_sensitive_data(
                clean_data
            )
        )

        clean_data["stored_at"] = (
            datetime.now().isoformat()
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                clean_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            "\nPage specification stored:"
        )

        print(
            filepath
        )

        return filepath

    # ======================================================
    # LOAD PAGE
    # ======================================================

    def load(
        self,
        url
    ):

        if not url:

            return None

        filename = (
            self.create_filename(
                url
            )
        )

        filepath = os.path.join(
            self.storage_dir,
            filename
        )

        if not os.path.exists(
            filepath
        ):

            return None

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(
                    file
                )

        except Exception as e:

            print(
                "\nUnable to load "
                "page snapshot:"
            )

            print(
                str(e)
            )

            return None

    # ======================================================
    # REMOVE SENSITIVE DATA
    # ======================================================

    def remove_sensitive_data(
        self,
        page_data
    ):

        elements = page_data.get(
            "elements",
            []
        )

        for element in elements:

            # --------------------------------------------------
            # Never store input values
            # --------------------------------------------------

            if "value" in element:

                element["value"] = None

            # --------------------------------------------------
            # Hidden input
            # --------------------------------------------------

            if (
                element.get("type")
                == "hidden"
            ):

                element["outer_html"] = ""

                element["value"] = None

        return page_data