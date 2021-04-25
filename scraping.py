# Mission to Mars
# 10.3.3 Scrape Mars Data:

# set up dependencies 
# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
#using pandas for the .read_html() function
import pandas as pd
import datetime as dt

# Scrape all function to automatically run the other functions below.
def scrape_all():

# Initiate headless driver for deployment
    # this is the old Splinter set up and the URL executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# for automation, make the 3 sets of code all functions
# function to scrape news sites.
def mars_news(browser):

    # Visit the mars nasa news site
    # Not sure why this is changed in 10.5.3 url = 'https://redplanetscience.com'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up the HTML parser 
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # slide_elem has been set to hold all the data that should be searched.  
        # find the data "content_title" in the slide_elem variable.
        # not sure why I don't need this now: slide_elem.find('div', class_='content_title')


        # Remove the HTML code comments.  
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p

    except AttributeError:
        return None, None

    return news_title, news_p

# Mod_10.3.4  Scrape Mars Data:
# ## JPL Space Images Featured Images

# function to scrape images
def featured_image(browser):

    # Visit URL
    #url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # chain some indexing at the end of .find to stipulate the 2nd button (remember(0,1,2)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the newly opened page
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try/except for error handling
    try:

        # Find the relative url of the image.  its relative as the image will change with each new story.  the returned URL is only for the image, not the site.
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None
    
    # Use an f string to add the base URL to the relative url derived above to get the complete url of the pictures to be scraped.
    # Use the base URL to create an absolute URL
    # img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# 10.3.5 Scrape Mars Data: Just the facts Ma'am
# Pull data from table format 

# function to grab facts
def mars_facts():

#add a try/except for error handling.
    try:
    # read the first table to be found
        # old url? df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # assign column headers
    df.columns=['description', 'Mars', 'Earth']

    #turn the description column into the index and maintain it without having to reassign the variable.
    df.set_index('description', inplace=True)

    # convert dataframe into html, add bootstrap
    # return df.to_html()
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

# If running as script, print scraped data
    print(scrape_all())   


