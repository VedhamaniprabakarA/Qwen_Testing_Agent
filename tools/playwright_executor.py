import os
import subprocess
import sys
import tempfile
from datetime import datetime


class PlaywrightExecutor:

    def __init__(
        self,
        timeout=120
    ):

        self.timeout = timeout

    # ======================================================
    # EXECUTE GENERATED PLAYWRIGHT CODE
    # ======================================================

    def execute(
        self,
        code
    ):

        if not code:

            return {
                "success": False,
                "status": "FAILED",
                "stdout": "",
                "stderr": "Generated Playwright code is empty.",
                "return_code": -1
            }

        # --------------------------------------------------
        # Clean markdown
        # --------------------------------------------------

        code = self.clean_code(
            code
        )

        # --------------------------------------------------
        # Create temporary Python file
        # --------------------------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"generated_test_{timestamp}.py"
        )

        temp_dir = os.path.join(
            "data",
            "generated_scripts"
        )

        os.makedirs(
            temp_dir,
            exist_ok=True
        )

        script_path = os.path.join(
            temp_dir,
            filename
        )

        # --------------------------------------------------
        # Save generated script
        # --------------------------------------------------

        with open(
            script_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                code
            )

        print(
            "\nGenerated script saved:"
        )

        print(
            script_path
        )

        # --------------------------------------------------
        # Execute Python script
        # --------------------------------------------------

        print(
            "\nStarting Playwright automation..."
        )

        print(
            "-" * 60
        )

        try:

            process = subprocess.run(
                [
                    sys.executable,
                    script_path
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            stdout = process.stdout
            stderr = process.stderr

            # --------------------------------------------------
            # SUCCESS
            # --------------------------------------------------

            if process.returncode == 0:

                return {
                    "success": True,
                    "status": "PASSED",
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": process.returncode,
                    "script_path": script_path
                }

            # --------------------------------------------------
            # FAILURE
            # --------------------------------------------------

            return {
                "success": False,
                "status": "FAILED",
                "stdout": stdout,
                "stderr": stderr,
                "return_code": process.returncode,
                "script_path": script_path
            }

        except subprocess.TimeoutExpired as e:

            return {
                "success": False,
                "status": "TIMEOUT",
                "stdout": (
                    e.stdout
                    if e.stdout
                    else ""
                ),
                "stderr": (
                    e.stderr
                    if e.stderr
                    else ""
                ),
                "return_code": -1,
                "script_path": script_path
            }

        except Exception as e:

            return {
                "success": False,
                "status": "FAILED",
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
                "script_path": script_path
            }

    # ======================================================
    # CLEAN GENERATED CODE
    # ======================================================

    def clean_code(
        self,
        code
    ):

        code = code.strip()

        if "```python" in code:

            code = code.replace(
                "```python",
                ""
            )

        if "```" in code:

            code = code.replace(
                "```",
                ""
            )

        return code.strip()