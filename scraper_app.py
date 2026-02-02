import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import fetch_screener_data, validate_screener_url, convert_to_csv, convert_to_json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Screener.in Web Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .fetch-btn>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .csv-btn>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .json-btn>button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        font-size: 3rem;
        font-weight: 800;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #11998e15 0%, #38ef7d15 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #11998e;
        margin: 1rem 0;
    }
    .error-box {
        background: linear-gradient(135deg, #eb334915 0%, #f4524515 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #eb3349;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🔍 Screener.in Web Scraper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem; margin-top: -1rem;'>Extract stock screening data with ease</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'url' not in st.session_state:
    st.session_state.url = ''
if 'fetched' not in st.session_state:
    st.session_state.fetched = False

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Screener.in URL")
    
    # URL input with example
    url_input = st.text_input(
        "Paste your screener.in link here:",
        value=st.session_state.url,
        placeholder="https://www.screener.in/screens/2448025/sales-profit-20-eps-up/",
        help="Enter a valid screener.in URL to fetch stock data"
    )
    
    # Example URLs
    with st.expander("📌 Example URLs"):
        st.markdown("""
        - **Sales & Profit Growth**: `https://www.screener.in/screens/2448025/sales-profit-20-eps-up/`
        - **High ROE**: `https://www.screener.in/screens/71064/high-roe/`
        - **Low Debt**: `https://www.screener.in/screens/71063/low-debt/`
        """)

with col2:
    st.markdown("### 📊 Quick Stats")
    if st.session_state.fetched and st.session_state.data is not None:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.data)}</div>
            <div class="metric-label">Total Records</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.data.columns)}</div>
            <div class="metric-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <p style='margin: 0; color: #666;'>📥 No data fetched yet. Enter a URL and click "Fetch Data".</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Action buttons
st.markdown("### 🎯 Actions")
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    st.markdown('<div class="fetch-btn">', unsafe_allow_html=True)
    fetch_button = st.button("🚀 Fetch Data", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn2:
    st.markdown('<div class="csv-btn">', unsafe_allow_html=True)
    csv_button = st.button("📄 Download CSV", use_container_width=True, disabled=not st.session_state.fetched)
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn3:
    st.markdown('<div class="json-btn">', unsafe_allow_html=True)
    json_button = st.button("📋 Download JSON", use_container_width=True, disabled=not st.session_state.fetched)
    st.markdown('</div>', unsafe_allow_html=True)

# Handle Fetch Data button
if fetch_button:
    if not url_input:
        st.markdown("""
        <div class="error-box">
            <p style='margin: 0;'><strong>⚠️ Error:</strong> Please enter a URL first.</p>
        </div>
        """, unsafe_allow_html=True)
    elif not validate_screener_url(url_input):
        st.markdown("""
        <div class="error-box">
            <p style='margin: 0;'><strong>⚠️ Error:</strong> Please enter a valid screener.in URL.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("🔄 Fetching data from screener.in... This may take a few moments."):
            try:
                # Fetch the data
                data = fetch_screener_data(url_input)
                
                # Store in session state
                st.session_state.data = data
                st.session_state.url = url_input
                st.session_state.fetched = True
                
                st.markdown(f"""
                <div class="success-box">
                    <p style='margin: 0;'><strong>✅ Success!</strong> Fetched {len(data)} records with {len(data.columns)} columns.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.rerun()
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <p style='margin: 0;'><strong>❌ Error:</strong> {str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

# Handle CSV Download button
if csv_button and st.session_state.fetched:
    try:
        csv_data = convert_to_csv(st.session_state.data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screener_data_{timestamp}.csv"
        
        st.download_button(
            label="⬇️ Click to Download CSV",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("""
        <div class="success-box">
            <p style='margin: 0;'>✅ CSV file ready for download!</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <p style='margin: 0;'><strong>❌ Error:</strong> Failed to convert to CSV: {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

# Handle JSON Download button
if json_button and st.session_state.fetched:
    try:
        json_data = convert_to_json(st.session_state.data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screener_data_{timestamp}.json"
        
        st.download_button(
            label="⬇️ Click to Download JSON",
            data=json_data,
            file_name=filename,
            mime="application/json",
            use_container_width=True
        )
        
        st.markdown("""
        <div class="success-box">
            <p style='margin: 0;'>✅ JSON file ready for download!</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <p style='margin: 0;'><strong>❌ Error:</strong> Failed to convert to JSON: {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

# Display data preview
if st.session_state.fetched and st.session_state.data is not None:
    st.markdown("---")
    st.markdown("### 📊 Data Preview")
    
    # Display options
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        show_rows = st.slider("Number of rows to display:", 5, 100, 10)
    with col_opt2:
        st.markdown(f"**Total Rows:** {len(st.session_state.data)}")
    
    # Display the dataframe
    st.dataframe(
        st.session_state.data.head(show_rows),
        use_container_width=True,
        height=400
    )
    
    # Column information
    with st.expander("📋 Column Information"):
        col_info = pd.DataFrame({
            'Column Name': st.session_state.data.columns,
            'Data Type': st.session_state.data.dtypes.values,
            'Non-Null Count': st.session_state.data.count().values
        })
        st.dataframe(col_info, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with ❤️ using Streamlit and Pandas</p>
        <p>Screener.in Web Scraper v1.0 | ⚠️ Please use responsibly and respect screener.in's terms of service</p>
    </div>
""", unsafe_allow_html=True)
