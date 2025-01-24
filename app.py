import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

# Load the trained Random Forest model
model = joblib.load('water_potability_model.pkl')

# Page config
st.set_page_config(
    page_title="Water Quality Analyzer",
    page_icon="💧",
    layout="wide"
)

# Custom CSS with animations
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    /* Title styling */
    .title {
        text-align: center;
        padding: 2rem;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 2.5em;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #0073e6;
        }
        to {
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #0073e6;
        }
    }
    
    /* Input container styling */
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Parameter card styling */
    .parameter-card {
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .parameter-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
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
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.1) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        pointer-events: none;
        z-index: -1;
        animation: moveLight 8s linear infinite;
    }
    
    @keyframes moveLight {
        0% {
            transform: translateY(-200px);
        }
        100% {
            transform: translateY(100vh);
        }
    }
    
    /* Water drops animation */
    .water-drop {
        position: fixed;
        pointer-events: none;
        z-index: -1;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        0% { transform: translateY(-200px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(calc(100vh + 200px)); opacity: 0; }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Result box styling */
    .result-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Range indicator styling */
    .range-indicator {
        font-size: 0.8em;
        color: #a8c7ff;
        margin-top: 0.3rem;
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
    
    function createLightBeam() {
        const beam = document.createElement('div');
        beam.className = 'light-beam';
        document.body.appendChild(beam);
    }
    
    // Create effects when the page loads
    window.addEventListener('load', () => {
        createWaterDrops();
        createLightBeam();
    });
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
        <p style="text-align: center; font-size: 1.2em;">
            Enter water quality parameters below to determine if the water is safe for consumption.
            The analysis is based on WHO and EPA guidelines.
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    ph = parameter_input(
        "pH Level 🧪",
        "ph",
        0.0, 14.0, 0.1,
        "6.5 - 8.5",
        "",
        "pH indicates water's acidity or alkalinity. 7 is neutral."
    )
    
    hardness = parameter_input(
        "Hardness 🪨",
        "hardness",
        0.0, 500.0, 0.1,
        "60 - 180",
        "mg/L",
        "Measures calcium and magnesium content"
    )
    
    solids = parameter_input(
        "Total Dissolved Solids 🔍",
        "solids",
        0.0, 100000.0, 1.0,
        "500 - 1500",
        "mg/L",
        "Total amount of dissolved minerals"
    )
    
    chloramines = parameter_input(
        "Chloramines 🧬",
        "chloramines",
        0.0, 10.0, 0.1,
        "1.0 - 4.0",
        "ppm",
        "Disinfectant level in water"
    )

with col2:
    sulfate = parameter_input(
        "Sulfate 🌡️",
        "sulfate",
        0.0, 500.0, 0.1,
        "250 - 500",
        "mg/L",
        "Sulfate mineral content"
    )
    
    conductivity = parameter_input(
        "Conductivity ⚡",
        "conductivity",
        0.0, 1000.0, 0.1,
        "50 - 500",
        "μS/cm",
        "Electrical conductivity of water"
    )
    
    organic_carbon = parameter_input(
        "Organic Carbon 🍂",
        "organic_carbon",
        0.0, 30.0, 0.1,
        "2.0 - 10.0",
        "mg/L",
        "Amount of organic matter"
    )
    
    trihalomethanes = parameter_input(
        "Trihalomethanes 💨",
        "trihalomethanes",
        0.0, 120.0, 0.1,
        "0 - 80",
        "μg/L",
        "Disinfection byproducts"
    )
    
    turbidity = parameter_input(
        "Turbidity 💭",
        "turbidity",
        0.0, 10.0, 0.1,
        "0 - 5",
        "NTU",
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
    else:
        result_color = "#f44336"
        result_text = "Not Potable"
        result_emoji = "⚠️"
        message = "The water may not be safe for consumption without treatment."
    
    # Display result
    st.markdown(f"""
        <div class="result-box" style="border: 2px solid {result_color} background-color: blue">
            <h2 style="color: {result_color}">Water Quality Result {result_emoji}</h2>
            <h3>The water is <span style="color: {result_color}; font-weight: bold">{result_text}</span></h3>
            <p style="font-size: 1.1em;">{message}</p>
            <p>Confidence: {probability[0][prediction[0]]:.2%}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability[0][prediction[0]] * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Prediction Confidence", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': result_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'lightgray'},
                {'range': [50, 75], 'color': 'gray'},
                {'range': [75, 100], 'color': 'darkgray'}
            ],
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig)