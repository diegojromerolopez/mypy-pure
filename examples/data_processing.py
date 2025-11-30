"""
Data Processing Example

This example demonstrates using @pure for data transformation pipelines.
Pure functions make data processing:
- Easy to test (no mocks needed)
- Easy to parallelize (no shared state)
- Easy to cache (deterministic results)
"""

from mypy_pure import pure


# ✅ Pure data transformations
@pure
def normalize_name(name: str) -> str:
    """Normalize a name to title case."""
    return name.strip().title()


@pure
def calculate_age(birth_year: int, current_year: int) -> int:
    """Calculate age from birth year."""
    return current_year - birth_year


@pure
def filter_active_users(users: list[dict]) -> list[dict]:
    """Filter only active users."""
    return [user for user in users if user.get('active', False)]


@pure
def transform_user_data(raw_data: dict, current_year: int) -> dict:
    """Transform raw user data into normalized format."""
    return {
        'id': raw_data['user_id'],
        'name': normalize_name(raw_data['full_name']),
        'age': calculate_age(raw_data['birth_year'], current_year),
        'email': raw_data['email'].lower(),
    }


@pure
def process_user_batch(users: list[dict], current_year: int) -> list[dict]:
    """Process a batch of users - pure pipeline."""
    active_users = filter_active_users(users)
    return [transform_user_data(user, current_year) for user in active_users]


# Example usage
if __name__ == '__main__':
    raw_users = [
        {
            'user_id': 1,
            'full_name': '  john doe  ',
            'birth_year': 1990,
            'email': 'JOHN@EXAMPLE.COM',
            'active': True,
        },
        {
            'user_id': 2,
            'full_name': 'jane smith',
            'birth_year': 1985,
            'email': 'Jane@Example.com',
            'active': False,
        },
        {
            'user_id': 3,
            'full_name': 'bob wilson',
            'birth_year': 1995,
            'email': 'bob@example.com',
            'active': True,
        },
    ]

    result = process_user_batch(raw_users, 2025)
    print('Processed users:', result)
    # Output: [
    #     {'id': 1, 'name': 'John Doe', 'age': 35, 'email': 'john@example.com'},
    #     {'id': 3, 'name': 'Bob Wilson', 'age': 30, 'email': 'bob@example.com'}
    # ]
