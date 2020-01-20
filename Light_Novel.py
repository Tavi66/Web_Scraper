#! /usr/bin/python3

#Download Light Novel Chapters
#And write to file (formatted)

import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import requests
import sys

#link:
#https://jingletranslations.wordpress.com/i-favor-the-villainess/

#Setup browser and beautiful soup
def setupBrowser():
    global browser
    global url
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    browser.get(url)
    
def setupSoup():
    global browser
    global content
    global soup
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
#print
def printAll():
    global soup
    print(soup.prettify())

def printContentDiv():
    global soup
    global content
    content = soup.find('div', class_='entry-content').find_all('a')
    #headers = soup.find('div', class_='entry-content').find_all('h4')
    #print chapter title and links
    #NEXT: find chapters by sections then print
    setList()
    
#Other functions
def setList():
    global urlList
    global titleList
    global content
    for link in content:
        url = link.get('href')
        title = link.string
        #print('Title: ',title)
        #print('Link: ',url)
        urlList.append(url)
        titleList.append(title)
    print('URL:', urlList)
    print('TITLE: ',titleList)
    
def closeBrowser():
    global browser
    browser.close()
    
#Main function
def main():
    global url
    
    print('from main()')
    while url == '':
        url = input('Enter LN Main Title link: ')
        
    setupBrowser()
    setupSoup()
    
    try:
        printContentDiv()
    except:
        print(sys.exc_info()[0])
        #closeBrowser()
        
    closeBrowser()

#Global Variables
browser = ''
url = ''
soup = ''
content = ''
urlList = []
titleList = []

#Program
main()
