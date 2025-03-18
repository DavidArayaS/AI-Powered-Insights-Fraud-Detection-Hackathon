def format_response(data):
    return f"Response: {data}"

def handle_api_request(url, params):
    import requests
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def aggregate_results(results):
    return sum(results) if results else 0