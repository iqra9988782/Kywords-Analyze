import streamlit as st
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from textblob import TextBlob
import plotly.express as px

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def clean_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    return tokens

def get_keyword_suggestions(keyword):
    # Simulate keyword suggestions (in real app, you'd use an API)
    base_words = ["online", "best", "buy", "cheap", "review", "tutorial", "guide", "top"]
    suggestions = [f"{keyword} {word}" for word in base_words]
    return suggestions

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def calculate_keyword_metrics(keyword):
    # Simulate keyword metrics (in real app, you'd use an API)
    import random
    return {
        "monthly_volume": random.randint(1000, 50000),
        "competition": random.uniform(0.1, 1.0),
        "difficulty": random.uniform(1, 100),
        "cpc": round(random.uniform(0.5, 5.0), 2)
    }

def main():
    st.set_page_config(page_title="Advanced Keyword Analyzer", layout="wide")
    
    st.title("🔍 Advanced Keyword Analyzer")
    
    # Sidebar for history
    with st.sidebar:
        st.header("Search History")
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.success("History cleared!")
        
        for item in st.session_state.history:
            st.text(f"• {item}")
    
    # Main input
    keyword = st.text_input("Enter your keyword:", key="keyword_input")
    
    if st.button("Analyze"):
        if keyword:
            # Add to history
            if keyword not in st.session_state.history:
                st.session_state.history.append(keyword)
            
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)
            
            # Get and display metrics
            metrics = calculate_keyword_metrics(keyword)
            
            col1.metric("Monthly Volume", f"{metrics['monthly_volume']:,}")
            col2.metric("Competition", f"{metrics['competition']:.2f}")
            col3.metric("Difficulty", f"{metrics['difficulty']:.1f}")
            col4.metric("CPC", f"${metrics['cpc']}")
            
            # Keyword suggestions
            st.subheader("Keyword Suggestions")
            suggestions = get_keyword_suggestions(keyword)
            
            # Create a DataFrame for suggestions with metrics
            suggestions_data = []
            for sugg in suggestions:
                metrics = calculate_keyword_metrics(sugg)
                suggestions_data.append({
                    "Keyword": sugg,
                    "Monthly Volume": metrics["monthly_volume"],
                    "Competition": metrics["competition"],
                    "Difficulty": metrics["difficulty"],
                    "CPC": metrics["cpc"]
                })
            
            df_suggestions = pd.DataFrame(suggestions_data)
            
            # Display suggestions in an interactive table
            st.dataframe(
                df_suggestions.style.background_gradient(subset=["Monthly Volume"], cmap="Blues"),
                use_container_width=True
            )
            
            # Visualization
            st.subheader("Volume vs Competition Analysis")
            fig = px.scatter(
                df_suggestions,
                x="Competition",
                y="Monthly Volume",
                size="CPC",
                color="Difficulty",
                hover_data=["Keyword"],
                title="Keyword Analysis Matrix"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Export options
            st.download_button(
                label="Download Analysis (CSV)",
                data=df_suggestions.to_csv(index=False),
                file_name=f"keyword_analysis_{keyword}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
