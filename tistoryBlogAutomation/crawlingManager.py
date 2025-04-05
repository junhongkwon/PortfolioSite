import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_util import init_browser


def crawlingheadlinePost(browser_):

    contents = []

    headline_a = WebDriverWait(browser_, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#wp--skip-link--target > div.wp-block-group.alignfull.top-hero-package.has-green-500-background-color.has-background.is-layout-constrained.wp-container-core-group-is-layout-4.wp-block-group-is-layout-constrained > div > div.hero-package-2__featured > div > div > div > h3 > a"))
    )
    headline_href = headline_a.get_attribute("href")
    browser_.get(headline_href)

    headline_h1 = WebDriverWait(browser_, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#wp-site-blocks > div.seamless-scroll-container.wp-block-techcrunch-seamless-scroll-container > div.article-hero.article-hero--image-and-text.has-green-500-background-color.wp-block-techcrunch-article-hero > div.article-hero__second-section > div.article-hero__content > div.article-hero__middle > h1"))
    )

    headline_ps = WebDriverWait(browser_, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.entry-content > p"))
    )
    contents.append(headline_h1.text)
    for p in (headline_ps):
        contents.append(p.text)

    return contents

def runCrawlingManager():

    browser = init_browser("https://techcrunch.com/")
    contents_result = crawlingheadlinePost(browser)
    browser.quit()
    return contents_result

