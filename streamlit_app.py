import streamlit as st
import requests

# Налаштування сторінки
st.set_page_config(page_title="CryptoMind AI Terminal", page_icon="📈", layout="wide")

# Завантаження даних із вашого JSON на GitHub
json_url = "https://raw.githubusercontent.com/2003stasan2003-hub/crypto-monitor/main/crypto_data.json"

@st.cache_data(ttl=60)
def load_data():
    try:
        res = requests.get(json_url)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return {}

data = load_data()

st.title("📈 CryptoMind AI: Мобільний Термінал")
st.markdown("---")

if data:
    # Блок карток цін
    col1, col2, col3, col4 = st.columns(4)
    
    btc = data.get("btc", {})
    eth = data.get("eth", {})
    sol = data.get("sol", {})
    usdt = data.get("usdt", {})

    with col1:
        st.metric("Bitcoin (BTC)", f"${btc.get('price', 0):,.2f}", f"{btc.get('change', 0):+.2f}%")
    with col2:
        st.metric("Ethereum (ETH)", f"${eth.get('price', 0):,.2f}", f"{eth.get('change', 0):+.2f}%")
    with col3:
        st.metric("Solana (SOL)", f"${sol.get('price', 0):,.2f}", f"{sol.get('change', 0):+.2f}%")
    with col4:
        st.metric("Tether (USDT)", f"${usdt.get('price', 0):,.4f}", f"{usdt.get('change', 0):+.2f}%")

    st.markdown("---")

    # Блок AI-Аналітики
    st.subheader("🧠 Глобальна AI-аналітика та прогноз")
    st.info(
        "🟢 **ЗЕЛЕНА ЗОНА РИЗИКУ (BUY):** Сприятливий фон, низька інфляція, приплив у спотові ETF. Час купувати та накопичувати.\n\n"
        "🔴 **ЧЕРВОНА ЗОНА РИЗИКУ (SELL):** Зона перегріву, фіксація прибутку китами, ризик корекції. Час виводити в USDT."
    )

    st.markdown("---")

    # Стрічка новин по днях
    st.subheader("📰 Інтерактивний дайджест новин та драйверів")
    news_dict = data.get("news_by_day", {})
    
    selected_day = st.selectbox("Оберіть день тижня для перегляду новин:", list(news_dict.keys()))
    
    if selected_day in news_dict:
        day_info = news_dict[selected_day]
        st.markdown(f"### 📅 День: {selected_day}")
        st.markdown(f"**📌 Драйвер / Подія:** {day_info.get('title')}")
        st.markdown(f"**📂 Категорія:** {day_info.get('category')}")
        st.markdown(f"**⚖️ Вплив:** {day_info.get('impact')}")
        st.markdown(f"**📊 Аналіз причин:** {day_info.get('analysis')}")

    st.markdown("---")
    
    # Мобільний конвертер валют у USDT
    st.subheader("🧮 Конвертер валют у USDT")
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        coin = st.selectbox("Оберіть монету", ["BTC", "ETH", "SOL", "USDT"])
        amount = st.number_input("Кількість", value=1.0)
    with c_col2:
        prices_map = {"BTC": btc.get('price', 0), "ETH": eth.get('price', 0), "SOL": sol.get('price', 0), "USDT": 1.0}
        total_usdt = amount * prices_map.get(coin, 0)
        st.metric("Результат конвертації", f"${total_usdt:,.2f} USDT")

else:
    st.error("Не вдалося завантажити дані з GitHub. Перевірте посилання або структуру JSON.")
