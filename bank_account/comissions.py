COMISSIONS = {
    "SA": {"Tier1": 2, "Tier2": 4, "Tier3": 6},
    "EN": {"Tier1": 1, "Tier2": 2, "Tier3": 3},
    "PA": {"Tier1": 3, "Tier2": 5, "Tier3": 7},
}


def apply_comissions(acc_balance, amount, code):
    if code in COMISSIONS:
        if 0 <= amount < 50:
            acc_balance -= amount * COMISSIONS[code]["Tier1"] / 100
        elif 50 <= amount < 500:
            acc_balance -= amount * COMISSIONS[code]["Tier2"] / 100
        elif amount >= 500:
            acc_balance -= amount * COMISSIONS[code]["Tier3"] / 100
    return acc_balance
