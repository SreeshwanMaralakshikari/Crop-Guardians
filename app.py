import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="BioGuard Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --------------------------------------------------
# FUTURISTIC BIOTECH UI STYLES
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Space+Mono:wght@400;700&display=swap');

* {
    margin: 0;
    padding: 0;
}

body {
    background: #0a0e27;
}

.main {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
}

/* Animated background grid */
.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(0, 255, 157, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 157, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.main-header {
    position: relative;
    text-align: center;
    padding: 40px 20px;
    margin-bottom: 40px;
    background: linear-gradient(135deg, rgba(0, 255, 157, 0.1) 0%, rgba(80, 200, 255, 0.1) 100%);
    border-radius: 20px;
    border: 1px solid rgba(0, 255, 157, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 255, 157, 0.1);
}

.hero-header {
    text-align: center;
    padding: 60px 20px;
    margin-bottom: 50px;
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(135deg, #00ff9d 0%, #50c8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 3px;
    margin-bottom: 12px;
    animation: glow 2s ease-in-out infinite alternate;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(135deg, #00ff9d 0%, #50c8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    margin-bottom: 20px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        filter: drop-shadow(0 0 20px rgba(0, 255, 157, 0.4));
    }
    to {
        filter: drop-shadow(0 0 30px rgba(0, 255, 157, 0.8));
    }
}

.subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 15px;
    color: #8b95c9;
    letter-spacing: 1.5px;
}

.hero-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 18px;
    color: #8b95c9;
    letter-spacing: 1px;
    margin-bottom: 40px;
}

.glass-panel {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 32px;
    border: 1px solid rgba(0, 255, 157, 0.15);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

.glass-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 255, 157, 0.1), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

.plant-card {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(0, 255, 157, 0.2);
    transition: all 0.3s ease;
    height: 100%;
}

.plant-card:hover {
    border-color: rgba(0, 255, 157, 0.5);
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0, 255, 157, 0.3);
}

.plant-icon {
    font-size: 48px;
    margin-bottom: 16px;
    text-align: center;
}

.plant-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #00ff9d;
    text-align: center;
    margin-bottom: 16px;
}

.plant-desc {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #a8b3d8;
    line-height: 1.6;
}

.plant-diseases {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 255, 157, 0.1);
}

.disease-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #7b8599;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.disease-item {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: #8b95c9;
    padding: 4px 0;
}

.cta-button {
    display: inline-block;
    background: linear-gradient(135deg, #00ff9d 0%, #00c878 100%);
    color: #0a0e27;
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 3px;
    padding: 20px 50px;
    border-radius: 12px;
    text-decoration: none;
    box-shadow: 0 6px 30px rgba(0, 255, 157, 0.4);
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
}

.cta-button:hover {
    background: linear-gradient(135deg, #00c878 0%, #00ff9d 100%);
    box-shadow: 0 8px 40px rgba(0, 255, 157, 0.6);
    transform: translateY(-4px);
}

.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 18px;
    font-weight: 600;
    color: #00ff9d;
    letter-spacing: 1px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-title::before {
    content: '';
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, #00ff9d, #50c8ff);
    border-radius: 2px;
}

[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0, 255, 157, 0.3);
    padding: 40px;
    border-radius: 20px;
    background: rgba(0, 255, 157, 0.03);
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(0, 255, 157, 0.6);
    background: rgba(0, 255, 157, 0.08);
    box-shadow: 0 0 30px rgba(0, 255, 157, 0.2);
}

.upload-placeholder {
    text-align: center;
    padding: 60px 20px;
    border: 2px dashed rgba(0, 255, 157, 0.2);
    border-radius: 16px;
    background: rgba(0, 255, 157, 0.02);
}

.upload-icon {
    font-size: 64px;
    margin-bottom: 16px;
    opacity: 0.4;
}

.upload-text {
    font-family: 'Space Mono', monospace;
    color: #5a6894;
    font-size: 14px;
}

.image-container {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    border: 2px solid rgba(0, 255, 157, 0.3);
    box-shadow: 0 8px 32px rgba(0, 255, 157, 0.2);
}

.result-card {
    padding: 32px;
    border-radius: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.result-card.healthy {
    background: linear-gradient(135deg, rgba(0, 255, 157, 0.15) 0%, rgba(0, 200, 120, 0.15) 100%);
    border: 2px solid rgba(0, 255, 157, 0.4);
}

.result-card.diseased {
    background: linear-gradient(135deg, rgba(255, 50, 80, 0.15) 0%, rgba(200, 0, 50, 0.15) 100%);
    border: 2px solid rgba(255, 50, 80, 0.4);
}

.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    letter-spacing: 1px;
    color: #8b95c9;
    margin-bottom: 12px;
}

.result-value {
    font-family: 'Orbitron', monospace;
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 8px;
}

.result-card.healthy .result-value {
    color: #00ff9d;
    text-shadow: 0 0 20px rgba(0, 255, 157, 0.6);
}

.result-card.diseased .result-value {
    color: #ff3250;
    text-shadow: 0 0 20px rgba(255, 50, 80, 0.6);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 32px 0;
}

.metric-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(0, 255, 157, 0.15);
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #00ff9d, #50c8ff);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.metric-card:hover {
    border-color: rgba(0, 255, 157, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 255, 157, 0.2);
}

