from decimal import Decimal


def calculate_credit(user):
    pass

def calculate_interest(user, amount):
    """
    Calculate interest for a loan.
    TODO: Add factors into interest calculation based on credit, loan amount, etc.
    """
    return (Decimal(amount) * Decimal(0.10)).quantize(Decimal('0.00'))