#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset:4 -*-

import unittest
import logging

import pandas_market_calendars as mcal
import pandas as pd

from qa_dataprovider.generic_dataprovider import GenericDataProvider
from qa_dataprovider.csv_dataprovider import CsvFileDataProvider


class TestCsv(unittest.TestCase):

    def test_daily_trading_days(self):
        provider = CsvFileDataProvider(["data"])

        daily = provider.get_data(['DIS'],'2010-01-01','2017-01-01')[0]

        assert daily.loc['2016-01-04']['Day'] == 1 # Monday Jan. 4
        assert daily.loc['20160108']['Day'] == 5 # Friday Jan. 8
        assert daily.loc['20160111']['Day'] == 6  # Monday Jan. 11
        assert daily.loc['20161230']['Day'] == 252  #240? Friday Dec. 30

    def test_filter_days(self):
        provider = CsvFileDataProvider(["data"])

        nyse = mcal.get_calendar('NYSE')

        days = nyse.valid_days(start_date='2000-01-01', end_date='2017-01-01')
        daily = provider.get_data(['DIS'], '2000-01-01', '2017-01-01')[0]
        assert len(days) == len(daily)

    def test_infront_daily(self):
        provider = CsvFileDataProvider(["data"])
        nyse = mcal.get_calendar('NYSE')
        days = nyse.valid_days(start_date='2008-01-01', end_date='2015-12-31')
        daily_xlp = provider.get_data(['NYSF_XLP'], '2008-01-01', '2015-12-31')[0]

        # XLP	2008-04-23	00:00	27,9	28,21	27,9	28,05	1363528
        # XLP     2010-11-05      00:00   29,19   29,2301 29,02   29,13   6008732
        #print(daily_xlp.loc['2010-11-05'])
        assert daily_xlp.loc['2010-11-05']['High'] == 29.2301



    def test_generic_5min(self):
        pass



if __name__ == '__main__':
    unittest.main()