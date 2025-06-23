import streamlit as st
import time
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
from streamlit_lottie import st_lottie

# App Config
st.set_page_config(page_title="AI in Walmart Supply Chain", layout="wide")

# Page Navigation
PAGES = [
    "Intro", "Inventory Management", "Fulfillment Centers", "Transportation & Logistics",
    "Last-Mile Delivery", "Sustainability & Cost Efficiency", "Conclusion"
]

selected_page = st.sidebar.radio("Navigate", PAGES)

# Load Lottie Animations
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie Animation URLs
animations = {
    "intro": load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_zrqthn6o.json"),
    "inventory": load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json"),
    "fulfillment": load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json" ),
    "transport": load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_j1adxtyb.json"),
    "lastmile": load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_puciaact.json"),
    "sustainability": load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_4kx2q32n.json")
}

# Page: Intro
if selected_page == "Intro":
    st.title("🚀 AI Innovations Transforming Walmart’s Retail Supply Chain")
    st_lottie(animations["intro"], height=300)
    st.write("""
        Welcome to a visual walkthrough of how Walmart is leveraging Artificial Intelligence to optimize every step of its supply chain—from inventory to delivery.

        In this presentation, we’ll explore how AI helps Walmart reduce waste, automate warehouses, and deliver faster—all while cutting costs and boosting sustainability.
    """)

# Page: Inventory Management
elif selected_page == "Inventory Management":
    st.title("📦 Inventory Management with AI")
    st_lottie(animations["inventory"], height=300)
    st.subheader("AI-Driven Demand Forecasting")
    st.write("""
        Machine learning models at Walmart analyze real-time sales, seasonal trends, and weather to forecast demand accurately. 
        This enables automated replenishment—avoiding both overstocking and stockouts.
    """)
    st.subheader("Inventory Anomaly Detection")
    st.write("""
        AI scans for irregularities such as missing inventory (due to theft or scanning errors) using computer vision and RFID/IoT sensors, allowing for real-time alerts.
    """)
    st.info("Result: Better accuracy, lower waste, and cost savings on unsold goods.")

# Page: Fulfillment Centers
elif selected_page == "Fulfillment Centers":
    st.title("🏭 AI in Fulfillment Centers")
    st_lottie(animations["fulfillment"], height=300)
    st.subheader("Dynamic Slotting & Layout Optimization")
    st.write("AI decides optimal placement of items inside warehouses, reducing picker travel time.")
    st.subheader("Computer Vision & Robotic Picking")
    st.write("Autonomous robots and AI vision systems ensure high-speed, accurate picking and packaging.")
    st.subheader("Predictive Equipment Maintenance")
    st.write("AI uses IoT sensors to monitor forklifts, conveyors, and predicts breakdowns in advance.")
    st.success("Boosts warehouse productivity while reducing downtime and errors.")

# Page: Transportation & Logistics
elif selected_page == "Transportation & Logistics":
    st.title("🚚 Transportation & Logistics")
    st_lottie(animations["transport"], height=300)
    st.subheader("AI Route Optimization")
    st.write("Real-time traffic, weather, and delivery windows are used by AI to find the most efficient delivery routes.")
    st.subheader("Dynamic Scheduling")
    st.write("Delivery loads and driver assignments are adjusted live for efficiency.")
    st.subheader("Predictive Fleet Maintenance")
    st.write("Telematics and engine sensors help AI anticipate failures before they happen.")
    st.subheader("Autonomous Middle-Mile Vehicles")
    st.write("Walmart uses self-driving vehicles to reduce costs and extend operational hours.")
    st.success("AI helps Walmart move faster, cheaper, and safer.")

# Page: Last-Mile Delivery
elif selected_page == "Last-Mile Delivery":
    st.title("🤖 Last-Mile Delivery")
    st_lottie(animations["lastmile"], height=300)
    st.subheader("Drones & Delivery Robots")
    st.write("AI-powered drones and bots are used to deliver groceries within 30 minutes in some areas.")
    st.subheader("Personalized Scheduling")
    st.write("AI learns from customer preferences to optimize delivery windows and reroute as needed.")
    st.info("Outcome: Faster delivery, more convenience, and reduced cost per delivery.")

# Page: Sustainability & Cost Efficiency
elif selected_page == "Sustainability & Cost Efficiency":
    st.title("🌍 Sustainability & Cost Efficiency")
    st_lottie(animations["sustainability"], height=300)
    st.subheader("Carbon Emission Tracking & Optimization")
    st.write("AI tools suggest greener routes and monitor fuel usage to reduce environmental impact.")
    st.subheader("Warehouse Energy Management")
    st.write("Smart sensors adjust lighting/heating in real-time to save electricity.")
    st.subheader("Waste Reduction")
    st.write("AI forecasting has helped Walmart save $86M by minimizing overstock and spoilage.")
    st.success("A greener, leaner, and more efficient supply chain.")

# Page: Conclusion
elif selected_page == "Conclusion":
    st.title("🎯 Conclusion")
    st_lottie(animations["intro"], height=250)
    st.write("""
        Walmart’s AI-powered supply chain is a blueprint for the future—smart, responsive, and sustainable. 
        From inventory to last-mile, AI ensures operations are accurate, fast, and cost-effective.
    """)
    st.balloons()
    st.success("Thank you for watching and exploring this with us! 🎉")