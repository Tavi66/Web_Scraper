#Ask user for link to download images
#Ask user for folder name
#Ask if user wants a PDF of the images
#Ask if user wants to download another link
#
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import requests
import datetime
from datetime import date
from datetime import timedelta

def setupSoup (browser):
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
        
#def setupSoup(url):
#    content = urllib.request.urlopen(url).read()
#    return content

def printText():
    print(soup.title.string)
    container = soup.find_all('a')
    for link in container:
        #identifies the episodes' links
        if link.parent.name == "li" and link.find_parents("ul", id = "_listUl"):
            print(link.get('href'))
    getImages(soup)
        
def printAllText(self):
    print(soup.get_text())
#
#WEBTOON
def getImages(soup):
    images = soup.find_all('img')
    parent = soup.find("div", id = "_imageList")
    count = 1
    for img in images:
        #match img parent to div containing episode images
        if img.parent == parent:
            if img.get('src') != 'https://webtoons-static.pstatic.net/image/bg_transparency.png':
                src = img.get('src')
                print(src)
                r = requests.get(src)
                print("Saving image...")
                imgNo = "/home/vi/Pictures/TestImages/" + str(count) + ".jpg"
                try:
                    urllib.request.urlretrieve(src, imgNo)
                    print("Saved image!")
                except:
                    print("Cannot save image.")

def alertIsPresent(browser):
    try:
        alert = browser.switch_to_alert();
        alert.accept()
    except:
        print("No Alert present.")
       
def scroll(browser, url):
    browser.get(url)
    alertIsPresent(browser)
    s = "window.scrollTo(0,document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
    lenOfPage = browser.execute_script(s)
    match = False
    while(match==False):
        lastCount = lenOfPage
        browser.implicitly_wait(5)
        lenOfPage = browser.execute_script(s)
        if lastCount == lenOfPage:
            match=True
#GARFIELD###############################
def popupIsPresent(browser):
    try: #Need to check xpath
        radio = browser.find_element_by_xpath("//input[@type='radio' and @value='adult']")
        radio.click()
        return True
    except:
        print("No pop-up present.")
        return False

def submit(browser):
    submit = browser.find_element_by_id('submit')
    submit.click()
    
def getImage(soup, filename, end):
    images = soup.find_all('img')
    parent = soup.find("div", class_ = "comic-arrows")
    count = 1
    for img in images:
        #match img parent to div containing episode images
        if img.parent == parent:
            src = img.get('src')
            if downloadImage(src, filename) and filename != end:
                nextImg = soup.find("a", class_="comic-arrow-right")
                src = nextImg.get('href')
                return src
            else: return "https://garfield.com/comic/" + end

def downloadImage(src, date):
    filename = location + date + ".jpg"
    try:
        print("Downloading image %s..." %(src))
        res = requests.get(src)
        res.raise_for_status()
        print("Saving image...")
        imageFile = open(filename, 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
        #urllib.request.urlretrieve(src, filename)
        print("Successfully saved image!")
        return True
    except:
        print("Cannot save image.")
        return False
###############################################
    #class_="chapter-c"
def getChapter(soup, start, end):
    #div = soup.find_all("div")
    #parent = soup.find("div", class_="col-xs-12")
    chapter = soup.find("div", class_="chapter-c")
    filename = "choung-" + str(start)
    print(chapter.prettify())
    
#Save to PDF
def truyen():
    print("Downloading Truyen...")
    location = "/home/vi/Documents/Truyen/"
    #https://truyenfull.vn/bac-tong-phong-luu/
    url = input('Enter link: ')
    chap = int(input('From chapter: '))
    endChap = int(input('to chapter: '))
    chapterUrl = url + "chuong-" + str(chap) + "/"
    print(chapterUrl)
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    browser.get(chapterUrl)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    #setupSoup(browser)
    getChapter(soup, chap, endChap)
###############################################
def webtoon():
    print("Downloading Webtoon")
    #url = input('Enter link: ')
    #browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    #scroll(browser, url)
    ##content = setupSoup(browser.page_source)
    #content = browser.page_source
    #soup = BeautifulSoup(content, 'html.parser')
    #getImages(soup)
###############################################
def garfield():
    print("Download from")
    year = int(input("Year: "))
    month = int(input("Month: "))
    day = int(input("Day: "))
    print("to")
    eYear = int(input("Year: "))
    eMonth = int(input("Month: "))
    eDay = int(input("Day: "))
    
    today = "https://garfield.com/comic/"
    date = datetime.date(year,month,day)
    end = str(datetime.date(eYear,eMonth,eDay))
    filename = str(date)
    url = "https://garfield.com/comic/" + filename
    endUrl = "https://garfield.com/comic/" + end
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    #Pass popup verification
    while True:
        browser.get(url)
        if popupIsPresent(browser):
            submit(browser)
            break

    while url != endUrl: #"https://garfield.com/comic/":
        browser.get(url)
        print("URL: " + url)
        #setupSoup(browser)
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        url = getImage(soup, filename, end )
        if url != endUrl: #Go to next comic strip if not today's date
            nextButton = browser.find_element_by_class_name('comic-arrow-right')
            nextButton.click()
            date = date + timedelta(days=1)
            filename = str(date)

    choice = input("Do you want to continue (y/n)? ")
    if choice == 'y':
        return
    
###############################################
def main():
    print("Download from: ")
    print("1. Webtoon")
    print("2. Garfield")
    print("3. Truyen")
    print("4. exit")
    option = int(input("Enter an option: "))
    
    #location = input("Enter download directory (Enter d for default): ")
    #if location == 'd':
    #    location = default
    while True:
        if option == 1:
            webtoon()
        elif option == 2:
            garfield()
        elif option == 3:
            truyen()
        elif option == 4:
            break
###############################################
location = "/home/vi/Pictures/Images/"
default = "/home/vi/Pictures/Images/"

garfield()
#truyen()        
#main()
