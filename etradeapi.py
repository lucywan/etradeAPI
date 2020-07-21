#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:55:55 2020

@author: lucywan
"""

#about 20 seconds total
from selenium.webdriver import Chrome
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException     
import time
import datetime

wdriver = "/Applications/chromedriver"
# driver = Chrome(wdriver)
# driver.get("https://us.etrade.com/home/welcome-back")

driver = webdriver.Chrome("/Applications/chromedriver")
driver.get("https://us.etrade.com/home/welcome-back")
def login(username, password):
#     u_name = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "user_orig")))
    u_name = driver.find_element_by_id("user_orig")
    u_name.clear()
    u_name.send_keys(username)
    p_word = driver.find_element_by_name("PASSWORD")
    p_word.clear()
    p_word.send_keys(password)
    logon = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/section/section/div/div/div[1]/div/section/div/div[1]/div/div/form/div[5]/div[2]/button")
    logon.click()
    time.sleep(1)

def getPortfolio():
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, """//*[@id="new-nav-layout"]/div[4]/div[1]/div[2]/div/div[3]/a"""))).click()
    portfolio = driver.find_element_by_xpath("""//*[@id="new-nav-layout"]/div[4]/div[1]/div[2]/div/div[3]/a""")
    portfolio.click()
#     ActionChains(driver).move_to_element(portfolio).click(portfolio).perform()
#     html_orig = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div/section[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div"))).get_attribute('innerHTML')
#     print(html_orig)
#     html_head = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div/section[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div")
#     html_orig = html_head.get_attribute('innerHTML')
    time.sleep(10)
    html = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[2]/div/div/div[1]/div/section[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div")
    html_orig = html.get_attribute('innerHTML')
    body = driver.find_element_by_xpath('//*[@id="center"]/div/div[4]/div[2]/div/div[1]')
    string = body.text
    print(string)
    string = string.split('\n')
    print(string)
    stocks = int(len(string)/13)
    j = 1
    simple_lis = []
    for i in range(stocks):
        lis = string[j:j+1] + string[j+3:j+12]
        simple_lis.append(lis)
        j += 13
    prog = re.compile('\<button class="header-name-button" data-col-name="">(.*?)\<')
    #header = prog.findall(html_orig)
    #remove actions add value (hard code)
    header = ['Symbol', 'LastPrice$', 'Change$',
       'Change%', 'Qty#', 'PricePaid$', 'DayGain$',
       'TotalGain$', 'TotalGain%', 'Value']
    port = pd.DataFrame(simple_lis, columns = header)
    port['Symbol'] = port['Symbol'].apply(lambda x: x.replace("info_outline",""))
    print(port)
    return port

def visit_trade_page():
    trade = driver.find_element_by_xpath('//*[@id="new-nav-layout"]/div[3]/div[3]/div[2]/a')
    trade.click()
def input_symbol(symbol):
    sym = driver.find_element_by_xpath('//*[@id="symbol"]')
    sym.clear()
    sym.send_keys(symbol)
    sym.send_keys(Keys.RETURN)
def preview_order():
    preview = driver.find_element_by_xpath('//*[@id="preview-review"]')
    preview.click()
    
def place_order():
    place_order = driver.find_element_by_xpath('//*[@id="etContent"]/div/div[1]/div/div/div[3]/section/div[1]/div/div/div/article/div/div/div[6]/div/div/div[2]/button')
    place_order.click()
def input_quant(quantity):
    quant = driver.find_element_by_xpath('//*[@id="quantity"]')
    quant.clear()
    quant.send_keys(quantity)
def input_limit(price):
    limit = driver.find_element_by_xpath('//*[@id="limitprice1"]')
    limit.clear()
    limit.send_keys(price)
def input_date(date):
    d = driver.find_element_by_xpath('//*[@id="gtd"]')
    d.clear()
    d.send_keys(date)
def sizes():
    p = re.compile("[^\sx]*")

    bid = driver.find_element_by_xpath('//*[@id="snapshotView"]/div[1]/div[2]/table/tbody/tr[1]/td').text
    ask = driver.find_element_by_xpath('//*[@id="snapshotView"]/div[1]/div[2]/table/tbody/tr[2]/td').text
    last = driver.find_element_by_xpath('//*[@id="snapshotView"]/div[1]/div[1]/table/tbody/tr[2]/td').text
    bid = float(p.search(bid).group(0))
    ask = float(p.search(ask).group(0))
    last = float(p.search(last).group(0))
    return str(max(bid, ask, last))
def weekday(date):
    month, day, year = (int(i) for i in date.split('/'))     
    if (datetime.date(year, month, day).weekday()) >= 5:
        return False
    return True
    
def trade_page_setup(symbol, action, quantity, price_type, duration = "", date = "", limit_price = ""):
    visit_trade_page()
    time.sleep(1)
    input_symbol(symbol)
    time.sleep(1)
    options = driver.find_element_by_xpath('//*[@id="ordertype"]')
    options_dropdown = Select(options);
    options_dropdown.select_by_visible_text(action)
    p_type = driver.find_element_by_xpath('//*[@id="pricetype"]')
    p_type_dropdown = Select(p_type);
    p_type_dropdown.select_by_visible_text(price_type)
    if (price_type == "Limit"):
        if limit_price == "":
            input_limit(sizes())
        else:
            input_limit(limit_price)
    input_quant(quantity)
    dur = driver.find_element_by_xpath('//*[@id="term"]')
    dur_dropdown = Select(dur);
    if (duration == ""):
        duration = "Good for Day"
    dur_dropdown.select_by_visible_text(duration)
    
    if (duration == "Good Until Date (GTD)"):
        input_date(date)
        
        
def trade(symbol, action, quantity, price_type, duration = "", date = "", limit_price = ""):
    trade_page_setup(symbol, action, quantity, price_type, duration = "")
    preview_order()
    try:
        driver.find_element_by_xpath('//*[@id="pricetype"]')
    except NoSuchElementException:
        print("True")
    time.sleep(1)
    place_order()
    
################################ example code
username = "********"
password = "********"
login(username, password)
getPortfolio()
trade("CLWT", "Buy", "1", "Limit", date = "06/11/2020")
trade("CLWT", "Buy", "1", "Limit", date = "06/11/2020")


#try to sell and see what error it gives you


#df = getPortfolio()
#df['Change&nbsp;%']
#   print(df.to_string())

#df['Symbol'].iloc[0]

#for i in range(df.shape[0]):
#    trade(df['Symbol'].iloc[i], "Sell", df['Change&nbsp;%'].iloc[i], "Market")

