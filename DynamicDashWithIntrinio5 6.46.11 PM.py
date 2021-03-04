# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Import pandas and numpy
import pandas as pd
import numpy as np

# Import my fiancial data classes
from IntrinioAPIGetStockPriceData import StockData
from IntrinioAPIStandardizedFinancials import FundamentalData

#############################################################
def create_table(dataframe, max_rows=30):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
#############################################################
## Dash Application ##
# Dash framwork
app = dash.Dash(__name__)

app.layout = html.Div(children = [
        html.A(html.Button("New Stock"), href="http://127.0.0.1:8050/", target="_blank"),
        html.Div(children="Input Ticker: "),
        dcc.Input(id='ticker', value='', type='text'),
        html.Div(children="Input Number of Trading Days: "),
        dcc.Input(id='tradingDays', value='', type='text'),
        html.Div(children="Input Fiscal Year: "),
        dcc.Input(id='FY', value='', type='text'),
        html.Div(id='general_data_output')

])

########################################################################
@app.callback(
    Output(component_id='general_data_output', component_property='children'),
    [Input(component_id='ticker', component_property='value'),
    Input(component_id='tradingDays', component_property='value'),
    Input(component_id='FY', component_property='value')]
)
def update_financialData(input_ticker, input_tradingDays, FY):
    ## Call Price Data ##
    TickerStockData = StockData(input_ticker, int(input_tradingDays)) # Ticker and number of trading days to query for
    TickerStockData.getStockData() # populate with data from ticker

    ## Call Fundamental Data ##
    Stock_FinancialData = FundamentalData(input_ticker, int(FY))
    Stock_FinancialData.getFinancialData()
    # Populate Dataframes with Fundamental Data
    balance_sheet_statement_DF = pd.DataFrame(list(Stock_FinancialData.balance_sheet_statement.items()), columns=['Line Item', 'Value in USD'])
    income_statement_DF = pd.DataFrame(list(Stock_FinancialData.income_statement.items()), columns=['Line Item', 'Value in USD'])
    cash_flow_statement_DF = pd.DataFrame(list(Stock_FinancialData.cash_flow_statement.items()), columns=['Line Item', 'Value in USD'])

    fundamentals = {
    'Indicator': [
    'P/E Ratio',
    'EV/EBITDA',
    'P/B Ratio',
    'EBITDA',
    'EBIT',
    'Enterprise Value',
    'CapEx',
    'Market Capitalization'
    ],'Value':[
    Stock_FinancialData.calculations['Price to Earnings (P/E)'],
    Stock_FinancialData.calculations['Enterprise Value to EBITDA (EV/EBITDA)'],
    Stock_FinancialData.calculations['Price to Book Value (P/BV)'],
    Stock_FinancialData.calculations['Earnings before Interest, Taxes, Depreciation and Amortization (EBITDA)'],
    Stock_FinancialData.calculations['Earnings before Interest and Taxes (EBIT)'],
    Stock_FinancialData.calculations['Enterprise Value (EV)'],
    Stock_FinancialData.calculations['Capital Expenditures (CapEx)'],
    Stock_FinancialData.calculations['Market Capitalization'],

    ]}

    fundamentals_DF = pd.DataFrame(fundamentals)

    return (html.H1(children= input_ticker), dcc.Graph(id = TickerStockData.identifier + ' Price Data',
              figure = {
                      'data': [
                              {'x' : TickerStockData.correspondingDates[0:len(TickerStockData.correspondingDates) -1], 'y' : TickerStockData.priceData[0:len(TickerStockData.priceData)-1], 'type':'line', 'name':TickerStockData.identifier},
                              ],
                      'layout': {
                              'title': TickerStockData.identifier + ' Price Data Over the Past ' + str(TickerStockData.dayCount) + ' Trading Days', 'xaxis':{ 'title':'Date' }, 'yaxis':{ 'title':'USD' }
                              }
                      }),html.H3(children='Fiscal Year: ' + FY),
                      html.H4(children='Balance Sheet Statement'),
                      create_table(balance_sheet_statement_DF),
                      html.H4(children='Income Statement'),
                      create_table(income_statement_DF),
                      html.H4(children='Cash Flow Statement'),
                      create_table(cash_flow_statement_DF),
                      html.H4(children='Fundamental Calculations'),
                      create_table(fundamentals_DF),)

########################################################################


if __name__ == '__main__':
    app.run_server(debug = True)
