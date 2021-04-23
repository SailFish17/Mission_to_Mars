# Mission to Mars
# 10.3.3 Scrape Mars Data:

# set up dependencies and the URL executable path
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#using pandas for the .read_html() function
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser 
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

# Mod_10.3.4  Scrape Mars Data:
# ## JPL Space Images Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# chain some indexing at the end of .find to stipulate the 2nd button (remember(0,1,2)
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the newly opened page
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative url of the image.  its relative as the image will change with each new story.  the returned URL is only for the image, not the site.
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use an f string to add the base URL to the relative url derived above to get the complete url of the pictures to be scraped.
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# 10.3.5 Scrape Mars Data: Just the facts Ma'am
# Pull data from table format 
# read the first table to be found
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# assign column headers
df.columns=['description', 'Mars', 'Earth']

#turn the description column into the index and maintain it without having to reassign the variable.
df.set_index('description', inplace=True)
df
df.to_html()

browser.quit()