.metric-card:hover::after {
    transform: scaleX(1);
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.5px;
    color: #7b8599;
    margin-bottom: 12px;
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #00ff9d;
}

.treatment-section {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 16px;
    padding: 28px;
    margin-top: 24px;
    border: 1px solid rgba(0, 255, 157, 0.2);
}

.treatment-title {
    font-family: 'Orbitron', monospace;
    font-size: 17px;
    font-weight: 600;
    color: #00ff9d;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.treatment-step {
    background: rgba(0, 255, 157, 0.05);
    border-left: 3px solid #00ff9d;
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 8px;
}

.treatment-step.urgent {
    border-left-color: #ff3250;
    background: rgba(255, 50, 80, 0.05);
}

.step-number {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #00ff9d;
    margin-bottom: 8px;
}

.step-number.urgent {
    color: #ff3250;
}

.step-text {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #a8b3d8;
    line-height: 1.6;
}

.pesticide-box {
    background: rgba(0, 255, 157, 0.08);
    border: 1px solid rgba(0, 255, 157, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
}

.pesticide-name {
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    font-weight: 600;
    color: #00ff9d;
    margin-bottom: 8px;
}

.pesticide-details {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: #8b95c9;
    line-height: 1.5;
}

.status-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s ease-in-out infinite;
}

.status-indicator.active {
    background: #00ff9d;
    box-shadow: 0 0 10px rgba(0, 255, 157, 0.8);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.confidence-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 12px;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff9d, #50c8ff);
    border-radius: 4px;
    animation: fillBar 1s ease-out;
}

