import json
import requests

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url).json()
        data = {
            "btc": {
                "price": response.get("bitcoin", {}).get("usd", 0),
                "change": response.get("bitcoin", {}).get("usd_24h_change", 0)
            },
            "eth": {
                "price": response.get("ethereum", {}).get("usd", 0),
                "change": response.get("ethereum", {}).get("usd_24h_change", 0)
            },
            "sol": {
                "price": response.get("solana", {}).get("usd", 0),
                "change": response.get("solana", {}).get("usd_24h_change", 0)
            },
            "sentiment": "БИЧАЧИЙ (Bullish)",
            "risk": "Середній",
            "news": [
                {"time": "10:15", "title": "SEC схвалила новий Ethereum-ETF та розширила рамки ліцензування", "impact": "Позитивний"},
                {"time": "09:50", "title": "Нові заяви ФРС США про можливе зниження інфляції до кінця року", "impact": "Нейтральний"},
                {"time": "09:00", "title": "Ескалація політичних ризиків у регіоні видобутку енергоресурсів", "impact": "Негативний"}
            ]
        }

        with open("crypto_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Дані успішно оновлено!")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    fetch_crypto_data()
