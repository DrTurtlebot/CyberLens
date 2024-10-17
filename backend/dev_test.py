from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Test Case 001: Verify the root endpoint to ensure the server is connected and responding.
def test_connected_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"root": "true"}


# Test Case 002: Verify the unknown endpoint to ensure the server is connected and responding.
def test_unknown_endpoint():
    response = client.get("/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


# Test Case 003: Verify the getcards with a valid URL to ensure the server is connected and responding.
def test_get_cards_url():
    # Input data in the correct JSON format
    input_data = "https://www.google.com"

    response = client.post(
        "/api/getcards/request_data",
        json=str(input_data),  # Use 'json' to send the correct JSON format
    )

    # Print response status and full response body for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")  # Debugging info

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response JSON matches the expected output
    expected_response = [
        "Summary",
        "AbuseIPDB",
        "ProxyCheck",
        "VirusTotal",
        "Registrar",
        "UrlScanScreenshot",
    ]
    assert response.json() == expected_response


#   Test Case 004: Verify the getcards with a valid IP to ensure the server is connected and responding.
def test_get_cards_ip():
    # Input data in the correct JSON format
    input_data = "1.1.1.1"

    response = client.post(
        "/api/getcards/request_data",
        json=str(input_data),  # Use 'json' to send the correct JSON format
    )

    # Print response status and full response body for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")  # Debugging info

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response JSON matches the expected output

    expected_response = [
        "Summary",
        "AbuseIPDB",
        "ProxyCheck",
        "VirusTotal",
        "UrlScanScreenshot",
    ]
    assert response.json() == expected_response


# Test Case 005: Test Invalid URL
def test_invalid_url():
    # Input data in the correct JSON format
    input_data = "thisurlsuperdoesnotexistwhatsoevercauseifitdidtheniwouldbeveryveryscaredseamlessintelligence.com"

    response = client.post(
        "/api/getcards/request_data",
        json=str(input_data),  # Use 'json' to send the correct JSON format
    )

    # Print response status and full response body for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")  # Debugging info

    # Assert that the response status code is 500
    assert response.status_code == 200

    # Assert that the response JSON matches the expected output
    expected_response = ["NotRecognised"]
    assert response.json() == expected_response


# Test Case 006: Test Empty URL
def test_empty_url():
    # Input data in the correct JSON format
    input_data = ""

    response = client.post(
        "/api/getcards/request_data",
        json=str(input_data),  # Use 'json' to send the correct JSON format
    )

    # Print response status and full response body for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")  # Debugging info

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response JSON matches the expected output
    expected_response = ["NotRecognised"]
    assert response.json() == expected_response


# ============================
# /api/proxycheck Endpoint Tests
# ============================


# Test Case 007: Verify the proxycheck endpoint with a valid IP to ensure the server is connected and responding.
def test_proxycheck_ip():
    # Input data in the correct JSON format
    input_data = "1.1.1.1"
    response = client.post("/api/proxycheck/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


# Test Case 008: Verify the proxycheck endpoint with a valid URL to ensure the server is connected and responding.
def test_proxycheck_url():
    # Input data in the correct JSON format
    input_data = "http://google.com"
    response = client.post("/api/proxycheck/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


# Test Case 009: Verify the proxycheck fails with bad input
def test_proxycheck_ip_bad_input():
    # Input data in the correct JSON format
    input_data = "1.1.1.1a"
    response = client.post("/api/proxycheck/request_data", json=str(input_data))
    assert response.status_code == 500


# ============================
# /api/abuseipdb Endpoint Tests
# ============================


# Test Case 010: Verify the abuseipdb endpoint with a valid IP to ensure the server is connected and responding.
def test_abuseipdb_ip():
    # Input data in the correct JSON format
    input_data = "1.1.1.1"
    response = client.post("/api/abuseipdb/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("data") != None


# Test Case 011: Verify the abuseipdb endpoint with a valid URL to ensure the server is connected and responding.
def test_abuseipdb_url():
    # Input data in the correct JSON format
    input_data = "http://google.com"
    response = client.post("/api/abuseipdb/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("data") != None


# Test Case 012: Verify the abuseipdb fails with bad input
def test_abuseipdb_ip_bad_input():
    # Input data in the correct JSON format
    input_data = "1.1.1.1a"
    response = client.post("/api/abuseipdb/request_data", json=str(input_data))
    assert response.status_code == 500


# ============================
# /api/virustotal Endpoint Tests
# ============================


# Test Case 013: Verify the virusTotal endpoint with a valid IP to ensure the server is connected and responding.
def test_virusTotal_ip():
    # Input data in the correct JSON format
    input_data = "1.1.1.1"
    response = client.post("/api/virustotal/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("raw_input") == input_data


# Test Case 014: Verify the virusTotal endpoint with a valid URL to ensure the server is connected and responding.
def test_virusTotal_url():
    # Input data in the correct JSON format
    input_data = "http://google.com"
    response = client.post("/api/virustotal/request_data", json=str(input_data))
    assert response.status_code == 200
    assert response.json().get("raw_input") == input_data
