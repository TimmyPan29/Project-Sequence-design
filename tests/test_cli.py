import io
import unittest
from contextlib import redirect_stdout

from sequence_design.cli import main


class CliTests(unittest.TestCase):
    def test_acf_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(("acf", "++-"))
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "3 0 -1")

    def test_zcp_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(("zcp", "++", "+-"))
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "2")


if __name__ == "__main__":
    unittest.main()

