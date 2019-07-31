#! /usr/bin/python3

#Ask user for link to download images
#Ask user for comic folder path. 
#get episode number/name from page_source
#create directory in comic directory (get title of page_source)
#Ask if user wants a PDF of the images
#Ask if user wants to download another link
#
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request
import requests
import datetime
from datetime import date
from datetime import timedelta
from PIL import Image

def setupSoup (browser, url):
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
def getImagesW(soup, browser):
    global location
    global parentFolder
    global titles
    global currentIndex

    images = soup.find_all('img', class_='_images')
    parent = soup.find("div", id = "_imageList")    
    title = titles[currentIndex]
    folderPath = location + parentFolder + title + '/'
    mkdir(folderPath)
    print('Retrieving ' + title + '...')
    count = 1
    for img in images:
        #match img parent to div containing episode images
        #if img.parent == parent:
        #print(img)
        if img.get('src') != 'https://webtoons-static.pstatic.net/image/bg_transparency.png':
            src = img.get('src')
            #print(src)
            browser.get(src)
            #print("Saving image...")
            filename = folderPath + str(count) + '.png'
            try:
                #print("Saving image...")
                #print(src)
                browser.save_screenshot(filename)
                cropImage(filename)
                count+=1
                #print("Saved image!")
#                    downloadImageW(src,browser)
            except:
                return
                #print("Cannot save image.")
    print('Finished retrieving ' + title + '!')
def getNextEpisode():
    print("Checking files...")
    #check if directory exists
    #check if episodes exists in directory
    #episodeList = checkFilesExist(episodeList)
    checkFilesExist(episodeList)
    print("File check complete!")
    #return episodeList
    
def getEpisodeList(soup):
    #print('Retrieving Episode List...')
    episodeList = []
    epList = soup.find('ul', id = '_listUl')
    #find the a-atributes
    for ep in epList.descendants:
        if ep.name == 'a' and not ep.parent.name == 'span':
            link = ep.get('href')
            #print(link)
            episodeList.append(link)
    return episodeList

def getEpisodeTitleList(soup):
    #print('Retrieving Episode Titles...')
    titleList = []
    epList = soup.find('ul', id = '_listUl')
    tList = soup.find_all('span', class_='subj')
    #find the a-attributes
    for t in tList:
        if t.parent.name == 'a':
            title = t.text
            #print(title)
            titleList.append(title)
    return titleList

#get all episodes in comic link + episode title
#get all pages #clicks each link get the episode link
def getEpisodes(soup,browser):
    global parentFolder
    global comicName
    global comicType
    
    if comicType == 'f':
        comicName = soup.find('h1',class_='subj').string
    else:
        comicName = input('Enter comic name: ')
        
    parentFolder = comicName + '/'
    root = "https://www.webtoons.com"
    if not rootExists():
        mkroot()
    #pages
    pagesParent = soup.find('div',class_='paginate')
    pages = soup.find_all('a')
    pageList = []
    episodeList = []
    episodeTitleList = []
    #get pages
    for link in pages:
        if link.parent == pagesParent:
            a = link.get('href')
            if not a == '#':
                pageList.append(root + a)
            else:
                pageList.append(a)

    print("\nRetrieving Episode List...")
    for a in pageList:
            #print("\nRetrieving Episode List from: " + a)
            if not a == '#':
                browser.get(a)
                content = browser.page_source
                soup = BeautifulSoup(content, 'html.parser')
            epList = getEpisodeList(soup)
            episodeList.extend(epList)
            #get episode titles
            episodeTitleList.extend(getEpisodeTitleList(soup))
            
    print("Retrieved Episode List!")

    print("Checking files...")
    #check if directory exists
    #check if episodes exists in directory
    #episodeList = checkFilesExist(episodeList)
    episodeList = checkFilesExist(episodeList,episodeTitleList)
    print("File check complete!")
    
    print("Titles: " + str(len(titles)) )
    print("Links: "+ str(len(episodeList)) )
    return episodeList
    #print(episodeList)
    #print(pageList)
    
#check which files exists
#if an episode exists, remove from list, then return remaining list
def checkFilesExist(episodeList, episodeTitleList):
    total = len(episodeTitleList)
    toRemoveEp = []
    toRemoveT = []
    for index in range(0,total):
        title = episodeTitleList[index]
        print(title)
        if episodeExists(title):
            print('[' + title + '] exists!' )
            #mark index to delete
            toRemoveT.append(title)
            toRemoveEp.append(episodeList[index])
            
    for item in toRemoveEp:
        print('Removing ' + item + '...')
        episodeList.remove(item)
        print('Removed episode url!')

    global titles
    titles = episodeTitleList
    for item in toRemoveT:
        print('Removing ' + item + '...')
        titles.remove(item)
        print('Removed episode name!')
        
    return episodeList

# def downloadImageW(src, browser):
#     browser.get(src)
#     print("Saving image...")
#     global filename
#     filename = "/home/vi/Pictures/Test/" + str(count) + ".png"
#     try:
#         res = requests.get(src)
#         res.raise_for_status()
#         print("Saving image...")
#         imageFile = open(filename, 'wb')
#         for chunk in res.iter_content(100000):
#             imageFile.write(chunk)
#         imageFile.close()
#
#         print("Saved image!")
#     except:
#         print("Cannot save image.")

