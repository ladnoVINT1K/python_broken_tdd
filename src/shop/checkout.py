"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

from shop.money import percent_of

PROMO_CODES = {"WELCOME10": 10, "SUMMER15": 15, "VIP35": 35}
SUPPORTED_CITIES = ("msk", "spb")
MAX_DISCOUNT_PERCENT = 30
VAT_PERCENT = 20
SHIPPING_KOPEKS = 49_000
FREE_DELIVERY_FROM_KOPEKS = 500_000
TIER_DISCOUNTS = ((10, 5), (25, 10), (50, 15))
REQUIRED_LINE_KEYS = ("sku", "qty", "unit_price_kopecks")


def _validate_line(line: dict[str, str], index: int, seen_skus: set[str]) -> str | None:
    """Check one order line against the validation rules."""
    for key in REQUIRED_LINE_KEYS:
        if key not in line:
            return f"Line {index} is missing required key '{key}'."

    sku = str(line["sku"])
    if not sku.strip():
        return f"Line {index} has an empty sku."

    if sku in seen_skus:
        return f"Duplicate sku '{sku}' is not allowed."
    seen_skus.add(sku)

    qty_raw = line["qty"]
    try:
        qty = int(qty_raw)
    except (TypeError, ValueError):
        return f"Line {index} qty must be an integer."
    if qty <= 0:
        return f"Line {index} qty must be greater than zero."

    price_raw = line["unit_price_kopecks"]
    try:
        unit_price_kopecks = int(price_raw)
    except (TypeError, ValueError):
        return f"Line {index} unit_price_kopecks must be an integer."
    if unit_price_kopecks < 0:
        return f"Line {index} unit_price_kopecks must not be negative."

    return None


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
<<<<<<< HEAD
    if not lines:
        return "Order must contain at least one line."

    seen_skus: set[str] = set()
    normalized_promo_code = promo_code.strip().upper()
    normalized_city = shipping_city.strip().lower()

    for index, line in enumerate(lines, start=1):
        if not isinstance(line, dict):
            return f"Line {index} must be a dictionary."

        reason = _validate_line(line, index, seen_skus)
        if reason is not None:
            return reason

    if normalized_promo_code and normalized_promo_code not in PROMO_CODES:
        return "Unknown promo code."

    if normalized_city and normalized_city not in SUPPORTED_CITIES:
        return "Unsupported shipping city."
=======
    for line in lines:
        if int(line["qty"]) <= 0:
            return "Quantity must be greater than zero."
>>>>>>> d1a1b67 (GREEN)

    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    reason = validate_order(lines, promo_code, shipping_city)
    if reason is not None:
        return None

<<<<<<< HEAD
    subtotal = 0
    total_quantity = 0
    for line in lines:
        qty = int(line["qty"])
        unit_price_kopecks = int(line["unit_price_kopecks"])
        subtotal += qty * unit_price_kopecks
        total_quantity += qty

    tier_percent = 0
    for threshold, percent in TIER_DISCOUNTS:
        if total_quantity >= threshold:
            tier_percent = percent

    promo_percent = PROMO_CODES.get(promo_code.strip().upper(), 0)
    discount_percent = max(tier_percent, promo_percent)
    if discount_percent > MAX_DISCOUNT_PERCENT:
        discount_percent = MAX_DISCOUNT_PERCENT

    discount = percent_of(subtotal, discount_percent)
    discounted_subtotal = subtotal - discount

    delivery = 0
    normalized_city = shipping_city.strip().lower()
    if normalized_city and discounted_subtotal < FREE_DELIVERY_FROM_KOPEKS:
        delivery = SHIPPING_KOPEKS

    base = discounted_subtotal + delivery
    vat = percent_of(base, VAT_PERCENT)
    return base + vat
=======
    subtotal = sum(int(line["qty"]) * int(line["unit_price_kopecks"]) for line in lines)
    return subtotal + percent_of(subtotal, VAT_PERCENT)
>>>>>>> d1a1b67 (GREEN)
