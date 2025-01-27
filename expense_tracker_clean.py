import streamlit as st
import pandas as pd
import os
import openai
from openai import AzureOpenAI
import csv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import requests
import plotly.express as px
import pandas as pd
import openai
from openai import AzureOpenAI
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime, timedelta

os.environ["AZURE_OPENAI_KEY"] = "cb1c33772b3c4edab77db69ae18c9a43"

openai_client = AzureOpenAI(
    azure_endpoint="https://testaisentiment.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)
os.environ["AZURE_OPENAI_KEY"] = "cb1c33772b3c4edab77db69ae18c9a43"

openai_client = AzureOpenAI(
    azure_endpoint="https://testaisentiment.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

azure_endpoint = "https://avatarpoc.cognitiveservices.azure.com/"
azure_key = "3cb3ae2e45644aff905e88491d89a2ee"
credential = AzureKeyCredential(azure_key)
text_analytics_client = TextAnalyticsClient(endpoint=azure_endpoint, credential=credential)

# Azure Text Analytics authentication
def authenticate_client():
    ta_credential = AzureKeyCredential(azure_key)
    text_analytics_client = TextAnalyticsClient(endpoint=azure_endpoint, credential=ta_credential)
    return text_analytics_client

azure_client = authenticate_client()

# Set up API keys
os.environ["AZURE_OPENAI_KEY"] = "cb1c33772b3c4edab77db69ae18c9a43"  # Replace with your Azure OpenAI key
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
google_api_key = "AIzaSyCRHbWFgUuSIjOm3CgHNKq6Q8RLMKXjlKU"  # Replace with your Google Places API key
azure_openai_endpoint = "https://testaisentiment.openai.azure.com/"  # Replace with your Azure OpenAI endpoint

# Azure Text Analytics setup
azure_text_analytics_endpoint = "https://avatarpoc.cognitiveservices.azure.com/"  # Replace with your endpoint
azure_text_analytics_key = "3cb3ae2e45644aff905e88491d89a2ee"  # Replace with your Azure Text Analytics Key
azure_credential = AzureKeyCredential(azure_text_analytics_key)
text_analytics_client = TextAnalyticsClient(endpoint=azure_text_analytics_endpoint, credential=azure_credential)


# Initialize the expenses list
expenses = []

# Load expenses from file
def load_expenses(file_path):
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])  # Convert amount to float
                expenses.append(row)

