from __future__ import print_function
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
import pandas as pd
import numpy as np
from collections import OrderedDict

class FundamentalData:

    def __init__(self, identifier="", fiscal_year=0):
        self.identifier = identifier
        # 'income_statement' # 'balance_sheet_statement' # 'cash_flow_statement'
        self.fiscal_year = fiscal_year
        self.income_statement = OrderedDict() # Ordered Dict is nessasary to maintain finaical statement configuration
        self.balance_sheet_statement = OrderedDict()
        self.cash_flow_statement = OrderedDict()
        self.calculations = {} # An Ordered Dict is unnessasary here as we query for specific key value pairs.


    def getFinancialData(self):
        # link API key
        intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'YOUR API KEY'

        fundamentals_api = intrinio_sdk.FundamentalsApi()
        statement_code = ['income_statement', 'balance_sheet_statement', 'cash_flow_statement', 'calculations']
        id_codes = []

        fiscal_period = 'FY' # str | The fiscal period


        # Get the ID for the statement
        i = 0
        for i in range(len(statement_code)):
            try:
                api_FundamentalResponse = fundamentals_api.lookup_fundamental(self.identifier, statement_code[i], self.fiscal_year, fiscal_period).__dict__
                id_codes.append(api_FundamentalResponse['_id']) # assign discovered ID to the id variable
            except ApiException as e:
                print("Exception in SecurityApi occured-- lookup_fundamental: %s\n" % e)

        # Get the data with the id for income_statement
        try:
            # get responce from api and convert object to dictinary
            api_FiancialsResponse = fundamentals_api.get_fundamental_standardized_financials(id_codes[0]).__dict__

            # get array of dictinarys
            financials = api_FiancialsResponse['_standardized_financials']

            # print out content
            i = 0
            while i < len(financials):
                # get the value of the line item
                currentValue = financials[i].__dict__['_value']

                # get the name of the current line item
                currentTag = financials[i].__dict__['_data_tag'].__dict__['_name']

                # format and print tag and value
                self.income_statement[currentTag]=currentValue

                # increment counter
                i += 1


        except ApiException as e:
            print("Exception in SecurityApi occured-- get_fundamental_standardized_financials: %s\n" % e)
        ##############################################################################
        # Get the data with the id for balance_sheet_statement
        try:
            # get responce from api and convert object to dictinary
            api_FiancialsResponse = fundamentals_api.get_fundamental_standardized_financials(id_codes[1]).__dict__

            # get array of dictinarys
            financials = api_FiancialsResponse['_standardized_financials']

            # print out content
            i = 0
            while i < len(financials):
                # get the value of the line item
                currentValue = financials[i].__dict__['_value']

                # get the name of the current line item
                currentTag = financials[i].__dict__['_data_tag'].__dict__['_name']

                # format and print tag and value
                self.balance_sheet_statement[currentTag]=currentValue

                # increment counter
                i += 1


        except ApiException as e:
            print("Exception in SecurityApi occured-- get_fundamental_standardized_financials: %s\n" % e)
        ##############################################################################
        # Get the data with the id for cash_flow_statement
        try:
            # get responce from api and convert object to dictinary
            api_FiancialsResponse = fundamentals_api.get_fundamental_standardized_financials(id_codes[2]).__dict__

            # get array of dictinarys
            financials = api_FiancialsResponse['_standardized_financials']

            # print out content
            i = 0
            while i < len(financials):
                # get the value of the line item
                currentValue = financials[i].__dict__['_value']

                # get the name of the current line item
                currentTag = financials[i].__dict__['_data_tag'].__dict__['_name']

                # format and print tag and value
                self.cash_flow_statement[currentTag]=currentValue

                # increment counter
                i += 1


        except ApiException as e:
            print("Exception in SecurityApi occured-- get_fundamental_standardized_financials: %s\n" % e)
        ##############################################################################
        # Get the data with the id for calculations
        try:
            # get responce from api and convert object to dictinary
            api_FiancialsResponse = fundamentals_api.get_fundamental_standardized_financials(id_codes[3]).__dict__

            # get array of dictinarys
            financials = api_FiancialsResponse['_standardized_financials']

            # print out content
            i = 0
            while i < len(financials):
                # get the value of the line item
                currentValue = financials[i].__dict__['_value']

                # get the name of the current line item
                currentTag = financials[i].__dict__['_data_tag'].__dict__['_name']

                # format and print tag and value
                self.calculations[currentTag]=currentValue

                # increment counter
                i += 1


        except ApiException as e:
            print("Exception in SecurityApi occured-- get_fundamental_standardized_financials: %s\n" % e)
        ##############################################################################
