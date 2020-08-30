from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask_pymongo import PyMongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C://Users/linda/OneDrive/Desktop/Working Files/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #Latest Mars News from NASA
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,"html.parser")
    section=soup.find(class_='item_list')
    link=section.find('a')
    href=link['href']
    title=section.find(class_="content_title")
    link=title.find('a')
    #article title
    news_title=link.text.strip()
    #teaser paragraph
    news_p=section.find(class_='article_teaser_body').text.strip()

    #JPL Mars Space feature image
    base_url="https://www.jpl.nasa.gov"
    search_url="/spaceimages/?search=&category=Mars"
    browser.visit(base_url+search_url)
    html=browser.html
    soup=bs(html,"html.parser")
    link=soup.find(class_='button fancybox')['data-fancybox-href']
    #featured image link
    featured_image_url=base_url+link

    # Mars space facts table
    url="https://space-facts.com/mars/"
    browser.visit(url)
    tables = pd.read_html(url)[0]
    tables.columns = ['Stat', 'Mars']
    tables.set_index('Stat', inplace=True)
    mars_table=tables.to_html(classes="table table-striped")

    #Hemisphere photos
    base_url="https://astrogeology.usgs.gov"
    search_url="/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(base_url+search_url)
    html=browser.html
    soup=bs(html,"html.parser")
    body=soup.find('body')
    n=len(body.find_all(class_='item'))
    hemisphere_image_urls=[]
    hem_name=[]
    hem_links=[]
    for x in range(n):
        img_link=soup.find_all(class_='description')[x]('a')[0]['href']
        img_url=base_url+img_link+'.tif'
    
        name=soup.find_all(class_='description')[x]('a')[0]('h3')[0].text.strip()
        dict={'title':name,'img_url':img_url}
        hemisphere_image_urls.append(dict)


    #combine in one dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feat_image": featured_image_url,
        "facts_table":mars_table,
        "hemi_images":hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
