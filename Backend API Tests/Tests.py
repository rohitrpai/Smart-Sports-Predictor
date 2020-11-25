import requests
from requests.auth import HTTPBasicAuth


def test_get_for_application_homepage_check_status_code_equals_200():
    try:
        response = requests.get("http://127.0.0.1:5000")
        assert response.status_code == 200
        print('Connection Successful!')
    except AssertionError as e:
        e.args += ('Received response code:', response.status_code)
        raise


def check_sign_in():
    try:
        response = requests.get('http://127.0.0.1:5000/login',
                                auth=('test', 'test'), verify=False)
        assert response.status_code == 200
        print('Sign in successful!')
    except AssertionError as e:
        print('Sign in error!')
        e.args += ('Received response code:', response.status_code)
        raise


'''def check_sign_in():
    try:
        credentials = {'username': 'test', 'password': 'aaaaa', 'check': '', 'log': 'submit'}
        response = requests.post('http://127.0.0.1:5000/login', data = credentials)
        assert response.status_code == 200
        print('Sign in successful!')
    except AssertionError as e:
        print('Sign in error!')
        e.args += ('Received response code:', response.status_code)
        raise'''


if __name__ == "__main__":
    test_get_for_application_homepage_check_status_code_equals_200()
    check_sign_in()
