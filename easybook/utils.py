import requests

def send_user_to_inventory(email, full_name, reference):
    url = "https://inventory.example.com/api/users/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_SECRET_API_TOKEN"  # If required
    }

    data = {
        "full_name": full_name,
        "email": email,
        "ref": reference
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print("Error sending user to inventory:", e)
        return False
