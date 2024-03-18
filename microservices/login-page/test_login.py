import requests

# Define the base URL of your Flask app
base_url = 'http://127.0.0.1:5000'

# Test case: Submitting login form without providing username and password
def test_empty_credentials():
    # Send a POST request to the login endpoint without providing any data
    response = requests.post(f'{base_url}/login')
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    # Check if the warning message is present in the response content
    assert 'Please provide username and password' in response.text

# Test case: Submitting login form with valid username and password
def test_valid_credentials():
    # Prepare the login data with valid credentials
    login_data = {'username': 'admin', 'password': 'password'}
    # Send a POST request to the login endpoint with valid data
    response = requests.post(f'{base_url}/login', data=login_data)
    # Check if the response status code is a redirection (302)
    # assert response.status_code == 302
    # Check if the response redirects to the success page
    print(response.headers)

    assert response.headers['Location'] == f'{base_url}/success'

def test_valid_credentials2():
    # Prepare the login data with valid credentials
    login_data = {'username': 'admin', 'password': 'password'}
    # Send a POST request to the login endpoint with valid data
    response = requests.post(f'{base_url}/login', data=login_data)
    # Check if the response status code is a redirection (302)
    assert response.status_code == 200  # Assuming the success page returns 200 OK
    # Check if the response URL matches the success page URL
    print(response.url)
    assert response.url == f'{base_url}/success'

# Test case: Submitting login form with invalid credentials
def test_invalid_credentials():
    # Prepare the login data with invalid credentials
    login_data = {'username': 'invalid', 'password': 'invalid'}
    # Send a POST request to the login endpoint with invalid data
    response = requests.post(f'{base_url}/login', data=login_data)
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    # Check if the warning message is present in the response content
    assert 'Invalid username and password' in response.text

# Run the test cases
if __name__ == '__main__':
    test_empty_credentials()
    test_valid_credentials2()
    test_invalid_credentials()
    print("All tests passed successfully.")
