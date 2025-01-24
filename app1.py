import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import time

# Load the trained Random Forest model
model = joblib.load('water_potability_model.pkl')

# Page config
st.set_page_config(
    page_title="Water Quality Analyzer",
    page_icon="💧",
    layout="wide"
)

# Custom CSS with modern color scheme
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    /* Title styling */
    .title {
        text-align: center;
        padding: 2rem;
        color: #48cae4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 2.5em;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px #48cae4, 0 0 10px #90e0ef, 0 0 15px #ade8f4; }
        to { text-shadow: 0 0 10px #00b4d8, 0 0 20px #0096c7, 0 0 30px #0077b6; }
    }
    
    /* Input container styling */
    .input-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Parameter card styling */
    .parameter-card {
        background: rgba(0, 180, 216, 0.1);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.7rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 180, 216, 0.2);
    }
    
    .parameter-card:hover {
        transform: translateY(-5px);
        background: rgba(0, 180, 216, 0.15);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00b4d8, #48cae4);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.2em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(45deg, #48cae4, #90e0ef);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Result box styling */
    .result-box {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Range indicator styling */
    .range-indicator {
        font-size: 0.9em;
        color: #90e0ef;
        margin-top: 0.5rem;
    }
    
    /* Light beam animation */
    .light-beam {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 200px;
        background: linear-gradient(
            to bottom,
            rgba(72, 202, 228, 0) 0%,
            rgba(72, 202, 228, 0.1) 50%,
            rgba(72, 202, 228, 0) 100%
        );
        pointer-events: none;
        z-index: -1;
        animation: moveLight 8s linear infinite;
    }
    
    @keyframes moveLight {
        0% { transform: translateY(-200px); }
        100% { transform: translateY(100vh); }
    }
    
    /* Water drops */
    .water-drop {
        position: fixed;
        pointer-events: none;
        z-index: -1;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(45deg, #48cae4, #90e0ef);
        opacity: 0.6;
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        0% { transform: translateY(-200px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(calc(100vh + 200px)); opacity: 0; }
    }
    
    /* Text colors */
    h1, h2, h3, h4 {
        color: #caf0f8;
        margin-bottom: 1rem;
    }
    
    ul {
        color: #caf0f8;
        list-style-type: none;
        padding-left: 0;
    }
    
    li {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    li:before {
        content: "•";
        position: absolute;
        left: 0;
        color: #48cae4;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #00b4d8;
    }
</style>

<div class="light-beam"></div>
<script>
    function createWaterDrops() {
        const container = document.body;
        for (let i = 0; i < 20; i++) {
            const drop = document.createElement('div');
            drop.className = 'water-drop';
            drop.style.left = Math.random() * 100 + 'vw';
            drop.style.animationDuration = (Math.random() * 2 + 1) + 's';
            drop.style.animationDelay = Math.random() + 's';
            container.appendChild(drop);
        }
    }
    
    window.addEventListener('load', createWaterDrops);
</script>
""", unsafe_allow_html=True)

# Helper function to create parameter input with scale
def parameter_input(label, key, min_val, max_val, step, normal_range, unit, help_text):
    st.markdown(f"""
        <div class="parameter-card">
            <h4>{label}</h4>
            <div class="range-indicator">
                Normal range: {normal_range} {unit}
            </div>
        </div>
    """, unsafe_allow_html=True)
    return st.number_input(
        label,
        min_value=min_val,
        max_value=max_val,
        step=step,
        help=f"{help_text}\nTypical range: {normal_range} {unit}",
        key=key
    )

# App title and description
st.markdown('<h1 class="title">💧 Water Quality Analyzer</h1>', unsafe_allow_html=True)
st.markdown("""
    <div class="input-container">
        <p style="text-align: center; font-size: 1.2em; color: #caf0f8;">
            Enter water quality parameters below to determine if the water is safe for consumption.
            The analysis is based on WHO and EPA guidelines.
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    ph = parameter_input(
        "pH Level 🧪", "ph", 0.0, 14.0, 0.1, "6.5 - 8.5", "",
        "pH indicates water's acidity or alkalinity"
    )
    
    hardness = parameter_input(
        "Hardness 🪨", "hardness", 0.0, 500.0, 0.1, "60 - 180", "mg/L",
        "Measures calcium and magnesium content"
    )
    
    solids = parameter_input(
        "Total Dissolved Solids 🔍", "solids", 0.0, 100000.0, 1.0, "500 - 1500", "mg/L",
        "Total amount of dissolved minerals"
    )
    
    chloramines = parameter_input(
        "Chloramines 🧬", "chloramines", 0.0, 10.0, 0.1, "1.0 - 4.0", "ppm",
        "Disinfectant level in water"
    )

with col2:
    sulfate = parameter_input(
        "Sulfate 🌡️", "sulfate", 0.0, 500.0, 0.1, "250 - 500", "mg/L",
        "Sulfate mineral content"
    )
    
    conductivity = parameter_input(
        "Conductivity ⚡", "conductivity", 0.0, 1000.0, 0.1, "50 - 500", "μS/cm",
        "Electrical conductivity of water"
    )
    
    organic_carbon = parameter_input(
        "Organic Carbon 🍂", "organic_carbon", 0.0, 30.0, 0.1, "2.0 - 10.0", "mg/L",
        "Amount of organic matter"
    )
    
    trihalomethanes = parameter_input(
        "Trihalomethanes 💨", "trihalomethanes", 0.0, 120.0, 0.1, "0 - 80", "μg/L",
        "Disinfection byproducts"
    )
    
    turbidity = parameter_input(
        "Turbidity 💭", "turbidity", 0.0, 10.0, 0.1, "0 - 5", "NTU",
        "Measure of water clarity"
    )

# Add parameter guide
st.markdown("""
    <div class="input-container">
        <h3>📊 Parameter Guide</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div class="parameter-card">
                <h4>pH Level</h4>
                <ul>
                    <li>< 6.5: Too acidic</li>
                    <li>6.5 - 8.5: Optimal</li>
                    <li>> 8.5: Too alkaline</li>
                </ul>
            </div>
            <div class="parameter-card">
                <h4>Hardness</h4>
                <ul>
                    <li>< 60: Soft water</li>
                    <li>60 - 180: Moderate</li>
                    <li>> 180: Hard water</li>
                </ul>
            </div>
            <div class="parameter-card">
                <h4>TDS</h4>
                <ul>
                    <li>< 500: Excellent</li>
                    <li>500 - 1500: Good</li>
                    <li>> 1500: Poor</li>
                </ul>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Analyze button
if st.button("Analyze Water Quality"):
    # Progress bar animation
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)  # Add small delay for visual effect
        progress_bar.progress(i + 1)
    
    # Prepare input features
    input_features = np.array([[
        ph, hardness, solids, chloramines, sulfate,
        conductivity, organic_carbon, trihalomethanes, turbidity
    ]])
    
    # Make prediction
    prediction = model.predict(input_features)
    probability = model.predict_proba(input_features)
    
    # Determine result styling
    if prediction[0] == 1:
        result_color = "#4CAF50"
        result_text = "Potable"
        result_emoji = "✅"
        message = "The water appears to be safe for consumption."
        bg_color = "rgba(76, 175, 80, 0.1)"
    else:
        result_color = "#f44336"
        result_text = "Not Potable"
        result_emoji = "⚠️"
        message = "The water may not be safe for consumption without treatment."
        bg_color = "rgba(244, 67, 54, 0.1)"
    
    # Display result
    st.markdown(f"""
        <div class="result-box" style="background-color: {bg_color};">
            <h2 style="color: {result_color}">Water Quality Result {result_emoji}</h2>
            <h3 style="color: #333;">
                The water is <span style="color: {result_color}; font-weight: bold">{result_text}</span>
            </h3>
            <p style="font-size: 1.2em; color: #333;">{message}</p>
            <p style="color: #666;">
                Confidence: <span style="color: {result_color}; font-weight: bold">{probability[0][prediction[0]]:.2%}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability[0][prediction[0]] * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "Prediction Confidence",
            'font': {'size': 24, 'color': '#333'}
        },
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#333"},
            'bar': {'color': result_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 50], 'color': f'{result_color}22'},
                {'range': [50, 75], 'color': f'{result_color}44'},
                {'range': [75, 100], 'color': f'{result_color}66'}
            ],
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='white',
        font={'color': "#333", 'family': "Arial"}
    )
    
    st.plotly_chart(fig)