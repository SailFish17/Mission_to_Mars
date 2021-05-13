#!/usr/bin/env python
# coding: utf-8

# Mission to Mars Challenge

# Set up Dependencies and the URL executable path

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#using pandas for the .read_html() function
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ###  Visit the NASA Mars News Site
# Visit the mars nasa news site
# class url replaced - url = 'https://redplanetscience.com'
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# slide_elem has been set to hold all the data that should be searched.  
# find the data "content_title" in the slide_elem variable.
slide_elem.find('div', class_='content_title')

# Remove the HTML code comments.  
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use an f string to add the base URL to the relative url derived above to get the complete url of the pictures to be scraped.
# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# ###  Scrape Mars Data: Just the Facts Ma'am
# Pull data from table format 
# Use pandas to read the html code and set it into a dataframe.

# read the first table to be found
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()

# assign column headers
df.columns=['description', 'Mars', 'Earth']

#turn the description column into the index and maintain it without having to reassign the variable.
df.set_index('description', inplace=True)
df

df.to_html()


# ### D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# #### Hemispheres
# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html=browser.html
img_soup = soup(html, 'html.parser')

images = img_soup.find_all('img')
images

for img in images:
    img_url= img['src']
    img_title = img['alt']
    hemisphere_image_urls.append({"url":f"https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url}", "title":img_title})

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

#5 Quit the browser
browser.quit()
