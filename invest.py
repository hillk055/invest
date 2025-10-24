import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tax import tax_with_ni
import math


class InvestmentAppreciation:

    def __init__(self, salary, property_metrics: {}):

        # Default Params

        self.rental_income: float = 0
        self.rental_property_value: float = 0
        self.salary_end: int = 20
        self.salary: int = 0

        # If no plans to sell property -> self.rental_income_end = math.inf
        self.rental_income_end: float = 0

        self.propert_metrics = property_metrics
        if len(property_metrics.keys()) != 0:
            for key, value in self.propert_metrics.items():
                if not value['Owned']:
                    continue
                self.rental_income, self.rental_property_value = value['Rent'], value['Value']
        print(self.rental_income)


        # Non-long term incomes (SALARY, RENTAL)
        # Salary can either be given as a list of upcoming salaries or a fixed value
        self.salary = salary

        if isinstance(self.salary, list):
            self.salary_end = len(self.salary)
        else:
            self.salary = [self.salary] * self.salary_end


        self.networth = 900_000 + 75_000
        self.portfolio_value = 100_000
        self.dividends = 200
        self.added_costs = 8000  # Every 5 years
        self.time_period = 20  # Years
        self.pension_value = 100_000
        self.money_drawn_each_year = 4500 * 12
        self.cash_savings: int = 100_000
        self.inflation: int = 4
        self.current_savings = 100_000
        self.premium_bonds_value = 50_000

        self.premium_bonds_interest: float = 3.8
        self.cash_interest: float = 4
        self.pension_interest = 7.5
        self.inflation = 4

    def convert(self):

        self.pension_interest /= 100
        self.premium_bonds_interest /= 100
        self.cash_interest /= 100
        self.inflation /= 100

    def property(self, i):

        if self.rental_income is None:
            return 0
        if i == self.rental_income_end:
            return

    def loop(self):

        """
        Assumptions:
        1) Interest added at the end of the year, lower bond estimate for savings
        2) All costs deducted before interest paid, in reality accumulated on a daily basis so interest amounts paid
        would be higher than calculated here.

        """
        pension = []
        savings = []
        self.convert()

        for i in range(self.time_period):

            savings.append(self.current_savings)
            pension.append(self.pension_value)

            if i != 0 and i % 5 == 0:
                self.current_savings -= self.added_costs

            # Add salary before retirement, after salary = 0
            if i < self.salary_end:
                print(self.salary[i])
                insurance_metrics = tax_with_ni(self.salary[i])
                salary = insurance_metrics['Net pay']
                self.current_savings += salary

            # Add rental income if given, or sell the property and rental income = 0
            if self.rental_income is not None:
                if i == self.rental_income_end:
                    self.current_savings += self.rental_property_value
                    self.rental_income = None
                else:
                    self.current_savings += self.rental_income

            # Add dividends and rental income every year
            self.current_savings += self.dividends
            self.current_savings -= self.money_drawn_each_year

            self.current_savings *= (1 + self.cash_interest)
            self.current_savings += self.premium_bonds_value * (1 + self.premium_bonds_interest)
            self.pension_value *= (1 + self.pension_interest)
            self.current_savings *= (1-self.inflation)

        return savings, pension


def main():

    sal1 = [78_000, 111_000, 108_000, 137_000, 137_000, 50_000, 36_000]
    properties = {'property1': {'Owned': True, 'Rent': 9600, 'Value': 225_000}}
    portfolio = {'cash isa': {'Value': 67_000, 'Tax Free': True, 'yield': 3.5},
                 'savings': {'Value': 214.109, 'Tax Free': False, 'yield': 3.5},
                 'current_account': {'Value': 22_440, 'Tax Free': False, 'yield': 3.5},
                 'pension': {'Value': 670_000, 'Tax Free': False, 'yield': 3.5}}

    inv = InvestmentAppreciation(salary=sal1, property_metrics=properties)
    '''save1, _ = inv.loop()
    sal2 = 40_000
    inv2 = InvestmentAppreciation(salary=sal2)
    sav2, _ = inv2.loop()
    plt.plot(save1)
    plt.plot(sav2)
    plt.show()'''


if __name__ == "__main__":

    main()











