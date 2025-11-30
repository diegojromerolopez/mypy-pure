from __future__ import annotations

from pathlib import Path
from unittest import TestCase


class TestPlugin(TestCase):
    def __run_mypy(self, file_path: Path, config_file: Path | None = None) -> tuple[str, str, int]:
        tests_path = Path(__file__).resolve().parent
        if config_file is None:
            config_file = tests_path / 'resources' / 'mypy.ini'

        import sys
        from io import StringIO

        from mypy.api import run as mypy_api_run

        capture = StringIO()
        old_stdout = sys.stdout
        sys.stdout = capture
        try:
            stdout, stderr, exit_status = mypy_api_run(
                [
                    '--config-file',
                    str(config_file),
                    '--no-error-summary',
                    '--hide-error-context',
                    '--follow-imports=silent',
                    '--strict',
                    '--no-incremental',
                    str(file_path),
                ]
            )
            # Combine captured stdout with mypy's returned stdout
            combined_stdout = stdout + capture.getvalue()
            return combined_stdout, stderr, exit_status
        finally:
            sys.stdout = old_stdout

    def _get_resource_path(self, filename: str) -> Path:
        return Path(__file__).resolve().parent / 'resources' / filename

    def test_pure_function_calls_custom_impure(self):
        resource = self._get_resource_path('pure_calls_custom_impure.py')
        config = self._get_resource_path('mypy_custom.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_simple_pure_function(self):
        resource = self._get_resource_path('pure_is_ok.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertEqual(stdout.strip(), '', f'Unexpected mypy output: {stdout}')

    def test_pure_function_calls_impure_stdlib(self):
        resource = self._get_resource_path('pure_calls_impure_stdlib.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_impure_function_indirectly(self):
        resource = self._get_resource_path('pure_calls_impure_indirect.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_impure_function_deeply_indirect(self):
        resource = self._get_resource_path('pure_calls_impure_deeply_indirect.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_print(self):
        resource = self._get_resource_path('pure_calls_print.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_sleep(self):
        resource = self._get_resource_path('pure_calls_sleep.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is annotated as pure but calls impure functions',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_pure_function(self):
        resource = self._get_resource_path('pure_calls_pure.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertEqual(stdout.strip(), '', f'Unexpected mypy output: {stdout}')

    def test_pure_function_calls_multiple_custom_impure(self):
        resource = self._get_resource_path('pure_calls_multiple_impure.py')
        config = self._get_resource_path('mypy_custom_multiple.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
        self.assertEqual(0, exit_status, f'Mypy failed with exit code {exit_status}. Stdout: {stdout} Stderr: {stderr}')
        self.assertIn(
            "Function 'pure_func' is annotated as pure but calls impure functions",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_external_impure(self):
        resource = self._get_resource_path('pure_calls_external_impure.py')
        config = self._get_resource_path('mypy_custom_multiple.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
        self.assertEqual(0, exit_status, f'Mypy failed with exit code {exit_status}. Stdout: {stdout} Stderr: {stderr}')
        self.assertIn(
            "Function 'pure_func' is annotated as pure but calls impure functions",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )
