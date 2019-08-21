from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium.common import exceptions
from urllib.error import HTTPError
import os
import csv
import time

bing = 'https://www.bing.com/'
aid = 1
class Image:
    def __init__(self,id,img):
        self.id = id
        self.img = img
class LinkImages:
    def __init__(self, image, titulo, selfLink):
        self.image = image
        self.titulo = titulo
        self.link = selfLink
    
def makeQuerry(search):
    listQ = list(search)
    querry = ''
    for word in listQ:
        if word == ' ':
            word = '+'
        elif word == ',':
            word = '%2C'
        elif word == '?':
            word = '%3F'
        querry += word
    return querry
def imageSave(imagesrc):
    fullpath = os.getcwd()
    imageName = imagesrc.split('/')[-1]
    imgPath = os.path.join(fullpath+'\\img', str(aid)+imageName)
    try:
        urlretrieve(imagesrc,imgPath)
    except (HTTPError, ValueError) as e:
        print(e)
    return imageName
    
def getLinkAndImage(a):
    global aid
    linkImages= []
    driver.get('{}{}'.format(bing, a.attrs['href']))
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div/ul/li[5]/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[3]/div/div/div').click()
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//div[@class="action  insbt pic nofocus"]').click()
    except exceptions.NoSuchElementException:
        print(':v')
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    listLinks = bs.find('div', {'id':'pagesIncl'}).find('ul').find_all('li')
    imageInfor = bs.find('div', {'class':'mainImage current'})
    imagesrc = imageSave(imageInfor.find('img').attrs['src'])
    image = Image(aid, imagesrc.split('/')[-1])
    aid +=1
    print('----------------------------------------------------------------------------------------------------------')
    print(aid, imageInfor.find('img').attrs['src'].split('/')[-1])
    print('----------------------------------------------------------------------------------------------------------')
    for links in listLinks:
        titulo = links.find('div', {'class':'pritext'}).get_text()
        selfLink = links.find('div', {'class':'domain'}).get_text()
        print(titulo)
        print(selfLink)
        linkImages.append(LinkImages(image,titulo, selfLink))
    return image, linkImages

def extractAll(bs):
    divImage = bs.find_all('div', {'class':'imgpt'})
    foundLinks = []
    foundImages = []
    limit = 0
    for div in divImage:
        if limit <= 14:    
            result = getLinkAndImage(div.find('a'))
            foundImages.append(result[0])
            foundLinks.append(result[1])
            limit += 1
        else:
            return foundImages, foundLinks

search = input('Pesquisar : ')
print('limite de 14 imgs por motivos éticos')

querry = makeQuerry(search)
driver = webdriver.Firefox()
driver.get('{}images/search?q={}'.format(bing, querry))
bs = BeautifulSoup(driver.page_source, 'html.parser')
images, linkdelas = extractAll(bs)
linkqebomnada = []
driver.close()
driver.quit()
if os.path.exists('geckodriver.log'):
    os.remove('geckodriver.log')
for listlinks in linkdelas:
    for link in listlinks:
        linkqebomnada.append(link)
#saving images
csvImages = open('images.csv', 'w', encoding='utf-8',newline='')
write = csv.writer(csvImages, quoting=csv.QUOTE_ALL)
classFields = (','.join(images[0].__dict__.keys())+',\n').split(',')
write.writerow(classFields)
try:
    for image in images:
        if image.id == '':
            pass
        write.writerow([image.id, image.img, '\n'])
finally:
    csvImages.close()
#Saving links
csvLinks = open('links.csv', 'w', encoding='utf-8',newline='')
write = csv.writer(csvLinks, quoting=csv.QUOTE_ALL)
classFields = (','.join(linkqebomnada[0].__dict__.keys())+',\n').split(',')
write.writerow(classFields)
for link in linkqebomnada:
    if link.image.id == '':
        pass
    write.writerow([link.image.id, link.titulo, link.link, '\n'])
csvLinks.close()

