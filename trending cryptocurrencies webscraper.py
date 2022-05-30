import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def get_data():
    # get the trending page parsed data into soup format using driver
    url = 'https://www.coingecko.com/en/coins/trending'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    #get the pct change (daily) of the top 10 gainers
    aa = soup.find_all('td', {'class': 'td-change24h change24h stat-percent text-center'})
    aa = aa[0:10]
    bb = [str(x) for x in aa]
    pct = []
    for x in bb:
        x = x.split('aed":', 1)[1]
        x = x.split(',', 1)[0]
        x = round(float(x),3)
        pct.append(x)

    # get the names of the top 10 coins 
    aa = soup.find_all('span', {'class': 'd-lg-none font-bold'})
    n = [str(x) for x in aa]
    n = n[0:10]
    for x in range(0, len(n)):
        n[x] = n[x].replace('</span>', '')
        n[x] = n[x].replace('<span class="d-lg-none font-bold">', '')

    #get price
    aa = soup.find_all('td', {'class': 'td-price price'})
    aa = aa[0:10]
    aa = [str(x) for x in aa]
    p = []
    for x in aa:
        x = x.split('$', 1)[1]
        x = x.split('<', 1)[0]
        p.append(x)

    #get volume
    aa = soup.find_all('td', {'class': 'td-liquidity_score lit'})
    aa = aa[0:10]
    aa = [str(x) for x in aa]
    v = []
    for x in aa:
        x = x.split('$', 1)[1]
        x = x.split('<', 1)[0]
        v.append(x)

    #create dataframe to print
    dataframe = {'Coin Names': n, 'Daily % Change': pct, 'Price': p, 'Daily Volume': v}
    df = pd.DataFrame(dataframe)
    print(df)

    





if __name__ == "__main__":
    get_data()
