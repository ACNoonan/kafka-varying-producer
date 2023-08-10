import requests

# Base URL of your Flask application
BASE_URL = "http://0.0.0.0:5000"

# Function to change the frequency to 1,000
def set_frequency_to_1000():
    frequency = 1000
    response = requests.post(f"{BASE_URL}/set_frequency", json={'frequency': frequency})
    if response.status_code == 200:
        print(f"Frequency successfully set to {frequency}")
    else:
        print(f"Failed to set frequency: {response.text}")

# Function to change the frequency to 10
def set_frequency_to_10():
    frequency = 10
    response = requests.post(f"{BASE_URL}/set_frequency", json={'frequency': frequency})
    if response.status_code == 200:
        print(f"Frequency successfully set to {frequency}")
    else:
        print(f"Failed to set frequency: {response.text}")

# Example usage
if __name__ == "__main__":
    set_frequency_to_1000()
    #set_frequency_to_10()
