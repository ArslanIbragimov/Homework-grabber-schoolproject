import configparser
import datetime
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# options:
options = webdriver.ChromeOptions()
options.headless = True


# functions
def path(pathToFile):
    pathMain = os.getcwd().replace('\\', '/').replace('/scripts', '') + pathToFile

    return pathMain


# variables:
config = configparser.ConfigParser()
url = 'https://elschool.ru/'
browser = webdriver.Chrome(r'Important/chromedriver.exe', options=options)
iniPath = path('/Important/config.ini')
config.read(iniPath)
login = config['elschool']['login']
password = config['elschool']['password']

getWeekday = datetime.datetime.now().weekday()

width = 1920
height = 1080
# code:

try:
    def logIn():
        browser.set_window_size(width=width, height=height)
        browser.get(url=url)
        loginInput = browser.find_element(By.XPATH, '//*[@id="login"]')
        passwordInput = browser.find_element(By.XPATH, '//*[@id="password"]')
        time.sleep(0.5)
        loginInput.send_keys(login)
        passwordInput.send_keys(password)
        print('Data access')
        browser.find_element(By.XPATH, '//*[@id="sub-btn"]').click()
        time.sleep(5)
        browser.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div/div[2]/div/div/a').click()


    def getLessons():
        browser.execute_script("document.body.style.zoom='100%'")
        print('Page scale set')
        if getWeekday == 0:
            browser.find_element(By.XPATH, f'/html/body/main/div[2]/div[1]/table/tbody[2]').screenshot(
                path('/Result/ELSCHOOL.png'))
            browser.execute_script('window.scrollTo(0, 600)')
            print('Tuesday')
        if getWeekday == 1:
            browser.execute_script('window.scrollTo(0, 1400)')
            browser.find_element(By.XPATH, f'/html/body/main/div[2]/div[1]/table/tbody[3]').screenshot(
                path('/Result/ELSCHOOL.png'))
            print('Wednesday')
        if getWeekday == 2:
            browser.find_element(By.XPATH, f'/html/body/main/div[2]/div[2]/table/tbody[1]').screenshot(
                path('/Result/ELSCHOOL.png'))
            print('Thursday')
        if getWeekday == 3:
            browser.execute_script('window.scrollTo(0, 600)')
            browser.find_element(By.XPATH, f'/html/body/main/div[2]/div[2]/table/tbody[2]').screenshot(
                path('/Result/ELSCHOOL.png'))
            print('Friday')
        if getWeekday == 6 or 5 or 4:
            browser.find_element(By.XPATH, '/html/body/main/div[1]/div[2]').click()
            browser.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/table/tbody[1]').screenshot(
                path('/Result/ELSCHOOL.png'))
            print('Monday')
        print('Screenshoted.')


    def quitBrowser():
        browser.close()


    def main():
        print('start main')
        logIn()
        print('def login')
        time.sleep(5)
        getLessons()
        print('def getLessons')

except Exception as ex:
    ex.args
finally:
    quitBrowser()
# Debug variables