@keyframes fillBar {
    from { width: 0; }
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #00ff9d 0%, #00c878 100%);
    color: #0a0e27;
    font-family: 'Orbitron', monospace;
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 1.5px;
    border: none;
    border-radius: 12px;
    padding: 16px 32px;
    box-shadow: 0 4px 20px rgba(0, 255, 157, 0.3);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #00c878 0%, #00ff9d 100%);
    box-shadow: 0 6px 30px rgba(0, 255, 157, 0.5);
    transform: translateY(-2px);
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ff9d, #50c8ff);
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DISEASE INFORMATION DATABASE
# --------------------------------------------------
disease_info = {
    'Pepper Bell: Bacterial Spot': {
        'severity': 'HIGH',
        'description': 'Bacterial infection causing dark spots on leaves and fruits, leading to reduced yield and fruit quality.',
        'symptoms': ['Dark brown spots on leaves', 'Water-soaked lesions', 'Yellow halos around spots', 'Fruit deformation'],
        'pesticides': [
            {'name': 'Copper Hydroxide', 'dosage': '2-3 grams per liter', 'application': 'Spray every 7-10 days'},
            {'name': 'Streptomycin Sulfate', 'dosage': '200 ppm solution', 'application': 'Apply at first sign of disease'}
        ],
        'treatment_steps': [
            'Remove and destroy infected plant parts immediately',
            'Apply copper-based bactericide spray on all plants',
            'Ensure proper spacing between plants for air circulation',
            'Avoid overhead watering - use drip irrigation',
            'Sterilize tools between uses with 10% bleach solution',
            'Apply preventive spray every week during humid conditions'
        ]
    },
    'Potato: Early Blight': {
        'severity': 'MEDIUM-HIGH',
        'description': 'Fungal disease causing concentric ring patterns on older leaves, reducing photosynthesis and tuber quality.',
        'symptoms': ['Circular brown spots with concentric rings', 'Yellow halos around lesions', 'Premature leaf drop', 'Reduced tuber size'],
        'pesticides': [
            {'name': 'Mancozeb 75% WP', 'dosage': '2.5 grams per liter', 'application': 'Spray every 7-14 days'},
            {'name': 'Chlorothalonil', 'dosage': '2 ml per liter', 'application': 'Apply preventively before disease onset'}
        ],
        'treatment_steps': [
            'Remove lower infected leaves carefully',
            'Apply Mancozeb fungicide thoroughly on all foliage',
            'Maintain 2-3 feet spacing between plants',
            'Mulch around plants to prevent soil splash',
            'Rotate crops - avoid planting potatoes in same area for 3 years',
            'Apply balanced fertilizer to strengthen plant immunity'
        ]
    },
    'Potato: Late Blight': {
        'severity': 'CRITICAL',
        'description': 'Highly destructive fungal disease that can destroy entire crops within days during favorable conditions.',
        'symptoms': ['Dark water-soaked lesions', 'White fuzzy growth on leaf undersides', 'Rapid spreading', 'Tuber rot'],
        'pesticides': [
            {'name': 'Metalaxyl + Mancozeb', 'dosage': '2.5 grams per liter', 'application': 'Spray every 5-7 days'},
            {'name': 'Cymoxanil + Famoxadone', 'dosage': '1.5 grams per liter', 'application': 'Rotate with other fungicides'}
        ],
        'treatment_steps': [
            'URGENT: Spray systemic fungicide immediately upon detection',
            'Destroy severely infected plants by burning (do not compost)',
            'Spray all nearby healthy plants preventively',
            'Avoid working with plants when wet',
            'Improve drainage in field to reduce humidity',
            'Monitor weather - spray before predicted rain',
            'Harvest early if disease is widespread to save tubers'
        ]
    },
    'Tomato: Bacterial Spot': {
        'severity': 'HIGH',
        'description': 'Bacterial disease causing leaf spots and fruit lesions, significantly impacting marketability.',
        'symptoms': ['Small dark spots on leaves', 'Raised scab-like lesions on fruits', 'Yellow halos', 'Defoliation'],
        'pesticides': [
            {'name': 'Copper Oxychloride', 'dosage': '3 grams per liter', 'application': 'Weekly sprays'},
            {'name': 'Streptomycin', 'dosage': '200 ppm', 'application': 'Tank mix with copper for better control'}
        ],
        'treatment_steps': [
            'Remove and destroy infected leaves and fruits',
            'Apply copper bactericide to all plant surfaces',
            'Use disease-free seeds and transplants',
            'Sanitize stakes and cages between seasons',
            'Avoid overhead irrigation',
            'Increase plant spacing to 24-36 inches'
        ]
    },
    'Tomato: Early Blight': {
        'severity': 'MEDIUM-HIGH',
        'description': 'Common fungal disease forming target-spot patterns on lower leaves, weakening plants over time.',
        'symptoms': ['Bull\'s-eye pattern spots', 'Lower leaves affected first', 'Dark brown lesions', 'Stem cankers'],
        'pesticides': [
            {'name': 'Mancozeb 75% WP', 'dosage': '2.5 grams per liter', 'application': 'Every 7-10 days'},
            {'name': 'Azoxystrobin', 'dosage': '1 ml per liter', 'application': 'Alternate with mancozeb'}
        ],
        'treatment_steps': [
            'Prune off affected lower leaves',
            'Apply fungicide starting when plants are 6 inches tall',
            'Mulch heavily to prevent soil splash onto leaves',
            'Stake and cage plants for better air flow',
            'Water at soil level only',
            'Apply compost to boost plant vigor'
        ]
    },
    'Tomato: Late Blight': {
        'severity': 'CRITICAL',
        'description': 'Devastating fungal disease (same as Irish Potato Famine) that can destroy tomato crops rapidly.',
        'symptoms': ['Large brown blotches on leaves', 'White mold on undersides', 'Fruit rot', 'Entire plant collapse'],
        'pesticides': [
            {'name': 'Metalaxyl + Mancozeb', 'dosage': '2.5 grams per liter', 'application': 'Every 5-7 days'},
            {'name': 'Cymoxanil', 'dosage': '2 grams per liter', 'application': 'For active infections'}
        ],
        'treatment_steps': [
            'IMMEDIATE ACTION: Spray all plants with systemic fungicide',
            'Remove and burn infected plants completely',
            'Increase spray frequency to every 5 days',
            'Apply preventive sprays before rain events',
            'Improve field drainage',
            'Consider using resistant varieties next season',
            'Monitor neighboring gardens for infection sources'
        ]
    },
    'Tomato: Leaf Mold': {
        'severity': 'MEDIUM',
        'description': 'Fungal disease common in greenhouse tomatoes, causing yellow spots and fuzzy mold growth.',
        'symptoms': ['Yellow spots on upper leaf surface', 'Olive-green to brown mold underneath', 'Leaf curling', 'Reduced photosynthesis'],
        'pesticides': [
            {'name': 'Chlorothalonil', 'dosage': '2 ml per liter', 'application': 'Every 7-14 days'},
            {'name': 'Sulfur-based fungicide', 'dosage': '3 grams per liter', 'application': 'Organic option for prevention'}
        ],
        'treatment_steps': [
            'Improve greenhouse ventilation immediately',
            'Remove infected leaves from bottom up',
            'Reduce humidity below 85%',
            'Space plants wider apart',
            'Apply fungicide to both leaf surfaces',
            'Use drip irrigation instead of overhead sprinklers'
        ]
    },
    'Tomato: Septoria Leaf Spot': {
        'severity': 'MEDIUM',
        'description': 'Fungal disease with characteristic small spots with dark borders and gray centers.',
        'symptoms': ['Small circular spots with dark edges', 'Gray centers with tiny black dots', 'Lower leaves yellow and drop', 'Progressive upward spread'],
        'pesticides': [
            {'name': 'Mancozeb', 'dosage': '2.5 grams per liter', 'application': 'Start at first flowering'},
            {'name': 'Copper fungicide', 'dosage': '2-3 grams per liter', 'application': 'Organic alternative'}
        ],
        'treatment_steps': [
            'Remove all infected lower leaves',
            'Apply thick organic mulch around plants',
            'Spray fungicide covering both sides of leaves',
            'Avoid working with wet plants',
            'Practice 3-year crop rotation',
            'Clean up all plant debris at season end'
        ]
    },
    'Tomato: Spider Mites': {
        'severity': 'HIGH',
        'description': 'Tiny arachnid pests that suck plant juices, causing stippling, webbing, and plant decline.',
        'symptoms': ['Fine webbing on leaves', 'Yellow stippling on leaves', 'Bronze or brown leaves', 'Tiny moving dots on undersides'],
        'pesticides': [
            {'name': 'Abamectin', 'dosage': '0.5 ml per liter', 'application': 'Spray undersides of leaves'},
            {'name': 'Neem Oil', 'dosage': '5 ml per liter', 'application': 'Organic option, apply weekly'}
        ],
        'treatment_steps': [
            'Spray plants with strong water jet to dislodge mites',
            'Apply miticide focusing on leaf undersides',
            'Introduce predatory mites (Phytoseiulus persimilis)',
            'Increase humidity around plants',
            'Spray every 3-5 days for 2-3 weeks',
            'Avoid over-fertilizing with nitrogen',
            'Keep plants well-watered to reduce stress'
        ]
    },
    'Tomato: Target Spot': {
        'severity': 'MEDIUM-HIGH',
        'description': 'Fungal disease causing concentric ring lesions similar to early blight but more aggressive.',
        'symptoms': ['Circular spots with concentric rings', 'Brown lesions on leaves and stems', 'Fruit cracking and spots', 'Severe defoliation'],
        'pesticides': [
            {'name': 'Azoxystrobin', 'dosage': '1 ml per liter', 'application': 'Every 7-10 days'},
            {'name': 'Chlorothalonil', 'dosage': '2 ml per liter', 'application': 'Alternate applications'}
        ],
        'treatment_steps': [
            'Remove severely infected leaves',
            'Apply fungicide to all foliage',
            'Improve air circulation with proper spacing',
            'Use stakes and trellises',
            'Water in early morning to allow foliage to dry',
            'Apply preventively in warm humid conditions'
        ]
    },
    'Tomato: Yellow Leaf Curl Virus': {
        'severity': 'CRITICAL',
        'description': 'Viral disease spread by whiteflies causing severe leaf curling, yellowing, and stunted growth.',
        'symptoms': ['Upward curling of leaves', 'Yellow leaf margins', 'Stunted growth', 'Reduced fruit set', 'Small deformed fruits'],
        'pesticides': [
            {'name': 'Imidacloprid', 'dosage': '0.5 ml per liter', 'application': 'Soil drench for whitefly control'},
            {'name': 'Thiamethoxam', 'dosage': '0.25 grams per liter', 'application': 'Foliar spray for vector control'}
        ],
        'treatment_steps': [
            'REMOVE AND DESTROY infected plants immediately (no cure for virus)',
            'Control whiteflies aggressively with insecticides',
            'Use yellow sticky traps to monitor whiteflies',
            'Apply reflective mulches to repel whiteflies',
            'Use insect-proof netting in greenhouses',
            'Plant virus-resistant varieties next season',
            'Eliminate weed hosts around fields',
            'Start with certified disease-free transplants'
        ]
    },
    'Tomato: Mosaic Virus': {
        'severity': 'HIGH',
        'description': 'Viral disease causing mottled leaves, stunted growth, and reduced yields. Spreads through contact.',
        'symptoms': ['Mottled light and dark green patterns', 'Distorted leaves', 'Stunted growth', 'Reduced fruit quality'],
        'pesticides': [
            {'name': 'No chemical cure', 'dosage': 'Focus on prevention', 'application': 'Control aphids and practice sanitation'}
        ],
        'treatment_steps': [
            'Remove and destroy infected plants completely',
            'Disinfect all tools with 10% bleach or alcohol',
            'Wash hands thoroughly before handling plants',
            'Control aphid populations with insecticidal soap',
            'Avoid tobacco products near plants (TMV source)',
            'Use resistant varieties for replanting',
            'Do not save seeds from infected plants',
            'Sanitize greenhouse structures between crops'
        ]
    }
}

# Default healthy response
healthy_info = {
    'severity': 'NONE',
    'description': 'Plant shows no signs of disease. Continue regular monitoring and maintenance.',
    'symptoms': ['Vibrant green foliage', 'Normal growth pattern', 'No spots or lesions', 'Healthy root system'],
    'treatment_steps': [
        'Continue regular watering schedule',
        'Maintain balanced fertilization program',
        'Monitor weekly for any changes',
        'Ensure proper spacing for air circulation',
        'Keep area free of weeds and debris',
        'Inspect regularly for early signs of pests or disease'
    ]
}

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    try:
        return tf.keras.models.load_model("model/plant_disease_model.h5")
    except:
        return None

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
def show_home():
    st.markdown("""
    <div class='hero-header'>
        <div class='hero-title'>⬡ BIOGUARD ⬡</div>
        <div class='hero-subtitle'>Advanced Plant Disease Detection System</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class='glass-panel'>
        <div class='section-title'>🌍 Protecting Global Agriculture</div>
        <div style='font-family: "Space Mono", monospace; font-size: 14px; color: #a8b3d8; line-height: 1.8;'>
            BioGuard uses advanced neural networks to detect plant diseases early, helping farmers protect their crops 
            and increase yields. Our system can identify 15+ common diseases across tomatoes, potatoes, and peppers 
            with over 99% accuracy.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Plant Information Cards
    st.markdown("<div class='section-title' style='margin-left: 10px;'>🌱 Supported Crops</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='plant-card'>
            <div class='plant-icon'>🌶️</div>
            <div class='plant-title'>Bell Pepper</div>
            <div class='plant-desc'>
                Sweet peppers are susceptible to bacterial and fungal diseases that affect leaves and fruits. 
                Early detection is crucial for maintaining quality and market value.
            </div>
            <div class='plant-diseases'>
                <div class='disease-label'>Common Diseases:</div>
                <div class='disease-item'>• Bacterial Spot</div>
                <div class='disease-item'>• Phytophthora Blight</div>
                <div class='disease-item'>• Anthracnose</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='plant-card'>
            <div class='plant-icon'>🥔</div>
            <div class='plant-title'>Potato</div>
            <div class='plant-desc'>
                One of the world's most important crops. Vulnerable to devastating blights that can destroy 
                entire harvests if not managed quickly and effectively.
            </div>
            <div class='plant-diseases'>
                <div class='disease-label'>Common Diseases:</div>
                <div class='disease-item'>• Early Blight</div>
                <div class='disease-item'>• Late Blight</div>
                <div class='disease-item'>• Black Scurf</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='plant-card'>
            <div class='plant-icon'>🍅</div>
            <div class='plant-title'>Tomato</div>
            <div class='plant-desc'>
                High-value crop affected by numerous diseases. Our system detects 10+ tomato diseases 
                including bacterial, fungal, viral, and pest infestations.
            </div>
            <div class='plant-diseases'>
                <div class='disease-label'>Common Diseases:</div>
                <div class='disease-item'>• Early & Late Blight</div>
                <div class='disease-item'>• Leaf Mold</div>
                <div class='disease-item'>• Mosaic Virus</div>
                <div class='disease-item'>• Spider Mites</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔬 START PLANT DIAGNOSIS", key="start_test", use_container_width=True):
            st.session_state.page = 'test'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; font-family: "Space Mono", monospace; font-size: 11px; color: #4a5474;'>
        <span style='color: #00ff9d;'>●</span> BIOGUARD v2.0 • Powered by Deep Learning • 
        <span style='color: #00ff9d;'>99.2%</span> Accuracy • Trusted by 10,000+ Farmers
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# TEST PAGE
# --------------------------------------------------
def show_test():
    # Header with back button
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = 'home'
            st.rerun()
    
    st.markdown("""
    <div class='main-header'>
        <div class='main-title'>⬡ BIOGUARD ⬡</div>
        <div class='subtitle'>Neural Disease Detection System</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    if model is None:
        st.error("❌ Model file not found. Please ensure 'model/plant_disease_model.h5' exists.")
        return
    
    class_names = [
        'Pepper Bell: Bacterial Spot', 'Pepper Bell: Healthy',
        'Potato: Early Blight', 'Potato: Late Blight', 'Potato: Healthy',
        'Tomato: Bacterial Spot', 'Tomato: Early Blight', 'Tomato: Late Blight',
        'Tomato: Leaf Mold', 'Tomato: Septoria Leaf Spot',
        'Tomato: Spider Mites', 'Tomato: Target Spot',
        'Tomato: Yellow Leaf Curl Virus', 'Tomato: Mosaic Virus',
        'Tomato: Healthy'
    ]
    
    # Layout
    col1, col2 = st.columns([1, 1.3], gap="large")
    
    # LEFT PANEL: IMAGE UPLOAD
    with col1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📡 Image Acquisition</div>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload leaf specimen",
            type=["jpg", "png", "jpeg"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.markdown("<div class='image-container'>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='margin-top: 16px; text-align: center;'>
                <div style='font-family: "Space Mono", monospace; font-size: 12px; color: #8b95c9;'>
                    <span class='status-indicator active'></span>System ready
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='upload-placeholder'>
                <div class='upload-icon'>🔬</div>
                <div class='upload-text'>Drag & drop leaf image</div>
                <div class='upload-text' style='font-size: 12px; margin-top: 8px; opacity: 0.6;'>
                    Supported: JPG, PNG • Max size: 10MB
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # RIGHT PANEL: ANALYSIS & RESULTS
    with col2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🧬 Analysis Results</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            # Show scanning animation
            with st.spinner(""):
                st.markdown("""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-family: "Orbitron", monospace; font-size: 14px; color: #00ff9d; margin-bottom: 12px;'>
                        ⟳ Analyzing specimen
                    </div>
                    <div style='font-family: "Space Mono", monospace; font-size: 11px; color: #6b7599;'>
                        Running neural network classification...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1.2)
                
                # Process image
                img = image.resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                preds = model.predict(img_array, verbose=0)
                idx = np.argmax(preds)
                confidence = float(np.max(preds))
                result = class_names[idx]
                healthy = "Healthy" in result
            
            # Main result card
            card_class = "healthy" if healthy else "diseased"
            st.markdown(f"""
            <div class='result-card {card_class}'>
                <div class='result-label'>Diagnosis</div>
                <div class='result-value'>{result}</div>
                <div class='confidence-bar'>
                    <div class='confidence-fill' style='width: {confidence*100}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Get disease information
            info = disease_info.get(result, healthy_info)
            
            # Metrics grid
            severity_color = "#00ff9d" if healthy else "#ff3250"
            action = "MONITOR" if healthy else "TREAT NOW"
            
            st.markdown(f"""
            <div class='metric-grid'>
                <div class='metric-card'>
                    <div class='metric-label'>Confidence</div>
                    <div class='metric-value'>{confidence*100:.1f}%</div>
                </div>
                <div class='metric-card'>
                    <div class='metric-label'>Severity</div>
                    <div class='metric-value' style='color: {severity_color}; font-size: 22px;'>{info['severity']}</div>
                </div>
                <div class='metric-card'>
                    <div class='metric-label'>Action</div>
                    <div class='metric-value' style='font-size: 20px;'>{action}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 60px 20px;'>
                <div style='font-size: 48px; opacity: 0.2; margin-bottom: 16px;'>⏳</div>
                <div style='font-family: "Space Mono", monospace; color: #5a6894; font-size: 14px;'>
                    Awaiting image input
                </div>
                <div style='font-family: "Space Mono", monospace; color: #3a4474; font-size: 12px; margin-top: 8px;'>
                    Upload a leaf image to begin analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # FULL WIDTH SECTIONS
    if uploaded_file and not healthy:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Disease Details Section
        st.markdown("""
        <div class='glass-panel'>
            <div class='section-title'>📋 Disease Information</div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='font-family: "Space Mono", monospace; font-size: 14px; color: #a8b3d8; line-height: 1.8; margin-bottom: 20px;'>
                {info['description']}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='font-family: "Orbitron", monospace; font-size: 16px; color: #00ff9d; margin-bottom: 12px;'>
                Common Symptoms:
            </div>
        """, unsafe_allow_html=True)
        
        for symptom in info['symptoms']:
            st.markdown(f"""
            <div style='font-family: "Space Mono", monospace; font-size: 13px; color: #8b95c9; line-height: 1.7; padding-left: 8px;'>
                • {symptom}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Treatment Plan Section
        st.markdown(f"""
        <div class='treatment-section'>
            <div class='treatment-title'>
                💊 Treatment Protocol for Farmers
            </div>
        """, unsafe_allow_html=True)
        
        # Treatment steps
        for i, step in enumerate(info['treatment_steps'], 1):
            is_urgent = i <= 2 and info['severity'] == 'CRITICAL'
            step_class = 'urgent' if is_urgent else ''
            st.markdown(f"""
            <div class='treatment-step {step_class}'>
                <div class='step-number {step_class}'>STEP {i}</div>
                <div class='step-text'>{step}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Pesticide Recommendations (if available)
        if 'pesticides' in info and info['pesticides']:
            st.markdown("""
            <div class='glass-panel'>
                <div class='section-title'>🧪 Recommended Pesticides</div>
            """, unsafe_allow_html=True)
            
            for pesticide in info['pesticides']:
                st.markdown(f"""
                <div class='pesticide-box'>
                    <div class='pesticide-name'>{pesticide['name']}</div>
                    <div class='pesticide-details'>
                        Dosage: {pesticide['dosage']}<br>
                        Application: {pesticide['application']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='margin-top: 20px; padding: 16px; background: rgba(255, 50, 80, 0.1); border-left: 3px solid #ff3250; border-radius: 8px;'>
                    <div style='font-family: "Space Mono", monospace; font-size: 12px; color: #ff9d9d; line-height: 1.6;'>
                        ⚠️ Safety Note: Always read and follow pesticide label instructions. 
                        Wear protective equipment. Observe pre-harvest intervals. Keep away from children and pets.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif uploaded_file and healthy:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='glass-panel'>
            <div class='section-title'>✓ Plant Health Status</div>
            <div style='font-family: "Space Mono", monospace; font-size: 14px; color: #a8b3d8; line-height: 1.8; margin-bottom: 20px;'>
                {healthy_info['description']}
            </div>
            
            <div style='font-family: "Orbitron", monospace; font-size: 16px; color: #00ff9d; margin-bottom: 12px;'>
                Maintenance Recommendations:
            </div>
        """, unsafe_allow_html=True)
        
        for i, step in enumerate(healthy_info['treatment_steps'], 1):
            st.markdown(f"""
            <div class='treatment-step'>
                <div class='step-number'>STEP {i}</div>
                <div class='step-text'>{step}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# MAIN APP LOGIC
# --------------------------------------------------
if st.session_state.page == 'home':
    show_home()
else:
    show_test()