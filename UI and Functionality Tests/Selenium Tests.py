import time
from selenium import webdriver


'''def test1():

    driver = webdriver.Chrome()

    driver.get("https://www.python.org")
    driver.maximize_window()
    print(driver.title)

    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)

    print(driver.current_url)
    driver.close() '''


def test_sign_in_functionality():
    driver = webdriver.Chrome()
    driver.get('C:\\Users\\rohit\\PycharmProjects\\Smart-Sports-Predictor\\Frontend\\login.html#')
    driver.maximize_window()

    username = driver.find_element_by_id("Uname")
    password = driver.find_element_by_id("Pass")
    remember_me = driver.find_element_by_id("check")
    login_button = driver.find_element_by_id("log")
    username.send_keys("test@test.com")
    password.send_keys("password")
    remember_me.click()
    login_button.click()
    time.sleep(5)

    driver.close()


def test_sign_up_functionality():
    driver = webdriver.Chrome()
    driver.get('C:\\Users\\rohit\\PycharmProjects\\Smart-Sports-Predictor\\Frontend\\registration.html#')
    driver.maximize_window()

    name = driver.find_element_by_id("Uname")
    surname = driver.find_element_by_xpath("/html/body/div/form/input[2]")
    user_name = driver.find_element_by_xpath("/html/body/div/form/input[3]")
    password = driver.find_element_by_id("Pass")
    remember_me = driver.find_element_by_id("check")
    login_button = driver.find_element_by_id("log")
    name.send_keys("test")
    surname.send_keys("run")
    user_name.send_keys("test run")
    password.send_keys("password")
    remember_me.click()
    login_button.click()
    time.sleep(5)

    driver.close()


if __name__ == "__main__":
    test_sign_in_functionality()
    test_sign_up_functionality()
