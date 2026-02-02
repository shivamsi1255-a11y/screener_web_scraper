# 🔍 Screener.in Web Scraper

A beautiful and powerful web scraping application for **screener.in** built with Python and Streamlit. Extract stock screening data, preview it in real-time, and download it in CSV or JSON format with just a few clicks!

---

## ✨ Features

* **🔗 URL Input**: Paste any screener.in URL
* **🚀 One-Click Fetch**: Automatically scrapes all pages
* **📊 Live Preview**: Interactive table preview
* **📄 CSV Export**: Download data in CSV format
* **📋 JSON Export**: Download data in JSON format
* **🎨 Beautiful UI**: Modern, gradient-based design
* **⚡ Fast & Efficient**: Automatic pagination handling
* **🛡️ Error Handling**: Robust validation and messages

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

1. **Double-click** `setup.bat`

   * Creates a virtual environment
   * Installs all dependencies

2. **Double-click** `run_scraper.bat`

3. Open your browser at:

   ```
   http://localhost:8501
   ```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper application
streamlit run scraper_app.py
```

---

## 📖 How to Use

### Step 1: Enter URL

Paste a screener.in URL, for example:

```
https://www.screener.in/screens/2448025/sales-profit-20-eps-up/
```

### Step 2: Fetch Data

Click **🚀 Fetch Data**. The app will:

* Fetch all pages
* Combine data
* Display total records

### Step 3: Preview Data

* Interactive table view
* Adjustable rows
* Column information

### Step 4: Download

* **📄 CSV Download**
* **📋 JSON Download**

Files are auto-named with timestamps.

---

## 📁 Project Structure

```
screener_scap/
│
├── scraper_app.py         # Main Streamlit application
├── scraper.py             # Web scraping logic
├── app.py                 # Neural network app (separate)
├── neural_network.py      # Neural network implementation
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── SCRAPER_README.md      # Scraper-specific documentation
├── setup.bat              # Setup script
├── run_scraper.bat        # Run scraper app
└── run.bat                # Run neural network app
```

---

## 🎯 Example URLs

* **Sales & Profit Growth (20% EPS Up)**

  ```
  https://www.screener.in/screens/2448025/sales-profit-20-eps-up/
  ```

* **High ROE Stocks**

  ```
  https://www.screener.in/screens/71064/high-roe/
  ```

* **Low Debt Companies**

  ```
  https://www.screener.in/screens/71063/low-debt/
  ```

---

## 🔧 Technical Details

### Dependencies

```
streamlit==1.29.0
pandas==2.0.3
beautifulsoup4==4.12.2
lxml==4.9.3
html5lib==1.1
python-dotenv==1.0.0
```

### How It Works

1. Validates screener.in URL
2. Iterates through pages automatically
3. Extracts tables using `pandas.read_html()`
4. Cleans and merges data
5. Exports CSV or JSON

### Key Functions

* `fetch_screener_data(link)`
* `validate_screener_url(url)`
* `convert_to_csv(df)`
* `convert_to_json(df)`

---

## 🎨 UI Highlights

* Gradient action buttons
* Responsive layout
* Live stats (rows & columns)
* Loading indicators
* Styled error/success messages

---

## ⚙️ Configuration

Edit `.env`:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_THEME_BASE=light
```

---

## 🛡️ Error Handling

Handles:

* Empty or invalid URLs
* Network issues
* Parsing failures
* Export errors

---

## 📊 Data Formats

### CSV

```csv
S.No.,Name,CMP,P/E,Market Cap,Div Yld %,...
1,Company A,1234.5,25.3,50000,1.2,...
```

### JSON

```json
[
  {"S.No.": "1", "Name": "Company A", "CMP": "1234.5"}
]
```

---

## ⚠️ Important Notes

1. 3-second delay between pages (rate limiting)
2. Respect screener.in Terms of Service
3. Intended for personal research
4. Verify data from official sources

---

## 🔄 Future Improvements

* Custom delay settings
* Progress bar
* Data filters
* Excel export
* Scheduled scraping
* Data comparison

---

## 🐛 Troubleshooting

| Issue         | Solution                          |
| ------------- | --------------------------------- |
| Import errors | `pip install -r requirements.txt` |
| Port in use   | Change port or free 8501          |
| Timeout       | Check internet                    |
| No data       | Verify URL                        |

Enable debug:

```env
LOG_LEVEL=DEBUG
```

---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

* Streamlit
* Pandas
* BeautifulSoup4
* Data source: Screener.in

---

## 🤝 Contributing

Contributions welcome:

* Bug reports
* Feature requests
* Pull requests
* Documentation improvements

---

**Happy Scraping! 🚀**

Use responsibly and respect website terms.
