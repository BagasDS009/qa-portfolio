"""Billing and shipping address test data."""

VALID_ADDRESS = {
    "street": "123 Test Street",
    "house_number": "42",
    "city": "Amsterdam",
    "state": "Noord-Holland",
    "country": "NL",
    "postcode": "1234AB",
}

VALID_BANK_TRANSFER = {
    "bank_name": "Test Bank",
    "account_name": "Test Account",
    "account_number": "1234567890",
}

PAYMENT_METHODS = {
    "bank_transfer": "Bank Transfer",
    "cash_on_delivery": "Cash on Delivery",
    "credit_card": "Credit Card",
    "buy_now_pay_later": "Buy Now Pay Later",
    "gift_card": "Gift Card",
}
