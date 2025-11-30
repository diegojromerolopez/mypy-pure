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
        config = self._get_resource_path('mypy_custom_impure.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is impure because it calls',
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
            'is impure because it calls',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_impure_function_indirectly(self):
        resource = self._get_resource_path('pure_calls_impure_indirect.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is impure because it calls',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_impure_function_deeply_indirect(self):
        resource = self._get_resource_path('pure_calls_impure_deeply_indirect.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is impure because it calls',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_print(self):
        resource = self._get_resource_path('pure_calls_print.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is impure because it calls',
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_sleep(self):
        resource = self._get_resource_path('pure_calls_sleep.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            'is impure because it calls',
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
            "Function 'pure_func' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_function_calls_external_impure(self):
        resource = self._get_resource_path('pure_calls_external_impure.py')
        config = self._get_resource_path('mypy_custom_multiple.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
        self.assertEqual(0, exit_status, f'Mypy failed with exit code {exit_status}. Stdout: {stdout} Stderr: {stderr}')
        self.assertIn(
            "Function 'pure_func' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_instance_method(self):
        resource = self._get_resource_path('pure_instance_method.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_instance_method' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_static_method(self):
        resource = self._get_resource_path('pure_static_method.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_static_method' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_class_method(self):
        resource = self._get_resource_path('pure_class_method.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_class_method' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_async_function(self):
        resource = self._get_resource_path('pure_async_function.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_async_function' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )
        self.assertIn(
            "Function 'impure_async_method' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_property_method(self):
        resource = self._get_resource_path('pure_property_method.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_property' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_nested_function(self):
        resource = self._get_resource_path('pure_nested_function.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
        self.assertEqual(0, exit_status)
        self.assertIn(
            "Function 'impure_nested' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )
        self.assertIn(
            "Function 'outer_calls_impure_nested' is impure because it calls",
            stdout,
            f'Expected purity violation, got: {stdout}',
        )

    def test_pure_uses_custom_pure_function(self):
        """Test that functions in pure_functions config are treated as pure."""
        resource = self._get_resource_path('pure_uses_custom_pure.py')
        config = self._get_resource_path('mypy_custom_pure.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config_file=config)
        # Should succeed - custom_pure_function is whitelisted as pure
        self.assertEqual(
            0,
            exit_status,
            f'Expected success but got errors. stdout: {stdout}, stderr: {stderr}',
        )
        # Should NOT contain purity violation
        self.assertNotIn(
            'is impure because it calls',
            stdout,
            f'Unexpected purity violation: {stdout}',
        )

    def test_pure_uses_external_auto_pure(self):
        """Test that functions in __mypy_pure__ of imported modules are treated as pure."""
        # We need to make sure the external module is importable by the plugin.
        # The plugin runs in the same process as the test (mostly), but importlib needs to find it.
        # Since we are running pytest from root, and resources are in mypy_pure/tests/resources,
        # we might need to add that dir to sys.path or ensure it's a package.
        # It is a package (has __init__.py? No, resources doesn't).

        # Actually, the plugin runs inside mypy, which runs in a separate process usually?
        # No, self.__run_mypy runs mypy as a subprocess or via api.run.
        # If via api.run (which we use in test_plugin.py? let's check), it's in-process.
        # But wait, `api.run` runs mypy. Mypy will load the plugin.
        # The plugin will try to `importlib.import_module('external_module_with_pure')`.
        # This module must be in the python path of the process running the plugin.

        # In our test setup, we might need to set PYTHONPATH.

        resource = self._get_resource_path('pure_uses_external_auto_pure.py')

        # We need to set PYTHONPATH to include the resources directory so the plugin can import the module
        import os

        resources_dir = str(Path(resource).parent)
        env = os.environ.copy()
        env['PYTHONPATH'] = resources_dir + os.pathsep + env.get('PYTHONPATH', '')
        env['MYPYPATH'] = resources_dir + os.pathsep + env.get('MYPYPATH', '')

        # We also need to modify sys.path for the plugin running in-process
        import sys

        sys.path.insert(0, resources_dir)
        try:
            # Pass the environment with MYPYPATH to mypy
            # But self.__run_mypy doesn't accept env argument currently.
            # We need to modify os.environ temporarily or update __run_mypy.
            # Let's modify os.environ temporarily.
            old_mypypath = os.environ.get('MYPYPATH')
            os.environ['MYPYPATH'] = env['MYPYPATH']
            try:
                stdout, stderr, exit_status = self.__run_mypy(resource)
            finally:
                if old_mypypath is None:
                    del os.environ['MYPYPATH']
                else:
                    os.environ['MYPYPATH'] = old_mypypath
        finally:
            sys.path.pop(0)

        self.assertEqual(
            0,
            exit_status,
            f'Expected success but got errors. stdout: {stdout}, stderr: {stderr}',
        )
        self.assertNotIn(
            'is impure because it calls',
            stdout,
            f'Unexpected purity violation: {stdout}',
        )

    def test_pure_uses_dotted_names_in_mypy_pure(self):
        """Test that __mypy_pure__ can contain dotted names (line 65 coverage)."""
        resource = self._get_resource_path('pure_uses_dotted_names.py')

        import os
        import sys

        resources_dir = str(Path(resource).parent)
        sys.path.insert(0, resources_dir)
        try:
            old_mypypath = os.environ.get('MYPYPATH')
            os.environ['MYPYPATH'] = resources_dir + os.pathsep + os.environ.get('MYPYPATH', '')
            try:
                stdout, stderr, exit_status = self.__run_mypy(resource)
            finally:
                if old_mypypath is None:
                    if 'MYPYPATH' in os.environ:
                        del os.environ['MYPYPATH']
                else:
                    os.environ['MYPYPATH'] = old_mypypath
        finally:
            sys.path.pop(0)

        self.assertEqual(
            0,
            exit_status,
            f'Expected success but got errors. stdout: {stdout}, stderr: {stderr}',
        )
        self.assertNotIn(
            'is impure because it calls',
            stdout,
            f'Unexpected purity violation: {stdout}',
        )

    def test_pure_recursive_functions(self):
        """Test that recursive functions work correctly (visited multiple times)."""
        resource = self._get_resource_path('pure_recursive.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)

        # Should succeed - recursive calls to pure functions are OK
        self.assertEqual(
            0,
            exit_status,
            f'Expected success but got errors. stdout: {stdout}, stderr: {stderr}',
        )
        self.assertNotIn(
            'is impure because it calls',
            stdout,
            f'Unexpected purity violation: {stdout}',
        )

    def test_whitelist_priority_over_blacklist(self):
        """Test that whitelist (pure_functions) takes priority over blacklist."""
        resource = self._get_resource_path('pure_whitelist_priority.py')
        config = self._get_resource_path('mypy_whitelist_priority.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)

        # Should succeed - print is whitelisted even though it's blacklisted
        self.assertEqual(
            0,
            exit_status,
            f'Expected success but got errors. stdout: {stdout}, stderr: {stderr}',
        )
        self.assertNotIn(
            'is impure because it calls',
            stdout,
            f'Unexpected purity violation: {stdout}',
        )
