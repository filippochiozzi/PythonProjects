# PythonProjects
Here are some of my python projects. THey are simple scripts meant to perform some analysis or get data from the web in a convenient manner

A brief explanation of the projects is below.
Note that these scripts here end by printing the results, but they can easily be integrated with other projects (which is what I hope to do over time) by just returning the dataframes and key values (without printing) to use them. 

trending cryptocurrencies webscraper: 
  In this project I parse Coingecko to get data on the CryptoCurrencies which gained the most (percentege wise) over the last 24 Hours.
  I decided to do this project since an API was not available for this specific information, and I wanted to run some analyses on the data without having to type everything in manually. 
  This project requires the libraries pandas, lxml, beatifulsoup4, requests and selenium (as well as the Google chromedriver).
  
 Portfolio Analysis Notebook: 
   In this jupyter notebook I created a simple program which retireves and calculates basic financial measures ona crypto portfolio (by getting historical data from the coingecko API). 
   I made this to understand if investing in a portfolio coul be justified using those results. 
   If anyone wishes to use it for their potfolio, it is very simple: just put the coinnames (the API tokens which can be found on coingecko) in the coins list and their respective weights in the portfolio in the weights list. 
   This project requires the libraries pandas, numpy, requests, json and matplotlib
 

