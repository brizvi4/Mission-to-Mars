# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Set up Splinter
def scrape_all():
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" : hemisphere(browser),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def hemisphere(browser):

    url='https://marshemispheres.com/'

    browser.visit(url)

    hemisphere_image_urls = []

    imgs_links= browser.find_by_css("a.product-item h3")

    for i in range(4):
        
        hemispheres={}

        # Find elements going to click link 
        browser.find_by_css("a.product-item h3")[i].click()

        element = browser.find_link_by_text('Sample').first
        
        title = browser.find_by_css("h2.title").text
        
        img_url = element['href']
        
        hemispheres["img_url"] = img_url
        
        hemispheres["title"] = title
        
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()
        
    return hemisphere_image_urls

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

        

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None    
    
    return news_title, news_paragraph

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    try:

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# ## Mars Facts
def mars_facts():

    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)


    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())





