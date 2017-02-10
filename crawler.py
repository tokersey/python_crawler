import sys
import re
import mechanize
from bs4 import BeautifulSoup


def crawler(argv):
    """
        Crawler to login to an account and grab some urls
    """

    username = argv[0]
    password = argv[1]
    user_id = argv[2]
    login_url = "https://github.com/login"
    page_url = "https://github.com/%s" % user_id

    # Create browser
    browser = mechanize.Browser(factory=mechanize.RobustFactory())

    # set options
    browser.set_handle_robots(False)
    browser.set_handle_refresh(False)

    login(browser, username, password, login_url)
    response = navigate(browser, page_url)
    get_elements(response, user_id)


def login(browser, username="", password="", login_url=""):
    """
        Login using mechanize

        Docs: http://wwwsearch.sourceforge.net/mechanize/development.html
    """

    # Open login page
    browser.open(login_url)

    # get the first form and use is to fill in the credentials
    # could also use browser.form(name="") or browser.form(id="")
    browser.form = list(browser.forms())[0]

    browser.form["login"] = username
    browser.form["password"] = password
    browser.submit()


def navigate(browser, url):
    """ Navigate to the given url """

    browser.open(url)

    return browser.response()

    # html = browser.response().readlines()

    # Print Formatted HTML response
    # print browser.response().read()


def get_elements(response, user_id):
    """
        Get links from webpage using BeautifulSoup

        Docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    """
    soup = BeautifulSoup(response.read(), "html.parser")

    # body_tag = soup.body

    # Print out page title to see what we get
    # print soup.title

    # Loop through all the links to output each one
    # for link in soup.find_all('a'):
        # print link.get('href')

    # print all links starting with a particular string
    for link in soup.findAll('a', attrs={'href': re.compile("^/%s" % user_id)}):
        print link.get('href')

if __name__ == "__main__":
    crawler(sys.argv[1:])
