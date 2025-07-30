import requests

def main():
    client_id = "5NqenMt8idHP6EJZTPJtQA"
    client_secret = "Zi-FEpICK9ZA9JAXTw_TCDAYW8H0bw"

    headers = {
        "User-Agent": "ai_econ_data_scraper_simple/1.0 by ai_eco_data_man11"
    }

    data = {
        "grant_type": "client_credentials"
    }

    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(client_id, client_secret),
        data=data,
        headers=headers
    )

    print("Status:", r.status_code)
    print("Response:", r.text)

main()