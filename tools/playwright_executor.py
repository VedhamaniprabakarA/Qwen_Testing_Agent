import subprocess
import sys
import tempfile
import os


class PlaywrightExecutor:

    def execute(self, code):

        temp_file = None

        try:

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8"
            ) as file:

                file.write(code)
                temp_file = file.name

            print("\nExecuting Playwright script...")
            print("-" * 60)

            process = subprocess.run(
                [
                    sys.executable,
                    temp_file
                ],
                capture_output=True,
                text=True,
                timeout=300
            )

            result = {
                "return_code": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "status": (
                    "PASSED"
                    if process.returncode == 0
                    else "FAILED"
                )
            }

            return result

        except subprocess.TimeoutExpired:

            return {
                "status": "TIMEOUT",
                "stdout": "",
                "stderr": "Playwright execution timed out."
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": str(e)
            }

        finally:

            if temp_file and os.path.exists(temp_file):

                try:
                    os.remove(temp_file)
                except Exception:
                    pass