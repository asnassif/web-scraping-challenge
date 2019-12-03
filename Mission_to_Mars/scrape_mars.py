# from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pymongo
from selenium import webdriver
from splinter import Browser



# This is for debugging

def savetofile(contents):
    file = open('_temporary.txt',"w",encoding="utf-8")
    file.write(contents)
    file.close()


def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # NASA Mars News

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_slides = soup.find_all('li', class_='slide')

    html = browser.html
    soup = bs(html, "html.parser")

    content_title = news_slides[0].find('div', class_='content_title')
    news_title = content_title.text.strip()

    article_teaser_body = news_slides[0].find('div', class_='article_teaser_body')
    news_p = article_teaser_body.text.strip()


    # JPL Mars Space Images

    url_JPL_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # base_url = 'https://www.jpl.nasa.gov'
    # url = base_url + '/spaceimages/?search=&category=Mars'

    # Setting up splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url_JPL_images)


    browser.visit(url)
    time.sleep(2)

    # Find the more info button and click that
    # more_info_button = browser.find_link_by_partial_text('more info')
    # more_info_button.click()

    # Using BeautifulSoup create an object and parse with 'html.parser'
    html = browser.html
    img_soup = bs(html, 'html.parser')

    # find the relative image url
    img_url = img_soup.find('figure', class_='lede').find('img')['src']
    img_url

    # Use the base url to create an absolute url
    JPL_link = 'https://www.jpl.nasa.gov'
    featured_image_url = JPL_link + img_url
    featured_image_url    



    # Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'

    # Executable Path:

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    streamitems = soup.find_all('li', class_='js-stream-item stream-item stream-item')

    i = 0
    while streamitems[i].find('strong',class_='fullname').text.strip() != 'Mars Weather':
        i = i+1
        
    mars_weather = streamitems[i].find('div',class_='js-tweet-text-container')
    temp = mars_weather.find('a').text
    mars_weather = mars_weather.text
    if len(temp) > 0:
        mars_weather = mars_weather[:(len(mars_weather) - len(temp) - 1)].strip()
    mars_weather = mars_weather.replace("\n", ", ")

    # Mars facts

    url = 'https://space-facts.com/mars/'
    
    dfs = pd.read_html(url)
    for df in dfs:
        try:
            df = df.rename(columns={0:"Description", 1:"Value"})
            df = df.set_index("Description")
            marsfacts_html = df.to_html().replace('\n', '')
            # df.to_html('marsfacts.html') # to save to a file to test
            break
        except:
            continue

    # Mars Hemispheres

    base_url = 'https://astrogeology.usgs.gov'
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Products List URL

    products = soup.find_all('div', class_='item')

    urls = []
    titles = []
    for product in products:
        urls.append(base_url + product.find('a')['href'])
        titles.append(product.find('h3').text.strip())

    img_urls = []
    for combined_url in urls:
        browser.visit(combined_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        combined_url = base_url+soup.find('img',class_='wide-image')['src']
        img_urls.append(combined_url)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    # Assigning scraped data to a page
    
    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["mars_weather"] = mars_weather
    marspage["marsfacts_html"] = marsfacts_html
    marspage["hemisphere_image_urls"] = hemisphere_image_urls

    return marspage
    