# Function to fetch news updates using Azure OpenAI
def fetch_news_updates():
    prompt = "Provide the latest financial and technology news headlines as a running ticker."
    try:
        response = openai_client.chat.completions.create(
            model="aipocexploration",
            messages=[
                {"role": "system", "content": "You are an AI assistant providing news updates."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return "⚠China's new AI model that rivals OpenAI, Google, Microsoft is taking the internet by storm"
		
# Save expenses to file
def save_expenses(file_path):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# Function to fetch nearby restaurants using Google Places API
def get_nearby_restaurants(location, cuisine, radius=50000):  # Radius set to 50 km
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,  # Format: "latitude,longitude"
        "radius": radius,  # Radius in meters
        "type": "restaurant",
        "keyword": cuisine,
        "key": google_api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

# Function to analyze and recommend using ChatGPT
def get_chatgpt_recommendation(restaurants, budget):
    message_text = [
        {"role": "system", "content": "You are an expert in financial advice and restaurant recommendations."},
        {"role": "user", "content": f"Here is a list of restaurants: {restaurants}. Recommend the best restaurant within a budget of {budget} euros, considering ratings and price level."}
    ]
    try:
        response = openai_client.chat.completions.create(
            model="aipocexploration",  # Use the model you’ve deployed in Azure OpenAI
            messages=message_text,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Function to fetch transportation options using Google Directions API
def get_transport_recommendation(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    modes = ["driving", "walking", "bicycling", "transit"]
    recommendations = []

    for mode in modes:
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "key": google_api_key,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                duration = route["legs"][0]["duration"]["text"]
                distance = route["legs"][0]["distance"]["text"]
                recommendations.append({"mode": mode, "duration": duration, "distance": distance})

    return recommendations
# Azure OpenAI: Summarize Text
# Azure OpenAI: Financial Insights
def get_financial_insights():
    insights = """
    1. **Create a Budget**: Track your monthly expenses and categorize them. Use apps like FinEd.
    2. **Emergency Fund**: Save 3-6 months' worth of expenses for emergencies.
    3. **Invest Wisely**: Explore index funds, ETFs, or real estate for long-term returns.
    4. **Cut Unnecessary Costs**: Cancel unused subscriptions and reduce discretionary spending.
    5. **Take Advantage of Cashback and Discounts**: Use credit cards with cashback rewards.
    6. **Articles to Explore**:
        - [10 Ways to Save Money](https://www.nerdwallet.com/article/finance/how-to-save-money)
        - [Beginner’s Guide to Investing](https://www.investopedia.com/articles/basics/06/invest1000.asp)
    """
    return insights

def get_openai_summary(text):
    message_text = [
        {"role": "system", "content": "You are an AI assistant providing financial advice."},
        {"role": "user", "content": f"Summarize the following text: {text}"}
    ]
    try:
        completion = requests.post(
            f"{azure_openai_endpoint}openai/deployments/aipocexploration/chat/completions?api-version=2024-02-15-preview",
            headers={"Content-Type": "application/json", "api-key": os.getenv("AZURE_OPENAI_KEY")},
            json={"messages": message_text, "max_tokens": 150}
        )
        completion.raise_for_status()
        return completion.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.set_page_config(page_title="Expense Tracker & Restaurant Finder", layout="wide")
# Running text banner for news updates
news_updates = fetch_news_updates()
st.markdown(
    f"""
    <div style='background-color: #004c99; color: white; padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
        <marquee>{news_updates}</marquee>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("💸 Personal Expense Tracker & 🍽️ Restaurant Finder")

# Tabs for navigation
#tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Overview", "➕ Add Expense", "📊 Visualize", "🤖 Insights", "🍽️ Restaurant Finder"])
# Tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview", "➕ Add Expense", "📊 Visualize", "🤖 Insights", "🍽️ Restaurant Finder", "🚗 Transport Finder"
])

file_path = 'expenses.csv'
load_expenses(file_path)

with tab1:
    st.header("Overview")
    if expenses:
        df = pd.DataFrame(expenses)
        df['amount'] = df['amount'].astype(float)
        total_expenses = df['amount'].sum()
        st.metric("Total Expenses", f"${total_expenses:.2f}")
        st.dataframe(df)
        st.subheader("Spending by Category")
        category_chart = px.pie(df, names='category', values='amount', title="Spending Distribution")
        st.plotly_chart(category_chart)
    else:
        st.write("No expenses recorded yet. Add some in the next tab!")

with tab2:
    st.header("Add Expense")
    with st.form("add_expense_form"):
        date = st.text_input("Date (YYYY-MM-DD)")
        category = st.selectbox("Category", ["Food", "Travel", "Entertainment", "Others"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if date and category and description:
                expense = {'date': date, 'category': category, 'amount': amount, 'description': description}
                expenses.append(expense)
                save_expenses(file_path)
                st.success("Expense added successfully!")
            else:
                st.error("Please fill in all fields.")

with tab3:
    st.header("Visualize Expenses")
    if expenses:
        df = pd.DataFrame(expenses)
        df['amount'] = df['amount'].astype(float)
        st.subheader("Spending Over Time")
        time_chart = px.line(df, x='date', y='amount', title="Spending Over Time")
        st.plotly_chart(time_chart)
        st.subheader("Spending by Category")
        bar_chart = px.bar(df, x='category', y='amount', color='category', title="Spending by Category")
        st.plotly_chart(bar_chart)
    else:
        st.write("No expenses to visualize.")

# Insights Tab
with tab4:
    st.header("Get Insights")
    st.subheader("💡 Financial Tips and Recommendations")
    insights = get_financial_insights()
    st.write(insights)

with tab5:
    st.header("Restaurant Finder")
    st.sidebar.header("Enter Your Preferences")
    location = st.sidebar.text_input("Enter your location (latitude,longitude)", "53.349805,-6.26031")  # Default: Dublin
    cuisine = st.sidebar.selectbox("Preferred cuisine", ["Italian", "Indian", "Chinese", "Mexican", "Other"])
    budget = st.sidebar.number_input("Enter your budget (in euros)", min_value=0.0, step=0.5)
    radius = st.sidebar.slider("Search radius (meters)", 500, 50000, 50000)  # Radius default set to 50 km

    if st.sidebar.button("Find Restaurants"):
        with st.spinner("Finding the best restaurants for you..."):
            restaurants = get_nearby_restaurants(location, cuisine, radius)
            if not restaurants:
                st.error("No restaurants found. Try increasing the radius or changing the cuisine.")
            else:
                restaurant_list = [
                    {"name": r["name"], "rating": r.get("rating", "N/A"), "price_level": r.get("price_level", "N/A"), "address": r.get("vicinity", "N/A")}
                    for r in restaurants
                ]
                recommendation = get_chatgpt_recommendation(restaurant_list, budget)
                st.success("Here is our recommendation:")
                st.write(recommendation)

                st.subheader("Nearby Restaurants")
                for r in restaurant_list:
                    st.write(f"**{r['name']}**")
                    st.write(f"- Rating: {r['rating']}")
                    st.write(f"- Price Level: {r['price_level']}")
                    st.write(f"- Address: {r['address']}")
                    st.write("---")
# Transport Finder Tab
with tab6:
    st.header("Transport Finder")
    origin = st.text_input("Enter the origin (e.g., Dublin 1)", "Dublin 1")
    destination = st.text_input("Enter the destination (e.g., Dublin 4)", "Dublin 4")
    if st.button("Find Best Transport"):
        with st.spinner("Fetching the best transport options..."):
            recommendations = get_transport_recommendation(origin, destination)
            if recommendations:
                st.subheader("Transport Recommendations")
                for rec in recommendations:
                    st.write(f"**Mode**: {rec['mode'].capitalize()}")
                    st.write(f"- Duration: {rec['duration']}")
                    st.write(f"- Distance: {rec['distance']}")
                    st.write("---")
            else:
                st.error("Could not fetch transport recommendations. Check the locations.")
