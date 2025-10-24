def tax_with_ni(income):
    total_income = income
    total_tax_to_pay = 0
    total_ni_to_pay = 0

    # ---- PERSONAL ALLOWANCE ----
    personal_allowance = 12_570
    if income > 100_000:
        personal_allowance = max(0, personal_allowance - (income - 100_000) / 2)

    # ---- INCOME TAX ----
    if income > 125_140:
        total_tax_to_pay += (income - 125_140) * 0.45
        income = 125_140

    if 50_270 < income <= 125_140:
        total_tax_to_pay += (income - 50_270) * 0.40
        income = 50_270

    if personal_allowance < income <= 50_270:
        total_tax_to_pay += (income - personal_allowance) * 0.20

    # ---- NATIONAL INSURANCE ----
    # Reset income for NI, since NI doesn't use personal allowance adjustments
    ni_income = total_income

    if ni_income > 50_270:
        total_ni_to_pay += (50_270 - 12_570) * 0.08  # 8% between £12,570–£50,270
        total_ni_to_pay += (ni_income - 50_270) * 0.02  # 2% above £50,270
    elif ni_income > 12_570:
        total_ni_to_pay += (ni_income - 12_570) * 0.08

    # ---- TOTAL DEDUCTIONS ----
    take_home_pay = total_income - total_tax_to_pay - total_ni_to_pay

    return {
        "Income": total_income,
        "Tax": round(total_tax_to_pay, 2),
        "National Insurance": round(total_ni_to_pay, 2),
        "Net pay": round(take_home_pay, 2)
    }






