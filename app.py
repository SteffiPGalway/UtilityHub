from tasks.portfolio_generator import github_repos, generate_portfolio_html
from tasks.currency_converter import convert_currency
from tasks.youtube_audio import download_youtube_video
from tasks.translate_text import translate_text
from tasks.stockprice import get_stock_price
from tasks.merge_pdf import merge_pdfs
from tasks.weather import get_weather
from dotenv import load_dotenv
import streamlit as st
import asyncio
import os

load_dotenv()

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard")

# Create columns for tiles
col1, col2, col3 = st.columns(3)

# ----- TILE 1: Stock Price Predictor -----
with col1:
    with st.container():
        st.markdown("### 📈 Stock Price Predictor")
        st.caption("Get the latest stock closing price.")

        ticker = st.text_input("Stock Ticker (e.g. AAPL, TSLA, MSFT)", key="stock_ticker")

        if st.button("Get Stock Price"):
            if ticker.strip():
                try:
                    price_series = get_stock_price(ticker)
                    latest_price = price_series.iloc[-1]  # last available close
                    st.metric(
                        label=f"{ticker} Latest Closing Price",
                        value=f"${latest_price:.2f}",
                        delta=f"${latest_price - price_series.iloc[-2]:.2f}" if len(price_series) > 1 else "N/A"
                        )
                except Exception as e:
                    st.error(f"Error fetching stock price: {e}")
            else:
                st.warning("Please enter a stock ticker.")

# ----- TILE 2: YouTube Downloader -----
with col2:
    st.title("🎬 YouTube Downloader")
    yt_url = st.text_input("Paste YouTube URL here:")

    # Optional: checkbox for audio-only download
    audio_only = st.checkbox("Audio only (MP3)")

    if st.button("Download"):
        if yt_url.strip():
            # Attempt download
            filepath = download_youtube_video(
                yt_url,
                output_path="downloads",
                filename="video.mp4" if not audio_only else "audio.mp3",
                audio_only=audio_only
            )

            if filepath:
                # Provide download button
                with open(filepath, "rb") as f:
                    st.download_button(
                        label=f"⬇ Download {'Audio' if audio_only else 'Video'}",
                        data=f,
                        file_name=os.path.basename(filepath),
                        mime="audio/mpeg" if audio_only else "video/mp4"
                    )
                st.success("✅ Download completed successfully!")
            else:
                st.error("❌ Download failed. YouTube may be blocking this request on Streamlit Cloud.")
        else:
            st.warning("Please enter a valid YouTube URL.")

# ----- TILE 3: Weather Update -----
with col3:
    with st.container():
        st.markdown("### 🌤️ Weather Update")
        st.caption("Check the weather for any city.")

        # Input text to enter city
        city_name = st.text_input("City")

        # Weather button
        if st.button("Get Weather"):
            if city_name.strip():
                api_key = os.environ.get('OPEN_WEATHER_MAP_API_KEY')
                if not api_key:
                    st.error("API key not found!")
                else:
                    try:
                        temp, weather_description, humidity = get_weather(api_key, city_name)  # Correct argument order
                        st.metric("Temperature (°C)", temp)
                        st.metric("Humidity", f"{humidity}%")
                        st.write(f"Condition: {weather_description.capitalize()}")
                    except Exception as e:
                        st.error(f"Error fetching weather: {e}")
            else:
                st.warning("Please enter a city name.")

col4, col5, col6 = st.columns(3)

