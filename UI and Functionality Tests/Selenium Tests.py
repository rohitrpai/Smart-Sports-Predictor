import time
from selenium import webdriver


def test_sign_in_functionality():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000')
    driver.maximize_window()

    go_to_login = driver.find_element_by_css_selector("body > div.signin > a.loginbuttons2")
    go_to_login.click()
    time.sleep(2)

    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    remember_me = driver.find_element_by_id("check")
    login_button = driver.find_element_by_name("log")
    username.send_keys("test")
    password.send_keys("test")
    remember_me.click()
    login_button.click()
    time.sleep(3)

    msg = driver.find_element_by_css_selector("body > div.container > div.row > div > div > div.msg")
    assert msg.is_displayed()

    driver.close()


def test_sign_up_fails_for_existing_user():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000/register')
    driver.maximize_window()

    lastname = driver.find_element_by_id("lastname")
    firstname = driver.find_element_by_id("firstname")
    user_name = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    email_id= driver.find_element_by_id("email")
    finish_reg = driver.find_element_by_name("log")
    lastname.send_keys("test")
    firstname.send_keys("test")
    user_name.send_keys("test")
    password.send_keys("test")
    email_id.send_keys("test")
    finish_reg.click()
    time.sleep(2)

    msg = driver.find_element_by_css_selector("#login > div")
    assert msg.is_displayed()

    driver.quit()


if __name__ == "__main__":
    #test_sign_in_functionality()
    test_sign_up_fails_for_existing_user()
