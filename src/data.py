from dataclasses import dataclass

import numpy as np

@dataclass
class Portfolio:
    value: list[int]
    cash: list[int]


@dataclass
class ManagerResult:
    year_1: Portfolio
    year_2: Portfolio
    year_3: Portfolio
    year_4: Portfolio
    year_5: Portfolio
    year_6: Portfolio
    year_7: Portfolio
    year_8: Portfolio
    year_9: Portfolio


@dataclass
class SimulationResult:
    managers: dict[str, ManagerResult]

    def add_iteration_result(self, iteration_result: dict[str, Portfolio]):
        for name, portfolio in iteration_result.items():
            # Year 1
            self.managers[name].year_1.cash.append(portfolio.cash[0])
            self.managers[name].year_1.value.append(portfolio.value[0])
            # Year 2
            self.managers[name].year_2.cash.append(portfolio.cash[1])
            self.managers[name].year_2.value.append(portfolio.value[1])
            # Year 3
            self.managers[name].year_3.cash.append(portfolio.cash[2])
            self.managers[name].year_3.value.append(portfolio.value[2])
            # Year 4
            self.managers[name].year_4.cash.append(portfolio.cash[3])
            self.managers[name].year_4.value.append(portfolio.value[3])
            # Year 5
            self.managers[name].year_5.cash.append(portfolio.cash[4])
            self.managers[name].year_5.value.append(portfolio.value[4])
            # Year 6
            self.managers[name].year_6.cash.append(portfolio.cash[5])
            self.managers[name].year_6.value.append(portfolio.value[5])
            # Year 7
            self.managers[name].year_7.cash.append(portfolio.cash[6])
            self.managers[name].year_7.value.append(portfolio.value[6])
            # Year 8
            self.managers[name].year_8.cash.append(portfolio.cash[7])
            self.managers[name].year_8.value.append(portfolio.value[7])
            # Year 9
            self.managers[name].year_9.cash.append(portfolio.cash[8])
            self.managers[name].year_9.value.append(portfolio.value[8])


def get_average_value_over_years_for_managers(manager_results: SimulationResult):
    for name, manager in manager_results.managers.items():
        avg = str(np.average(manager.year_9.value))

        print(name + ": final_value=" + avg)
