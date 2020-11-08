import requests

def test_get_for_application_homepage_check_status_code_equals_200():
    response = requests.get("https://google.com")
    assert response.status_code == 200

if __name__ == "__main__":
    test_get_for_application_homepage_check_status_code_equals_200()