def cropImage(filename):
    #530x843
    #img = Image.open(filename)
    #img.crop((463,0,993,843))
    global comicType
    if comicType == 'f':
        img = Image.open(filename)
        cropped = img.crop((467,0,993,843))
        cropped.save(filename)
    #elif comicType == 'c':
    #    cropped = img.crop((425,0,1035,843))
    #cropped.save(filename)
    
def alertIsPresent(browser):
    #browser.implicitly_wait(2)
    try:
        alert = browser.switch_to_alert();
        print("Alert is present...")
        alert.accept()
        print("Alert accepted!")
    except:
        print("No Alert present.")
       
def scroll(browser, url):
    alertIsPresent(browser)
    #browser.get(url)
    body = browser.find_element_by_tag_name('body')
    body.send_keys(Keys.SPACE)
    browser.implicitly_wait(5)
    for i in range (0,600):
        body.send_keys(Keys.SPACE)
    browser.implicitly_wait(1)
    
    #try explicit wait. if element img.get 'src' not 'bg.transparent'

def rootExists():
#    folder = ""
#    for c in folderName:
#        if c == '&':
#            folder.append('and')
#        else:
#            folder.append(c)
    global parentFolder
    global location
    path = location + parentFolder
    print("Checking " + path + "...")
    if os.path.exists(path):
        print("["+parentFolder+"] exists!")
        return True  
    else:
        print("["+parentFolder+"] does not exist!")
        return False
    
def episodeExists(filename):
    global parentFolder
    global location
    path = str(location + parentFolder + filename)
    print("Checking " + path + "...")
    if os.path.exists(path):
        print("[" + filename + "] exists!")
        return True
    else:
        #print("File does not exist!")
        return False
    
def mkroot():
    global parentFolder
    global location
    path = location + parentFolder
    os.mkdir(path)

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    
#def mkdir(typeOfComic):
#    if(typeOfComic == 1): #Webtoon
#        global newPath
#        global location
#        global parentFolder
#        newPath = location + parentFolder + "/Episode " + episodeNo +"/"
#        if not os.path.exists(newPath):
#            os.mkdir(newPath)
#    elif (typeOfComic == 2): #Other 
#        return

def moveImages():
    global newPath
    global count
    global parentFolder
    path = "/home/vi/Pictures/Webtoon/" + parentFolder + "/Episode " + episodeNo +"/"
    for i in range(1,count):
        oldPath = "/home/vi/Pictures/Test/" + str(i) + ".png"
        newPath = path + str(i) + ".png"
        os.rename(oldPath, newPath)

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
def other():
    print('Empty...')
###############################################
def webtoon():
    global parentFolder
    global episodeNo
    global comicType
    global location
    global currentIndex

    location = "/home/vi/Pictures/Webtoon/"
    
    print("Downloading Webtoon")
    #get info of comic
    url = input('Enter link: ')
    #parentFolderName = input ('Enter comic root folder: ') + '/'
    #episodeNo = input ('Enter episode #: ')
    comicType = input ('Featured or Challenge (f/c): ')
    
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    browser.get(url)
    
    #scroll through page
    #scroll(browser, url)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')

    #global comicName
    #comicName = soup.find('h1',class_='subj').string
    #parentFolder = comicName + '/'

    #if comicType == 'f' or comicType == 'c':
    episodes = getEpisodes(soup, browser)
    #this works for featured webtoons
    for link in episodes:
        browser.get(link)
        scroll(browser,link)
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        getImagesW(soup, browser)
        currentIndex+=1
    #elif comicType == 'c':
    #    episodes = getEpisodes(soup,browser)
        
    #episodes = ['https://www.webtoons.com/en/fantasy/mage-and-demon-queen/episode-5/viewer?title_no=1438&episode_no=5',
    #            'https://www.webtoons.com/en/fantasy/mage-and-demon-queen/episode-4/viewer?title_no=1438&episode_no=4']
    #global titles
    #titles = ['Episode 5','Episode 4']
    
    #mkdir(1)
    #moveImages()
    #getNextEpisode(soup,browser)
    #downloadImageW(url, browser)
    #browser.close()
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
    browser.get(url)
    #Pass popup verification
    while True:
        #browser.get(url)
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
    #location = input("Enter download directory (Enter d for default): ")
    #if location == 'd':
    #    location = default
    while True:
        print("Download from: ")
        print("1. Webtoon")
        print("2. Garfield")
        print("3. Other")
        print("4. exit")
        option = int(input("Enter an option: "))
        if option == 1:
            webtoon()
        elif option == 2:
            garfield()
        elif option == 3:
            other()
        elif option == 4:
            break
        
###############################################
location = "/home/vi/Pictures/Images/"
default = "/home/vi/Pictures/Images/"
parentFolder = "#"
episodeNo = "#"
newPath = "#"
filename = "#"
comicType = 'f' # f = featured # c = challenge
comicName = "#"
titles = []
currentIndex = 0

#webtoon()
#garfield()      
main()
