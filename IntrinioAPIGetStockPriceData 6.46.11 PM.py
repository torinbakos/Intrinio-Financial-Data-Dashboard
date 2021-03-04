import time
from datetime import datetime, date, timedelta
import intrinio_sdk
from intrinio_sdk.rest import ApiException

class StockData:

    def __init__(self, identifier="", dayCount=0):
        self.dayCount = dayCount
        self.identifier = identifier
        self.priceData = []
        self.correspondingDates = []


    def getStockData(self):
        intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'YOUR API KEY'
        security_api = intrinio_sdk.SecurityApi()

        page_size = self.dayCount
        frequency = 'daily' # str | Sort by date `asc` or `desc` (optional)
        next_page = '' # str | Gets the next page of data from a previous API call (optional)
        start_date = str(date.today() - timedelta(days = self.dayCount)) # date | Get historical data on or after this date (optional)
        end_date = str(date.today())

        try:
            api_StockPriceResponse = security_api.get_security_stock_prices(self.identifier, start_date=start_date, end_date=end_date, frequency=frequency, page_size=page_size).__dict__
            list_of_StockPriceDicts = api_StockPriceResponse['_stock_prices']
            i = 0
            while i < len(list_of_StockPriceDicts):
                self.priceData.append(list_of_StockPriceDicts[i].__dict__['_adj_close'])
                self.correspondingDates.append(list_of_StockPriceDicts[i].__dict__['_date'])
                i += 1
        except ApiException as e:
            print("Exception in SecurityApi occured-- get_security_historical_data: %s\n" % e)
