"""
Configuration Processing Example

This example demonstrates using @pure for configuration merging and validation.
Pure config processing:
- No file I/O in the pure functions
- Easy to test with different config combinations
- Deterministic behavior
"""

from mypy_pure import pure


# ✅ Pure configuration processing
@pure
def merge_configs(default: dict, user: dict) -> dict:
    """Merge user config into default config."""
    result = default.copy()
    result.update(user)
    return result


@pure
def validate_config(config: dict) -> list[str]:
    """Validate configuration and return list of errors."""
    errors = []

    # Check required fields
    required_fields = ['host', 'port', 'database']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: '{field}'")

    # Validate port
    if 'port' in config:
        port = config['port']
        if not isinstance(port, int) or port < 1 or port > 65535:
            errors.append(f"Invalid port: {port}. Must be between 1 and 65535")

    # Validate timeout
    if 'timeout' in config:
        timeout = config['timeout']
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            errors.append(f"Invalid timeout: {timeout}. Must be positive number")

    # Validate max_connections
    if 'max_connections' in config:
        max_conn = config['max_connections']
        if not isinstance(max_conn, int) or max_conn < 1:
            errors.append(f"Invalid max_connections: {max_conn}. Must be positive integer")

    return errors


@pure
def normalize_config(config: dict) -> dict:
    """Normalize configuration values."""
    normalized = config.copy()

    # Ensure host is lowercase
    if 'host' in normalized:
        normalized['host'] = normalized['host'].lower()

    # Ensure database name is lowercase
    if 'database' in normalized:
        normalized['database'] = normalized['database'].lower()

    # Convert string port to int if needed
    if 'port' in normalized and isinstance(normalized['port'], str):
        try:
            normalized['port'] = int(normalized['port'])
        except ValueError:
            pass  # Leave as is, will be caught by validation

    return normalized


@pure
def apply_environment_overrides(config: dict, environment: str) -> dict:
    """Apply environment-specific overrides."""
    env_configs = {
        'development': {'debug': True, 'log_level': 'DEBUG'},
        'staging': {'debug': False, 'log_level': 'INFO'},
        'production': {'debug': False, 'log_level': 'WARNING', 'ssl': True},
    }

    overrides = env_configs.get(environment, {})
    return merge_configs(config, overrides)


@pure
def process_config(default: dict, user: dict, environment: str) -> dict:
    """Complete config processing pipeline."""
    # Merge configs
    config = merge_configs(default, user)

    # Normalize values
    config = normalize_config(config)

    # Apply environment overrides
    config = apply_environment_overrides(config, environment)

    # Validate (raises if invalid)
    errors = validate_config(config)
    if errors:
        raise ValueError(f"Invalid configuration: {', '.join(errors)}")

    return config


# Example usage
if __name__ == '__main__':
    default_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'myapp',
        'timeout': 30,
        'max_connections': 10,
        'ssl': False,
        'debug': False,
    }

    user_config = {
        'host': 'DB.EXAMPLE.COM',  # Will be normalized to lowercase
        'port': '5433',  # Will be converted to int
        'database': 'PRODUCTION_DB',  # Will be normalized to lowercase
    }

    try:
        final_config = process_config(default_config, user_config, 'production')
        print('Final configuration:')
        for key, value in sorted(final_config.items()):
            print(f'  {key}: {value}')
    except ValueError as e:
        print(f'Configuration error: {e}')
