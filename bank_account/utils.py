COMISSIONS = {
    "OUT": {"Tier1": 2, "Tier2": 4, "Tier3": 6},
    "INC": {"Tier1": 1, "Tier2": 2, "Tier3": 3},
    "PAY": {"Tier1": 3, "Tier2": 5, "Tier3": 7},
}


def apply_movement(acc_balance, amount, kind):
    if kind in COMISSIONS:
        if 0 <= amount < 50:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier1"] / 100)
        elif 50 <= amount < 500:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier2"] / 100)
        elif amount >= 500:
            total_amount = amount + (amount * COMISSIONS[kind]["Tier3"] / 100)

        if acc_balance >= total_amount:
            total_balance = acc_balance - total_amount
            return total_balance, True
    return acc_balance, False
