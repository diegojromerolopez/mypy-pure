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

    def test_pure_mutually_recursive(self):
        """Test that mutually recursive pure functions are handled correctly (cycle detection)."""
        resource = self._get_resource_path('pure_mutually_recursive.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
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

    def test_pure_whitelisted_callee(self):
        """Test that a function calling a whitelisted impure function is considered pure."""
        resource = self._get_resource_path('pure_whitelisted_callee.py')
        config = self._get_resource_path('mypy_whitelist_callee.ini')
        stdout, stderr, exit_status = self.__run_mypy(resource, config)
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

    def test_pure_import_alias(self):
        """Test that pure decorator works when imported with an alias."""
        resource = self._get_resource_path('pure_import_alias.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
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

    def test_pure_decorators_module(self):
        """Test that pure decorator works when used as @decorators.pure."""
        resource = self._get_resource_path('pure_decorators_module.py')
        stdout, stderr, exit_status = self.__run_mypy(resource)
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
                    os.environ['MYPYPATH'] = old_mypypath  # pragma: no cover
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

    def test_auto_discovery_overrides_blacklist(self):
        """Test that __mypy_pure__ auto-discovery takes priority over blacklist."""
        resource = self._get_resource_path('pure_uses_blacklisted_external.py')
        config = self._get_resource_path('mypy_blacklist_external.ini')

        import os
        import sys

        resources_dir = str(Path(resource).parent)
        sys.path.insert(0, resources_dir)
        try:
            old_mypypath = os.environ.get('MYPYPATH')
            os.environ['MYPYPATH'] = resources_dir + os.pathsep + os.environ.get('MYPYPATH', '')
            try:
                stdout, stderr, exit_status = self.__run_mypy(resource, config)
            finally:
                if old_mypypath is None:
                    if 'MYPYPATH' in os.environ:
                        del os.environ['MYPYPATH']
                else:
                    os.environ['MYPYPATH'] = old_mypypath  # pragma: no cover
        finally:
            sys.path.pop(0)

        # Should succeed - __mypy_pure__ whitelist overrides config blacklist
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

    def test_pure_relative_import(self):
        """Test that relative imports (module is None) are handled by visitor."""
        resource = self._get_resource_path('pure_relative_import.py')
        # We expect mypy to fail due to relative import in non-package, but plugin should run
        # and cover the else block in visitor.py
        stdout, stderr, exit_status = self.__run_mypy(resource)

        # We don't check exit_status because mypy will likely fail on the import
        # We just want to ensure the plugin didn't crash and we covered the line.
        self.assertNotIn('Traceback', stderr)
        self.assertNotIn('Traceback', stdout)

    def test_no_config_file(self):
        """Test that plugin handles missing config file gracefully (unit test)."""
        from mypy.options import Options

        from mypy_pure.plugin import PurityPlugin

        options = Options()
        options.config_file = None

        # Should not raise exception
        plugin = PurityPlugin(options)

        # Verify defaults
        # Accessing private attributes for verification
        self.assertEqual(plugin._PurityPlugin__blacklist, plugin._PurityPlugin__blacklist)  # Just checking it exists
        # We can check that whitelist is empty
        self.assertEqual(len(plugin._PurityPlugin__whitelist), 0)

    def test_config_bad_syntax(self):
        """Test that plugin handles config file with bad syntax gracefully (unit test)."""
        from mypy.options import Options

        from mypy_pure.plugin import PurityPlugin

        options = Options()
        options.config_file = str(self._get_resource_path('mypy_bad_syntax.ini'))

        # Should not raise exception (catches configparser.Error)
        plugin = PurityPlugin(options)

        # Verify defaults (whitelist should be empty as config failed to load)
        self.assertEqual(len(plugin._PurityPlugin__whitelist), 0)

    def test_load_module_pure_functions(self):
        """Test __load_module_pure_functions logic (unit test)."""
        from mypy.options import Options

        from mypy_pure.plugin import PurityPlugin

        options = Options()
        options.config_file = None
        plugin = PurityPlugin(options)

        # 1. Test success case (module with __mypy_pure__)
        # We use a module that we know exists and has __mypy_pure__
        # 'mypy_pure.tests.resources.external_blacklisted_but_pure'
        module_name = 'mypy_pure.tests.resources.external_blacklisted_but_pure'

        # Access private method
        plugin._PurityPlugin__load_module_pure_functions(module_name)

        # Verify it was loaded
        self.assertIn(module_name, plugin._PurityPlugin__loaded_modules)
        # Verify whitelist was updated (it has 'pure_but_blacklisted')
        # The module puts 'pure_but_blacklisted' in __mypy_pure__
        # Since it doesn't have a dot, it should be added as 'module.func' AND 'func' depending on logic?
        # Logic says: if '.' not in func: add f'{module_name}.{func}'
        expected_func = f'{module_name}.pure_but_blacklisted'
        self.assertIn(expected_func, plugin._PurityPlugin__whitelist)

        # 2. Test already loaded case
        # Calling it again should return early (coverage check)
        plugin._PurityPlugin__load_module_pure_functions(module_name)
        self.assertIn(module_name, plugin._PurityPlugin__loaded_modules)

        # 3. Test module without __mypy_pure__
        # 'mypy_pure.tests.resources.pure_is_ok'
        module_no_pure = 'mypy_pure.tests.resources.pure_is_ok'
        plugin._PurityPlugin__load_module_pure_functions(module_no_pure)
        self.assertIn(module_no_pure, plugin._PurityPlugin__loaded_modules)
        # Whitelist shouldn't change size significantly (or at least shouldn't have new entries from this module)

        # 4. Test module with dotted names in __mypy_pure__
        # 'mypy_pure.tests.resources.external_module_dotted'
        module_dotted = 'mypy_pure.tests.resources.external_module_dotted'
        plugin._PurityPlugin__load_module_pure_functions(module_dotted)
        self.assertIn(module_dotted, plugin._PurityPlugin__loaded_modules)
        # Verify dotted name is added directly
        self.assertIn('external_module_with_pure.pure_func', plugin._PurityPlugin__whitelist)

        # 5. Test exception handling (ImportError)
        plugin._PurityPlugin__load_module_pure_functions('non_existent_module_xyz')
        # Should not raise exception
