import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Load the trained Random Forest model
model = joblib.load('water_potability_model.pkl')

# Page config
st.set_page_config(
    page_title="Water Quality Analyzer",
    page_icon="💧",
    layout="wide"
)

# Custom CSS with modern styling and animations
st.markdown("""
<style>
    /* Color variables */
    :root {
        --primary-dark: #1a237e;
        --primary: #3949ab;
        --primary-light: #7986cb;
        --accent: #00acc1;
        --success: #4caf50;
        --warning: #ff9800;
        --danger: #f44336;
        --background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        --text-light: #ffffff;
        --text-dark: #263238;
    }

    /* Main container */
    .main {
        background: var(--background);
        color: var(--text-light);
        min-height: 100vh;
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
        from { text-shadow: 0 0 5px #fff, 0 0 10px var(--primary-light); }
        to { text-shadow: 0 0 10px #fff, 0 0 20px var(--primary-light); }
    }

    /* Input container styling */
    .input-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Parameter card styling */
    .parameter-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .parameter-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        border-color: var(--accent);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary), var(--accent));
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, var(--accent), var(--primary));
    }

    /* Analysis grid styling */
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }

    .analysis-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .analysis-card:hover {
        transform: translateY(-5px);
    }

    /* Meter styling */
    .meter {
        height: 10px;
        background: #e0e0e0;
        border-radius: 5px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .meter-value {
        height: 100%;
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 5px;
        transition: width 1s ease-in-out;
    }

    /* Range indicator */
    .range-indicator {
        font-size: 0.8em;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.3rem;
    }

    /* Water drop animation */
    .water-drop {
        position: fixed;
        pointer-events: none;
        z-index: -1;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.2));
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.3));
        animation: fall linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-100vh) scale(0); opacity: 0; }
        50% { transform: translateY(0) scale(1); opacity: 1; }
        100% { transform: translateY(100vh) scale(0.5); opacity: 0; }
    }
</style>
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
        "pH indicates water's acidity or alkalinity"
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
    
    # Create detailed analysis
    st.markdown("""
        <div class="analysis-grid">
            <div class="analysis-card">
                <h3>pH Analysis</h3>
                <div class="meter">
                    <div class="meter-value" style="width: {}%"></div>
                </div>
                <p>{}</p>
            </div>
            <div class="analysis-card">
                <h3>Mineral Content</h3>
                <div class="meter">
                    <div class="meter-value" style="width: {}%"></div>
                </div>
                <p>{}</p>
            </div>
            <div class="analysis-card">
                <h3>Contamination Risk</h3>
                <div class="meter">
                    <div class="meter-value" style="width: {}%"></div>
                </div>
                <p>{}</p>
            </div>
        </div>
    """.format(
        min(100, max(0, (ph - 6.5) / (8.5 - 6.5) * 100)),
        "Optimal pH level" if 6.5 <= ph <= 8.5 else "pH level needs adjustment",
        min(100, hardness / 180 * 100),
        "Good mineral balance" if 60 <= hardness <= 180 else "Mineral content needs adjustment",
        100 - (probability[0][1] * 100),
        "Low contamination risk" if probability[0][1] > 0.7 else "Moderate to high contamination risk"
    ), unsafe_allow_html=True)
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability[0][1] * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Water Quality Score", 'font': {'size': 24, 'color': '#2a3f5f'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#0288d1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ff9800'},
                {'range': [40, 70], 'color': '#4caf50'},
                {'range': [70, 100], 'color': '#2196f3'}
            ],
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "#2a3f5f", 'family': "Arial"}
    )
    
    st.plotly_chart(fig)

    # Add result statement block
    result_color = "#4caf50" if prediction[0] == 1 else "#f44336"
    result_text = "✅ WATER IS POTABLE" if prediction[0] == 1 else "❌ WATER IS NOT POTABLE"
    result_description = (
        "This water sample meets the WHO and EPA safety standards for drinking water based on the analyzed parameters. "
        "Regular monitoring is still recommended to maintain water quality."
        if prediction[0] == 1 else 
        "This water sample does not meet the safety standards for drinking water. "
        "Treatment or filtration is recommended before consumption."
    )
    
    recommendations = []
    if ph < 6.5 or ph > 8.5:
        recommendations.append("Adjust pH levels to be between 6.5 and 8.5")
    if hardness > 180:
        recommendations.append("Consider using a water softener")
    if solids > 1500:
        recommendations.append("Install a reverse osmosis system to reduce dissolved solids")
    if chloramines > 4:
        recommendations.append("Reduce chloramine levels through filtration")
    if turbidity > 5:
        recommendations.append("Use a sediment filter to improve water clarity")

    recommendation_html = ""
    if recommendations:
        recommendation_html = """
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee;">
                <h4 style="color: #666;">Recommendations:</h4>
                <ul style="color: #666; padding-left: 1.5rem;">
                    {}
                </ul>
            </div>
        """.format("".join(f"<li>{r}</li>" for r in recommendations))

    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            border-left: 5px solid {result_color};
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            animation: slideUp 0.5s ease-out;
        ">
            <h2 style="
                color: {result_color};
                margin-bottom: 1rem;
                font-size: 2em;
                font-weight: bold;
            ">{result_text}</h2>
            <p style="
                color: #333;
                font-size: 1.2em;
                line-height: 1.5;
                margin: 1rem 0;
            ">{result_description}</p>
            <div style="
                margin-top: 1.5rem;
                padding-top: 1.5rem;
                border-top: 1px solid #eee;
                color: #666;
            ">
                <span style="font-size: 1.1em;">Confidence Score: 
                    <strong style="color: {result_color}">{probability[0][1]*100:.1f}%</strong>
                </span>
            </div>
            {recommendation_html}
        </div>
    """, unsafe_allow_html=True)

# Add parameter guide
st.markdown("""
    <div class="input-container">
        <h3>📊 Parameter Guide</h3>
        <div class="analysis-grid">
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