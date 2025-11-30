"""
Business Logic Example

This example demonstrates using @pure for business rules and calculations.
Pure business logic is:
- Deterministic and testable
- Easy to reason about
- Safe to refactor
- Can be cached/memoized
"""

from mypy_pure import pure


# ✅ Pure business calculations
@pure
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError('Discount must be between 0 and 100')
    return price * (1 - discount_percent / 100)


@pure
def calculate_tax(amount: float, tax_rate: float) -> float:
    """Calculate tax amount."""
    return amount * tax_rate


@pure
def calculate_shipping_cost(weight_kg: float, distance_km: float, is_express: bool) -> float:
    """Calculate shipping cost based on weight, distance, and delivery speed."""
    base_cost = weight_kg * 0.5 + distance_km * 0.1
    if is_express:
        return base_cost * 1.5
    return base_cost


@pure
def apply_loyalty_discount(subtotal: float, loyalty_points: int) -> tuple[float, int]:
    """Apply loyalty points as discount. Returns (new_subtotal, points_used)."""
    max_discount = subtotal * 0.2  # Max 20% discount
    points_value = loyalty_points * 0.01  # 1 point = $0.01

    discount = min(points_value, max_discount)
    points_used = int(discount / 0.01)

    return subtotal - discount, points_used


@pure
def calculate_order_total(
    items: list[dict],
    tax_rate: float,
    shipping_weight_kg: float,
    shipping_distance_km: float,
    is_express: bool,
    loyalty_points: int,
) -> dict:
    """Calculate complete order total with all fees and discounts."""
    # Calculate subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in items)

    # Apply item-level discounts
    for item in items:
        if 'discount_percent' in item:
            item_discount = calculate_discount(item['price'] * item['quantity'], item['discount_percent'])
            subtotal -= item['price'] * item['quantity'] - item_discount

    # Apply loyalty discount
    subtotal_after_loyalty, points_used = apply_loyalty_discount(subtotal, loyalty_points)

    # Calculate shipping
    shipping = calculate_shipping_cost(shipping_weight_kg, shipping_distance_km, is_express)

    # Calculate tax (after discounts, before shipping)
    tax = calculate_tax(subtotal_after_loyalty, tax_rate)

    # Calculate total
    total = subtotal_after_loyalty + shipping + tax

    return {
        'subtotal': round(subtotal, 2),
        'loyalty_discount': round(subtotal - subtotal_after_loyalty, 2),
        'points_used': points_used,
        'shipping': round(shipping, 2),
        'tax': round(tax, 2),
        'total': round(total, 2),
    }


# Example usage
if __name__ == '__main__':
    order_items = [
        {'name': 'Widget', 'price': 29.99, 'quantity': 2},
        {'name': 'Gadget', 'price': 49.99, 'quantity': 1, 'discount_percent': 10},
    ]

    result = calculate_order_total(
        items=order_items,
        tax_rate=0.08,  # 8% tax
        shipping_weight_kg=2.5,
        shipping_distance_km=100,
        is_express=True,
        loyalty_points=500,  # $5 worth of points
    )

    print('Order breakdown:')
    for key, value in result.items():
        print(f'  {key}: ${value}')
