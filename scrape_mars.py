# Import dependencies
import pandas as pd
import requests

from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver

## -------------------------------------------------------------------------------

# Define function to grab title and description of top news story from mars news website
def mars_news():

    # Define executable path and create a 'browser' instance
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define url, use splinter to visit the url, get the response object, and create the beautiful soup object.
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')

    # Find all the artcicle data
    all_titles = soup.find_all('div', class_='content_title')
    all_descriptions = soup.find_all('div', class_='article_teaser_body')

    # Find the top most article data
    news_title = all_titles[0].text
    news_p = all_descriptions[0].text

    # Close the browser
    browser.quit()
    
    return news_title, news_p

## -------------------------------------------------------------------------------

# Define function to grab the featured image from JPL Mars Space Images website
def featured_image():

    # Define executable path and create a 'browser' instance
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define url (base to be used in final url path calculation and mars specific for page visit),
    # use splinter to visit the url, navigate the site, get the response object, 
    # and create the beautiful soup object.
    base_url = 'https://www.jpl.nasa.gov'
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)

    featured_image_xpath = '//*[@id="full_image"]'
    browser.find_by_xpath(featured_image_xpath)[0].click()
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')

    # Find the featured image url. 
    featured_image_path = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = base_url + featured_image_path

    # Close the browser
    browser.quit()

    return featured_image_url

## -------------------------------------------------------------------------------

# Define function to grab latest Mars Weather Tweet
def mars_tweet():

    # Define executable path and create a 'browser' instance
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define url, use splinter to visit the url, get the response object, and create the beautiful soup object.
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')

    # Find the most recent tweet (i.e., the top most tweet)
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').\
                        contents[0]

    # Clean up the text by replacing \n's with spaces and removing the url at the end.
    mars_weather = mars_weather.replace('\n', ' ')

    # Close the browser
    browser.quit()
    
    return mars_weather

## -------------------------------------------------------------------------------

# Define function to grab Mars Facts Table
def mars_table():

    # Define executable path and create a 'browser' instance
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define url, use splinter to visit the url, get the response object, and create the beautiful soup object.
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    response = browser.html
    soup = BeautifulSoup(response, 'html.parser')

    # Find the table and use pandas to extract it into a dataframe.
    scraped_table = soup.find('table', id='tablepress-p-mars')
    mars_facts_dataframe = pd.read_html(str(scraped_table))[0]

    # Remove the column headers and reset the index
    mars_facts_dataframe.columns = ['label', 'information']
    mars_facts_dataframe = mars_facts_dataframe.set_index('label')

    # Convert the table to an html string
    final_table = mars_facts_dataframe.to_html()

    # Close the browser
    browser.quit()

    return final_table

## -------------------------------------------------------------------------------

# Define function to grab dictionaries of Mars Hemisphere Image URLs stored in a list

def mars_hemispheres():

    # Define executable path and create a 'browser' instance
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Define base url and mars search url, define lists for hemisphere names and for image_urls,
    # iterate through each hemisphere type to find the src of the image via beautiful soup, and populate the dictionary.
    base_url = 'https://astrogeology.usgs.gov'
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Define lists of data from which to build our image urls.
    hemispheres_list = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']
    xpath_list = ['//*[@id="product-section"]/div[2]/div[1]/a/img', '//*[@id="product-section"]/div[2]/div[2]/a/img', '//*[@id="product-section"]/div[2]/div[3]/a/img', '//*[@id="product-section"]/div[2]/div[4]/a/img']
    hemisphere_image_urls = []

    # Iteration
    for i in range(len(hemispheres_list)):
        # Visit the page and navigate using splinter
        browser.visit(mars_url)
        browser.find_by_xpath(xpath_list[i])[0].click()
        browser.find_by_xpath('//*[@id="wide-image-toggle"]')[0].click()

        # Store the response and create the beautiful soup object
        response = browser.html
        soup = BeautifulSoup(response, 'html.parser')

        # Grab the src from img tag (img_path) and build the correct url
        img_path = soup.find('img', class_='wide-image')['src']
        img_url = base_url + img_path

        # Store the dictionary entry temporarily and then append it to our list
        temp_dict = {'title': hemispheres_list[i], 'img_url': img_url}   
        hemisphere_image_urls.append(temp_dict)
    
    # Close the browser
    browser.quit()

    return hemisphere_image_urls

## -------------------------------------------------------------------------------

# Define function that combines all functions above to return a single dictionary
# with all the relevant scraped data

def scrape():
    
    # Define variables representing outputs of functions
    news_title, news_p = mars_news()
    image = featured_image()
    tweet = mars_tweet()
    table = mars_table()
    hemispheres = mars_hemispheres()
    
    # Define dictionary
    scrape_dict = {
        'article_headline': news_title,
        'article_description': news_p,
        'featured_image': image,
        'tweet': tweet,
        'table': table,
        'hemisphere_images': hemispheres
    }

    print(scrape_dict)
    return scrape_dict

scrape()