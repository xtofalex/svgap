import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from scripts.run_generation_pilot import generate


ECHO = f'{sys.executable} -c "import sys; sys.stdout.write(sys.stdin.read())"'
FAIL = f'{sys.executable} -c "import sys; sys.exit(3)"'
EMPTY = f'{sys.executable} -c "pass"'


class CommandProviderTests(TestCase):
    def test_command_receives_prompt_on_stdin_and_returns_stdout(self) -> None:
        with TemporaryDirectory() as sandbox:
            response, command = generate(
                "command", None, "module m; endmodule", Path(sandbox), ECHO
            )
        self.assertEqual(response, "module m; endmodule")
        self.assertEqual(command, [ECHO])

    def test_failing_command_raises(self) -> None:
        with TemporaryDirectory() as sandbox:
            with self.assertRaises(subprocess.SubprocessError):
                generate("command", None, "prompt", Path(sandbox), FAIL)

    def test_empty_stdout_raises(self) -> None:
        with TemporaryDirectory() as sandbox:
            with self.assertRaises(subprocess.SubprocessError):
                generate("command", None, "prompt", Path(sandbox), EMPTY)

    def test_command_provider_requires_command(self) -> None:
        with TemporaryDirectory() as sandbox:
            with self.assertRaises(OSError):
                generate("command", None, "prompt", Path(sandbox), None)
