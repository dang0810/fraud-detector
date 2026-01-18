import streamlit as st
import pandas as pd
import io
from src.detector import TransactionDetector

# Page config
st.set_page_config(
    page_title="Fraud Detector",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF4B4B, #FF8C8C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #3d3d5c;
    }
    .flagged-row {
        background-color: rgba(255, 75, 75, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🔍 Transaction Fraud Detector</p>', unsafe_allow_html=True)
st.markdown("**Analyze transactions to detect suspicious activities using rule-based detection.**")

# Sidebar
st.sidebar.header("⚙️ Configuration")
threshold = st.sidebar.slider(
    "Amount Threshold ($)",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=500,
    help="Transactions above this amount will be flagged"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Detection Rules")
st.sidebar.markdown("""
1. **High Amount** - Above threshold
2. **Unusual Country** - Not CA/US
3. **High Frequency** - < 60s apart
""")

# Main content
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "📁 Upload Transaction CSV",
    type=['csv'],
    help="CSV must contain: user_id, amount, country, time"
)

# Use sample data option
use_sample = st.checkbox("Use sample data instead", value=uploaded_file is None)

if use_sample or uploaded_file is not None:
    # Load data
    if use_sample:
        # Create sample data
        sample_data = {
            'user_id': [101, 102, 101, 103, 104, 105],
            'amount': [200, 7000, 50, 300, 15000, 450],
            'country': ['CA', 'CA', 'UK', 'US', 'US', 'RU'],
            'time': [
                '2026-01-18 10:00:00', '2026-01-18 10:05:00',
                '2026-01-18 10:00:45', '2026-01-18 11:00:00',
                '2026-01-18 12:00:00', '2026-01-18 13:00:00'
            ]
        }
        df = pd.DataFrame(sample_data)
        # Save to temp file for detector
        temp_path = "temp_transactions.csv"
        df.to_csv(temp_path, index=False)
        data_path = temp_path
        st.info("📊 Using sample data with 6 transactions")
    else:
        # Save uploaded file
        temp_path = "temp_uploaded.csv"
        df = pd.read_csv(uploaded_file)
        df.to_csv(temp_path, index=False)
        data_path = temp_path
        st.success(f"✅ Loaded {len(df)} transactions from uploaded file")
    
    # Run detection
    if st.button("🔍 Analyze Transactions", type="primary", use_container_width=True):
        with st.spinner("Analyzing..."):
            detector = TransactionDetector(data_path, threshold=threshold)
            detector.load_data()
            flagged = detector.detect_fraud()
            
            # Store results in session state
            st.session_state['flagged'] = flagged
            st.session_state['all_data'] = detector.df
            st.session_state['analyzed'] = True

    # Display results
    if st.session_state.get('analyzed', False):
        flagged = st.session_state['flagged']
        all_data = st.session_state['all_data']
        
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_transactions = len(all_data)
        flagged_count = len(flagged)
        flagged_rate = (flagged_count / total_transactions * 100) if total_transactions > 0 else 0
        total_flagged_amount = flagged['amount'].sum() if len(flagged) > 0 else 0
        
        with col1:
            st.metric("Total Transactions", total_transactions)
        with col2:
            st.metric("Flagged", flagged_count, delta=None)
        with col3:
            st.metric("Flag Rate", f"{flagged_rate:.1f}%")
        with col4:
            st.metric("Flagged Amount", f"${total_flagged_amount:,.0f}")
        
        st.markdown("---")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("##### 🥧 Transaction Status")
            status_data = pd.DataFrame({
                'Status': ['Normal', 'Flagged'],
                'Count': [total_transactions - flagged_count, flagged_count]
            })
            st.bar_chart(status_data.set_index('Status'))
        
        with col_chart2:
            st.markdown("##### 📈 Flagged by Reason")
            if len(flagged) > 0:
                reasons = []
                for reason in flagged['reason']:
                    if 'High Amount' in reason:
                        reasons.append('High Amount')
                    if 'Unusual Country' in reason:
                        reasons.append('Unusual Country')
                    if 'High Frequency' in reason:
                        reasons.append('High Frequency')
                
                reason_counts = pd.Series(reasons).value_counts()
                st.bar_chart(reason_counts)
            else:
                st.info("No flagged transactions")
        
        st.markdown("---")
        
        # Flagged transactions table
        st.subheader("🚨 Flagged Transactions")
        if len(flagged) > 0:
            display_df = flagged[['user_id', 'amount', 'country', 'time', 'reason']].copy()
            display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No suspicious transactions detected!")
        
        # All transactions
        with st.expander("📋 View All Transactions"):
            st.dataframe(all_data, use_container_width=True, hide_index=True)

else:
    st.info("👆 Upload a CSV file or check 'Use sample data' to get started")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "Built with Streamlit • "
    "<a href='https://github.com/dang0810/fraud-detector' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
