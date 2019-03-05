import random
import argparse
import pprint
import numpy as np
import json

# Variables
PROJECT_MIN = 1
PROJECT_MAX = 15
BUS_RF_MIN = 1
BUS_RF_MAX = 10
PROJECT_RF_MIN = 1
PROJECT_RF_MAX = 10
PARETO_SHAPE = 3.0
WEIBULL_SHAPE = 5.0

TOTAL_PROJ_COUNT = 0


class Business:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.bus_rf = int()
        self.project_count = int()
        self.projects = dict()
        self.bus_data = dict()
        self.bus_payroll = int()
        self.claim_count = 0
        self.claim_amount = 0

        # Generate business risk factor and projects
        self.set_bus_rf()
        self.set_project_count()

        # Generate set of projects
        self.generate_projects()

        # Consolidate business level data from individual projects
        self.count_claims()
        self.count_claim_amount()
        self.count_payroll()

        # Generate output dict
        self.output_data()

    def set_bus_rf(self):
        self.bus_rf = random.randint(BUS_RF_MIN, BUS_RF_MAX)

    def set_project_count(self):
        self.project_count = random.randint(PROJECT_MIN, PROJECT_MAX)

    def generate_projects(self):
        global TOTAL_PROJ_COUNT
        for j in range(self.project_count):
            proj = Project(TOTAL_PROJ_COUNT, self.bus_id, self.bus_rf)
            self.projects['proj_id_' + str(TOTAL_PROJ_COUNT)] = proj.project_data
            TOTAL_PROJ_COUNT += 1

    def count_claims(self):
        for project in self.projects:
            self.claim_count += self.projects[project]['is_claim']

    def count_claim_amount(self):
        for project in self.projects:
            if self.projects[project]['claim_amount'] is not np.nan:
                self.claim_amount += self.projects[project]['claim_amount']

    def count_payroll(self):
        for project in self.projects:
            self.bus_payroll += self.projects[project]['payroll']

    def output_data(self):
        self.bus_data['bus_id'] = self.bus_id
        self.bus_data['bus_risk_factor'] = self.bus_rf
        self.bus_data['project_count'] = self.project_count
        self.bus_data['claim_count'] = self.claim_count
        self.bus_data['claim_amount'] = self.claim_amount
        self.bus_data['projects'] = self.projects
        self.bus_data['payroll'] = self.bus_payroll


class Project:
    def __init__(self, proj_id, bus_id, bus_rf):
        self.project_id = proj_id
        self.project_rf = int()
        self.payroll = int()
        self.is_claim = int()
        self.claim_amount = np.nan
        self.project_data = dict()
        self.bus_id = bus_id

        # Assigns values to variables
        self.set_project_rf(bus_rf)
        self.set_is_claim()
        self.set_payroll()
        self.set_claim_amount()
        self.populate_project_data(bus_rf)

    def set_payroll(self):
        self.payroll = int(np.random.weibull(WEIBULL_SHAPE) * 100000)

    def set_project_rf(self, bus_rf):
        self.project_rf = max(min(bus_rf + int(np.random.normal(loc=0.0, scale=2.0)), PROJECT_RF_MAX), PROJECT_RF_MIN)

    def set_is_claim(self):
        # self.is_claim = True if random.random() <= np.exp(self.project_rf)/np.exp(10) else False
        self.is_claim = True if random.random() >= np.log(12 - self.project_rf) else False
        # self.is_claim = True if np.random.exponential(scale=(11 -self.pro  ject_rf)) <= 0.5 else False

    def set_claim_amount(self):
        if self.is_claim == 1:
            self.claim_amount = int(np.random.pareto(PARETO_SHAPE) * self.payroll)

    def populate_project_data(self, bus_rf):
        self.project_data['bus_id'] = self.bus_id
        self.project_data['bus_risk_factor'] = bus_rf
        self.project_data['project_id'] = self.project_id
        self.project_data['project_risk_factor'] = self.project_rf
        self.project_data['is_claim'] = self.is_claim
        self.project_data['claim_amount'] = self.claim_amount
        self.project_data['payroll'] = self.payroll


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate businesses')

    parser.add_argument('-b', '--businesses', action="store", type=int)
    args = parser.parse_args()

    businesses = args.businesses

    pp = pprint.PrettyPrinter(indent=1)

    # Set random seed
    # random.seed(a=42)

    business_dict = dict()

    for i in range(businesses):
        business = Business(i)
        business_dict['bus_id_' + str(i)] = business.bus_data

    # pp.pprint(business_dict)

    with open("business.json", "w") as f:
        json.dump(business_dict, f)
