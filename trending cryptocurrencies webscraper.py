#!/usr/bin/env python
#  ^ GCH usually you put this as the first line of a script in
#    in Linux.
#    If you have this line and the file is executable, you do not
#    need to call explicitly python.
#    You just call the script by name and the right python interpreter 
#    (or also other interpreted languages) is called by
#    the command line shell

# GCH
# There is difference between COMMENTs (lines starting with # like this one)
# and documentation.
# Read: https://realpython.com/documenting-python-code/
# Documentation in python is done using the docstring syntax.
# Look for example here: https://python-sprints.github.io/pandas/guide/pandas_docstring.html
# Docstring is important because it is understood by the python interpreter and by tools
# to display documentation of your code.
# For example, in visual code, if you hoover with the mouse over a call, the docstring is displayed.

'''
This program loads data about crypto currencies from a web page with specific format
or from a local file and creates a table with data for the top 10 currencies.
Run:
 python '.\new trending cryptocurrencies webscraper.py' --help
to get help
or
 python '.\new trending cryptocurrencies webscraper.py' --test
to run tests
'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import argparse


def get_data_list(soup, how_many, tag_name, tag_attrs, strip_char=""):
    '''
    Function to extract data from an BeautifulSoup document.

    :param BeautifulSoup soup: the input beautiful document
    :param int how_many: how many of the filtered items shall be processed
    :param string tag_name: the name of the tag to filter using BeautifulSoup.find_all()
    :param dictionary tag_attrs: a distionary of 'attribute': 'value' for filtering
    :param string strip_char: a string to be filtered out, if needed, from the result
    :return: a list with all filtered record.span.string content (stripped if needed)
    :rtype: list or strings

    >>> html_snippet = """
    ... [<td class="td-liquidity_score lit">
    ... <a href="/en/coins/bitcoin-god/trading_exchanges">
    ... <span class="no-wrap" data-no-decimal="false" data-price-btc="21.73214765" data-price-previous="439632.2629217823" data-target="price.price">$439,632</span>
    ... </a> </td>, <td class="td-liquidity_score lit">
    ... <a href="/en/coins/moonbirds-nft-index-by-mexc/trading_exchanges">
    ... <span class="no-wrap" data-no-decimal="false" data-price-btc="23.4021717895561" data-price-previous="473416.15319491184" data-target="price.price">$473,416</span>
    ... </a> </td>, <td class="td-liquidity_score lit">
    ... <a href="/en/coins/scardust/trading_exchanges">
    ... <span class="no-wrap" data-no-decimal="false" data-price-btc="4.62961255332621" data-price-previous="92705.78768478197" data-target="price.price">$92,706</span>
    ... </a> </td>] 
    ... """
    >>> soup = BeautifulSoup(html_snippet, 'lxml')
    >>> #samp_data = soup.find_all('td', {'class': 'td-liquidity_score lit'})
    >>> get_data_list(soup, 3, 'td', {'class': 'td-liquidity_score lit'}, "$")
    ['439,632', '473,416', '92,706']

    '''

    out_vec = []
    all_found_records = soup.find_all(tag_name, tag_attrs)
    needed_records = all_found_records[0:how_many]
    for record in needed_records:
        record_soup = BeautifulSoup(str(record), 'lxml')
        out_vec.append(record_soup.span.string.replace(strip_char,""))

    return out_vec

def load_from_web(url = 'https://www.coingecko.com/en/coins/trending', save_in_file = None):
    '''
    load the trending page from the web and parses data into soup format using driver

    If save_in_file is != None it also save the loaded page for reuse or testing

    >>> # as a test, loads the page from the default url and saves it in file
    >>> # then counts that there are al least 10 td tags
    >>> soup = load_from_web(save_in_file = "test_save.html")
    Loading data from web url: https://www.coingecko.com/en/coins/trending
     >>> td_tags = soup.find_all('td', {'class': 'td-change24h change24h stat-percent text-center'})
    >>> found_tags = len(td_tags)
    >>> found_tags >= 10
    True
    >>> # now loads the file
    >>> new_soup = load_from_file("test_save.html")
    Loading data from file: test_save.html
    >>> new_td_tags = soup.find_all('td', {'class': 'td-change24h change24h stat-percent text-center'})
    >>> found_tags == len(new_td_tags)
    True
    '''

    print("Loading data from web url: " + url)

    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url)

    if save_in_file != None:
        with open(save_in_file, "w", encoding="utf-8") as text_file:
            text_file.write(driver.page_source)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    return soup

def load_from_file(file_name):
    '''
    load the trending page from a file

    The file has been typically save by calling load_from_web()

    >>> # as a test, loads an existing file
    >>> # and counts the td tags found there
    >>> soup = load_from_file("page.html")
    Loading data from file: page.html
    >>> td_tags = soup.find_all('td', {'class': 'td-change24h change24h stat-percent text-center'})
    >>> len(td_tags)
    60
    '''
    print("Loading data from file: " + file_name)

    contents = ""
    with open(file_name, "r", encoding="utf-8") as text_file:
        contents = text_file.read()
    
    soup = BeautifulSoup(contents, 'lxml')

    return soup

def load_from_string(contents):
    '''
    load the trending page from a string

    The string has been created in some way, by loading from a source os as a text string.
    This is very useful for small and quick regression tests, in particula doctest.

    :param str contents: the input html.... describe the format
    :return: the parsed data
    :rtype: BeautifulSoup 


    >>> html_snippet = """
    ... <td class="td-liquidity_score lit">
    ... <a href="/en/coins/bitcoin-god/trading_exchanges">
    ... <span class="no-wrap" data-no-decimal="false" data-price-btc="21.73214765" data-price-previous="439632.2629217823" data-target="price.price">$439,632</span>
    ... </a> </td>
    ... """
    >>> soup = load_from_string(html_snippet)
    Loading data from string
    >>> print(soup)
    <html><body><td class="td-liquidity_score lit">
    <a href="/en/coins/bitcoin-god/trading_exchanges">
    <span class="no-wrap" data-no-decimal="false" data-price-btc="21.73214765" data-price-previous="439632.2629217823" data-target="price.price">$439,632</span>
    </a> </td>
    </body></html>

    '''
    print("Loading data from string")

    soup = BeautifulSoup(contents, 'lxml')

    return soup

def set_args(parser):
    '''
    Defines specific application command line parameters.
    It is called  by the startup utility runOrTest().
    In our case it adds exclusive command line options to load data from a 
    file or from the web.

    :param ArgumentParser parser: the ArgumentParser to be estended

    '''
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", type=str, const=None, help="Load data from a local file")
    group.add_argument("--url",  type=str, const=None, help="Load data from web at the given url")

def get_data(args):  # argv unused now, but required. To be cleaned up
    '''
    Get the trending page parsed data into soup format using driver

    This is the actual program.
    It can load data from a file or from the web.
    Loading from a file is essential to be able to test with a know set of data,
    so that it is possible to reproduce tests.

    :param list args: arguments parsed by ArgumentParser

    '''

    # GCH
    # I have split access to internet to read the page
    # (in general all data collection for a more complex application)
    # from the data manipulation .
    # This makes it easier to write tests.
    #

    # GCH: 
    # Loads data from a file or from a web url, depending
    # on the command line parameters.
    if args.file != None:
        # If a filename is given, use it
        full_soup = load_from_file(args.file)
    elif args.url != None:
        # If a url is given, use it
        full_soup = load_from_web(args.url)
    else:
        # otherwise it will default to the standard url
        full_soup = load_from_web()

    # GCH: made names of variables "speaking".
    # It is also bad practice to reuse the same variable for things 
    # of different type
    # You can syntactically do it in Python, but not in other
    # strongly typed languages.
    # Also, variable name of 1/2 characters are not searchable and therefore difficult
    # to debug.

    # get the names of the top 10 coins 
    name = get_data_list(full_soup, 10, 
                           'span', {'class': 'd-lg-none font-bold'} )
    
    # get the pct change (daily) of the top 10 gainers
    # This is a simpler parsing just taking the value from the span tag
    # instead of parsing the jason string.
    # It has only 1 decimal (do you really need 3?)
    # but can use the same parsing scheme as all other filters.
    pct = get_data_list(full_soup, 10, 
                           'td', {'class': 'td-change24h change24h stat-percent text-center'}, "%" )

    # get prices
    price = get_data_list(full_soup, 10, 
                           'td', {'class': 'td-price price'}, "$" )
      
    # get volumes
    vol = get_data_list(full_soup, 10, 
                           'td', {'class': 'td-liquidity_score lit'}, "$" )

    # create dataframe to print
    dataframe = {'Coin Names': name, 'Daily % Change': pct, 'Price': price, 'Daily Volume': vol}
    df = pd.DataFrame(dataframe)
    print(df)
    # The end

############################################################
#
# These should go in a separate library of utilities
#
###########################################################
import os, sys

def runOrTest(argv=sys.argv, fname=None, main=None, app_args=None):
    """ 
    Utility function to allow running automatically all doctest and unittest tests in a file.

    If the argv list contains the --test argument, the system will try to run the tests.
    Otherwise, if not None, it will execute the function passed in the main argument.
    This allows to selectively execute or test also executable python scripts.
 
    Args:
        argv: The command line arguments. If contains --test, the tests are executed.
              Default are the command line arguments coming from sys.argv.
        fname: The name of this same file. Must be .....
        main: A function with the signature main(argv) to be executed if not testing.
              The original argv list is passed.
              Default is None.
        app_args: function setting application specific command line arguments.


    Examples:
           # Just put the following code (uncommented) at the end of your file:
           if __name__ == '__main__':
               import m1tools.test.testRunner
               runOrTest(main=mainForTest)

           -------------

           >>> runOrTest(argv=[""], main=mainForTest)
           Running mainForTest with arguments: Namespace(test=False)

    """
    import argparse
    import pytest

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run doctest and unitest tests, if exist")
    if app_args != None:
        app_args(parser)
    args, unknown = parser.parse_known_args(argv)

    if args.test:
        # If no filename is given (the default) take the filename of the main
        if fname == None:
            import __main__ as main
            fname = main.__file__

        # --doctest-tests to ensure we test also for modules/files that contain the 'test' string in the name
        # pytestargs = ["", "-v", "--with-doctest", "--doctest-tests", "--with-xunit", "--xunit-file=" + fname + ".xml", fname]
        pytestargs = ["-v", "--doctest-modules", fname]
        pytest.main(pytestargs) 
    else:
        if main != None:
            main(args)

def mainForTest(args):
    """
    Just a simple example of main(), used for test and documentation purposes of runOrTest().
    Prints on stdout the passed arguments, typically command line arguments.

    Args:
    argv: arguments passed on the command line

    >>> mainForTest(['AAA', 'BBB'])
    Running mainForTest with arguments: ['AAA', 'BBB']
    """    
    
    print ('Running mainForTest with arguments: %s' % str(args))

####################

######################################
# Unit test
#
# This is an example of unittest
#
######################################

import unittest

class MyTest(unittest.TestCase):
    

    def test_true(self):
        """
        This test loads the standard data test file
        and verifies that it can parse exactly 60 records.
        """
        soup = load_from_file("page.html")
        td_tags = soup.find_all('td', {'class': 'td-change24h change24h stat-percent text-center'})
        self.assertEqual(len(td_tags),60)
    
# End pytest test() #
#####################

if __name__ == "__main__":
    runOrTest(main=get_data, app_args = set_args)

# __oOo__