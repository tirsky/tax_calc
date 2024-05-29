class TaxCalculator:
    def __init__(self, tax_config):
        self.tax_config = tax_config

    def calculate_net_income(self, gross_income):
        net_income = 0
        remaining_income = gross_income

        for i, threshold in enumerate(self.tax_config["thresholds"]):
            if remaining_income <= threshold:
                net_income += remaining_income * (1 - self.tax_config["rates"][i])
                remaining_income = 0
                break
            else:
                net_income += threshold * (1 - self.tax_config["rates"][i])
                remaining_income -= threshold

        if remaining_income > 0:
            net_income += remaining_income * (1 - self.tax_config["rates"][-1])

        return net_income

    def find_gross_salary_for_net(self, desired_net_monthly_salary):
        desired_net_annual_salary = desired_net_monthly_salary * 12
        gross_income = 0
        remaining_net = desired_net_annual_salary

        for i, threshold in enumerate(self.tax_config["thresholds"]):
            if remaining_net <= threshold * (1 - self.tax_config["rates"][i]):
                gross_income += remaining_net / (1 - self.tax_config["rates"][i])
                remaining_net = 0
                break
            else:
                gross_income += threshold
                remaining_net -= threshold * (1 - self.tax_config["rates"][i])

        if remaining_net > 0:
            gross_income += remaining_net / (1 - self.tax_config["rates"][-1])

        return gross_income

    def calculate_tax(self, gross_income):
        tax = 0
        remaining_income = gross_income

        for i, threshold in enumerate(self.tax_config["thresholds"]):
            if remaining_income <= threshold:
                tax += remaining_income * self.tax_config["rates"][i]
                remaining_income = 0
                break
            else:
                tax += threshold * self.tax_config["rates"][i]
                remaining_income -= threshold

        if remaining_income > 0:
            tax += remaining_income * self.tax_config["rates"][-1]

        return tax

class TaxComparison:
    def __init__(self, net_monthly_salary, before_reform_config, after_reform_config):
        self.net_monthly_salary = net_monthly_salary
        self.before_reform_calculator = TaxCalculator(before_reform_config)
        self.after_reform_calculator = TaxCalculator(after_reform_config)

    def compare_taxes(self):
        gross_income = self.after_reform_calculator.find_gross_salary_for_net(self.net_monthly_salary)
        tax_before = self.before_reform_calculator.calculate_tax(gross_income)
        tax_after = self.after_reform_calculator.calculate_tax(gross_income)
        difference_annual = tax_after - tax_before
        difference_monthly = difference_annual / 12
        return gross_income, tax_before, tax_after, difference_annual, difference_monthly

# Константы налогов
TAX_BEFORE_REFORM = {
    "rates": [0.13, 0.15],
    "thresholds": [5000000]
}

TAX_AFTER_REFORM = {
    "rates": [0.13, 0.15, 0.18, 0.20, 0.22],
    "thresholds": [2400000, 5000000, 20000000, 50000000]
}

# Пример использования
desired_net_salary = 300000  # Желаемая зарплата на руки в месяц
comparison = TaxComparison(desired_net_salary, TAX_BEFORE_REFORM, TAX_AFTER_REFORM)
gross_income, tax_before, tax_after, difference_annual, difference_monthly = comparison.compare_taxes()

print(f"Для зарплаты на руки {desired_net_salary} рублей в месяц:")
print(f"Брутто-зарплата: {gross_income / 12:.2f} рублей в месяц")
print(f"Налог до реформы: {tax_before:.2f} рублей в год")
print(f"Налог после реформы: {tax_after:.2f} рублей в год")
print(f"Разница в налогах в год: {difference_annual:.2f} рублей")
print(f"Разница в налогах в месяц: {difference_monthly:.2f} рублей")
