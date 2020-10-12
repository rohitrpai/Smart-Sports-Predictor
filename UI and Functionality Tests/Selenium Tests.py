from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def test1():

    driver = webdriver.Chrome('C:\\bin\chromedriver')

    driver.get("https://www.python.org")
    driver.maximize_window()
    print(driver.title)

    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)

    print(driver.current_url)
    driver.close()


if __name__ == "__main__":
    test1()