# ----- TILE 4: Portfolio Generator -----
with col4:
    st.subheader("💼 Portfolio Generator")
    st.text("Generate a simple portfolio from your GitHub repos.")

    github_user = st.text_input("GitHub Username", key="github_user")

    if st.button("Generate Portfolio"):
        if github_user.strip():
            try:
                repos = github_repos(github_user)
                if repos:
                    output_file = generate_portfolio_html(github_user, repos)
                    with open(output_file, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    st.markdown(html_content, unsafe_allow_html=True)

                    with open(output_file, "rb") as f:
                        st.download_button(
                            "⬇ Download Portfolio HTML",
                            f,
                            file_name="portfolio.html",
                            mime="text/html"
                        )
                else:
                    st.warning("No repositories found for this user.")
            except Exception as e:
                st.error(f"Error generating portfolio: {e}")
        else:
            st.warning("Please enter a GitHub username.")

# ----- TILE 5: Stock Price Scraper -----
with col5:
    st.subheader("📊 Stock Price Scraper")
    st.text("Scrape stock prices for multiple symbols.")

    stock_symbols = st.text_input("Enter stock symbols (comma-separated)", key="stock_symbols")

    if st.button("Scrape Prices"):
        if stock_symbols.strip():
            symbols = [s.strip().upper() for s in stock_symbols.split(",") if s.strip()]
            if symbols:
                try:
                    from tasks.stock_scraper import scrape_stock_prices  # Import here to avoid circular import
                    output_path, df = scrape_stock_prices(symbols)
                    st.success(f"✅ Stock prices scraped successfully! Saved to {output_path}")
                    st.dataframe(df)

                    with open(output_path, "r", encoding="utf-8") as f:
                        csv_data = f.read()
                    st.download_button(
                        "⬇ Download CSV",
                        csv_data,
                        file_name="stocks.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error scraping stock prices: {e}")
            else:
                st.warning("Please enter valid stock symbols.")
        else:
            st.warning("Please enter some stock symbols.")

col7, col8, col9 = st.columns(3)

# ----- TILE 7: Language Translation -----
with col7:
    with st.container():
        st.markdown("### 🌐 Language Translation")
        st.caption("Translate text between different languages.")
    
        input_text = st.text_area("Enter text to translate", height=150)
        target_lang = st.selectbox("Select target language", ["en", "fr", "es", "de"])

        # Translate button
        if st.button("Translate"):
            if input_text.strip():
            # Run the async translation function
                try:
                    translated = asyncio.run(translate_text(input_text, target_lang))
                    st.success(f"Translated text: {translated.text}")  # googletrans result has .text
                except Exception as e:
                    st.error(f"Translation failed: {e}")
            else:
                st.warning("Please enter some text before translating.")

# ----- TILE 8: Currency Converter ----- 
with col8: 
    with st.container(): 
        st.markdown("### 💱 Currency Converter")
        st.caption("Convert an amount between currencies.") 

        amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="amount") 
        from_currency = st.text_input("From Currency (e.g. USD)", key="from_currency") 
        to_currency = st.text_input("To Currency (e.g. EUR)", key="to_currency") 
        if st.button("Convert", key="convert_btn"): 
            try: 
                result = convert_currency(amount, from_currency, to_currency) 
                st.success(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}") 
            except Exception as e: 
                st.error("⚠️ Currency service is temporarily unavailable. Please try again later.")

col10, col11, col12 = st.columns(3)

# ----- TILE 10: PDF Merge -----
with col10:
    with st.container():
        st.markdown("### 📄 Merge PDFs")
        st.caption("Upload two or more PDF files to merge them.")

        num_pdfs = st.number_input(
            "How many PDF files do you want to upload?", 
            min_value=2, 
            step=1, 
            key="merge_count"
            )

        pdf_list = []
        for i in range(num_pdfs):
            uploaded_file = st.file_uploader(
                f"Upload PDF file {i+1}", 
                type=["pdf"], 
                key=f"pdf_{i}"
                )
            if uploaded_file is not None:
                pdf_list.append(uploaded_file)

     # Add a submit button
        if st.button("Merge PDFs"):
            if len(pdf_list) == num_pdfs:
                output_path = "merged.pdf"
                merge_pdfs(pdf_list, output=output_path)
                st.success("✅ PDFs merged successfully!")

                with open(output_path, "rb") as f:
                    st.download_button(
                        "⬇ Download merged PDF",
                        f,
                        file_name="merged.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("⚠ Please upload all PDF files before merging.")
