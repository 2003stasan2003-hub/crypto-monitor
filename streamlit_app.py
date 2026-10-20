import streamlit as st
import requests

st.set_page_config(page_title="CryptoMind AI: Фундаментальний Термінал", page_icon="🧠", layout="wide")

json_url = "https://raw.githubusercontent.com/2003stasan2003-hub/crypto-monitor/main/crypto_data.json"

@st.cache_data(ttl=30)
def load_data():
    try:
        res = requests.get(json_url)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return {}

data = load_data()

st.title("🧠 CryptoMind AI: Аналітичний Термінал та Прогнози")
st.markdown("---")

if data:
    # 1. Картки цін
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

    # 2. Блок комплексної аналітики (Макро, Ончейн, Сентимент)
    st.subheader("🌐 Комплексний аналіз ринку (Фонду, Кити, Сентимент)")
    
    market_intel = data.get("market_intelligence", {})
    macro = market_intel.get("macro_analysis", {})
    onchain = market_intel.get("onchain_analysis", {})
    
    # Індекс страху та жадібності
    fng_val = market_intel.get("fear_and_greed_index", 50)
    fng_label = market_intel.get("sentiment_label", "Нейтрально")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🏛️ А. Макроекономіка (ФРС та SEC)")
        st.info(
            f"📈 **Ставка ФРС:** {macro.get('fed_rate', 'Н/Д')}\n\n"
            f"📉 **Інфляція (CPI):** {macro.get('cpi_inflation', 'Н/Д')}\n\n"
            f"⚖️ **Регулятори (SEC / ETF):** {macro.get('sec_regulations', 'Н/Д')}"
        )
        
        st.markdown("### 🐋 Б. Ончейн-аналітика (Дії китів)")
        st.success(
            f"🔄 **Рух на біржах:** {onchain.get('whale_movement', 'Н/Д')}\n\n"
            f"💥 **Ліквідації:** {onchain.get('liquidations', 'Н/Д')}"
        )

    with col_b:
        st.markdown("### 🌡️ В. Сентимент натовпу")
        st.metric("Індекс страху та жадібності", f"{fng_val} / 100", fng_label)
        if fng_val <= 25:
            st.warning("⚠️ Екстремальний страх: Ринкова паніка. Ідеальна можливість для купівлі (🟢 BUY).")
        elif fng_val >= 75:
            st.error("🚨 Екстремальна жадібність: Ринок перегрітий. Час фіксувати прибуток у USDT (🔴 SELL).")
        else:
            st.info("⚖️ Помірний баланс: Сприятливі умови для зваженої торгівлі.")

        st.markdown("### 🎯 Загальний прогноз AI")
        st.markdown(
            "🟢 **Зелена зона ризику (Ріст):** Підтримується дешевшими грошима ФРС та відтоком монет китами з бірж.\n\n"
            "🔴 **Червона зона ризику (Падіння):** Активується при зростанні інфляції або досягненні екстремальної жадібності."
        )

    st.markdown("---")

    # 3. Інтерактивний дайджест новин по днях
    st.subheader("📰 Драйвери та новини по днях тижня")
    news_dict = data.get("news_by_day", {})
    selected_day = st.selectbox("Оберіть день для детального аналізу:", list(news_dict.keys()))
    
    if selected_day in news_dict:
        day_info = news_dict[selected_day]
        st.markdown(f"### 📅 День: {selected_day}")
        st.markdown(f"**📌 Подія:** {day_info.get('title')}")
        st.markdown(f"**📂 Категорія:** {day_info.get('category')}")
        st.markdown(f"**⚖️ Вплив:** {day_info.get('impact')}")
        st.markdown(f"**📊 Аналіз українською:** {day_info.get('analysis')}")

else:
    st.error("Помилка завантаження даних із GitHub.")
