import requests


def test_get_for_application_homepage_check_status_code_equals_200():
    try:
        response = requests.get("http://127.0.0.1:5000")
        assert response.status_code == 200
        print('test_get_for_application_homepage_check_status_code_equals_200 - Pass')
    except AssertionError as e:
        e.args += ('test_get_for_application_homepage_check_status_code_equals_200 - Fail. Received response code:', response.status_code)
        raise


def check_signin_with_valid_credentials_success():
    try:
        credentials = {'username': 'test', 'password': 'test'}
        session = requests.Session()
        response = session.post('http://127.0.0.1:5000/login', data=credentials)
        assert response.status_code == 200
        print('check_signin_with_valid_credentials_success - Pass')
    except AssertionError as e:
        e.args += ('check_signin_with_valid_credentials_success - Fail. Received response code:', response.status_code)
        raise


def check_signin_with_empty_password_fails():
    try:
        credentials = {'username': 'test', 'password': ''}
        session = requests.Session()
        response = session.post('http://127.0.0.1:5000/login', data=credentials)
        assert response.status_code == 401
        print('check_signin_with_empty_password_fails - Pass')
    except AssertionError as e:
        e.args += ('check_signin_with_empty_password_fails - Fail. Received response code:', response.status_code)
        raise


def check_signin_with_empty_username_fails():
    try:
        credentials = {'username': '', 'password': 'test'}
        session = requests.Session()
        response = session.post('http://127.0.0.1:5000/login', data=credentials)
        assert response.status_code == 401
        print('check_signin_with_empty_username_fails - Pass')
    except AssertionError as e:
        e.args += ('check_signin_with_empty_username_fails - Fail. Received response code:', response.status_code)
        raise


def check_signin_with_empty_credentials_fails():
    try:
        credentials = {'username': '', 'password': ''}
        session = requests.Session()
        response = session.post('http://127.0.0.1:5000/login', data=credentials)
        assert response.status_code == 401
        print('check_signin_with_empty_credentials_fails - Pass')
    except AssertionError as e:
        e.args += ('check_signin_with_empty_credentials_fails - Fail. Received response code:', response.status_code)
        raise


if __name__ == "__main__":
    test_get_for_application_homepage_check_status_code_equals_200()
    check_signin_with_valid_credentials_success()
    check_signin_with_empty_password_fails()
    check_signin_with_empty_username_fails()
    check_signin_with_empty_credentials_fails()
