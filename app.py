import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="AI Medicine Assistant",
    page_icon="💊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .info-box {
        background: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Knowledge Base - Medicines, Diet, Precautions
KNOWLEDGE_BASE = {
    "fever": {
        "medicines": [
            "Paracetamol (500mg) - 1 tablet every 6-8 hours (max 4g/day)",
            "Ibuprofen (400mg) - 1 tablet every 8 hours (with food)",
            "Meftal-P - For severe fever (consult doctor)"
        ],
        "diet": [
            "Hydrating fluids: Water, ORS, coconut water, fresh juices",
            "Light foods: Khichdi, porridge, boiled vegetables, soup",
            "Fruits: Banana, apple, papaya, watermelon",
            "Avoid: Spicy, oily, heavy foods"
        ],
        "precautions": [
            "Rest completely, stay hydrated",
            "Monitor temperature regularly",
            "Sponge bath with lukewarm water if fever > 102°F",
            "Consult doctor if fever persists >3 days or >103°F",
            "Avoid self-medication beyond 48 hours"
        ]
    },
    "cold": {
        "medicines": [
            "Cetirizine (10mg) - 1 tablet at night for runny nose",
            "Dolo 650 - For body ache/fever",
            "Sinarest - 1 tablet twice daily (morning & evening)",
            "Steam inhalation with Vicks - 2-3 times daily"
        ],
        "diet": [
            "Warm fluids: Herbal tea, ginger-honey tea, warm soup",
            "Vitamin C rich: Oranges, lemon water, amla juice",
            "Light diet: Dal-chawal, vegetable soup",
            "Avoid: Cold drinks, ice cream, fried foods"
        ],
        "precautions": [
            "Keep warm, avoid cold exposure",
            "Steam inhalation 3-4 times daily",
            "Gargle with warm salt water 3 times daily",
            "Avoid sharing towels/utensils",
            "Consult doctor if symptoms persist >7 days"
        ]
    },
    "cough": {
        "medicines": [
            "Cough syrup (Ascoril/Honitus) - 10ml thrice daily",
            "Montair LC - 1 tablet at night",
            "Dolo 650 - For associated fever",
            "Steam inhalation with Karvol plus"
        ],
        "diet": [
            "Warm liquids: Honey-lemon water, tulsi tea",
            "Soft foods: Porridge, mashed potato, soup",
            "Fruits: Banana, pear, apple (peeled)",
            "Avoid: Cold foods, dairy products, nuts"
        ],
        "precautions": [
            "Elevate head while sleeping",
            "Avoid smoke, dust, allergens",
            "Honey (1 tsp) with warm water morning & night",
            "Consult doctor if cough with blood/sputum"
        ]
    },
    "headache": {
        "medicines": [
            "Paracetamol (650mg) - 1 tablet (max 3-4/day)",
            "Ibuprofen (400mg) - 1 tablet with food",
            "For migraine: Sumatriptan (consult doctor)"
        ],
        "diet": [
            "Hydrating foods: Water, coconut water, buttermilk",
            "Magnesium rich: Banana, spinach, almonds",
            "Avoid: Caffeine excess, processed foods",
            "Light meals: Khichdi, curd rice"
        ],
        "precautions": [
            "Rest in dark quiet room",
            "Cold compress on forehead",
            "Avoid screen time during headache",
            "Track triggers (stress, dehydration, sleep)",
            "Consult if headache with vomiting/vision issues"
        ]
    },
    "diarrhea": {
        "medicines": [
            "ORS - 1 glass after each loose stool",
            "Norflox TZ - 1 tablet twice daily (3 days)",
            "Loperamide - 1 tablet after loose stool (max 4/day)",
            "Electral powder in 1L water"
        ],
        "diet": [
            "BRAT diet: Banana, Rice, Apple, Toast",
            "Boiled water, ORS, coconut water",
            "Curd/rice, khichdi, boiled potato",
            "Avoid: Milk, spicy, oily, raw foods"
        ],
        "precautions": [
            "Maintain hydration (ORS mandatory)",
            "Hand hygiene crucial",
            "Monitor urine output/color",
            "Consult doctor if >6 stools/day or blood",
            "No anti-diarrheal in children <12 yrs"
        ]
    },
    "stomach pain": {
        "medicines": [
            "Pantop D - 1 tablet empty stomach morning",
            "Meftal Spas - 1 tablet for cramps (max 3/day)",
            "Digene - 1-2 tablets after meals",
            "Cyclopam - For severe spasms"
        ],
        "diet": [
            "Light bland diet: Khichdi, curd rice, boiled dal",
            "Hydration: Warm water, jeera water",
            "Probiotics: Curd, buttermilk",
            "Avoid: Spicy, fried, raw salads"
        ],
        "precautions": [
            "Eat small frequent meals",
            "Avoid lying down immediately after eating",
            "Hot water bag on abdomen",
            "Consult if pain >24hrs or with vomiting"
        ]
    }
}

# Common symptoms mapping
SYMPTOM_MAP = {
    "fever": "fever",
    "cold": ["cold", "cough", "sneezing", "runny nose"],
    "cough": "cough",
    "headache": ["headache", "migraine", "head pain"],
    "diarrhea": ["diarrhea", "loose motion", "stomach upset"],
    "stomach pain": ["stomach pain", "abdominal pain", "belly ache"]
}

def find_disease(query):
    """Find matching disease from user query"""
    query_lower = query.lower()
    for disease, keywords in SYMPTOM_MAP.items():
        if isinstance(keywords, list):
            if any(keyword in query_lower for keyword in keywords):
                return disease
        elif keywords in query_lower:
            return disease
    return None

def main():
    st.markdown('<h1 class="main-header">💊 AI Medicine Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar disclaimer
    with st.sidebar:
        st.warning("⚠️ **DISCLAIMER**: This is for educational purposes only. Always consult a doctor before taking any medicine.")
        st.info("📞 **Emergency**: Call doctor immediately for severe symptoms")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2>🔍 Ask about your symptoms</h2>', unsafe_allow_html=True)
        
        # User input
        user_query = st.text_input(
            "Enter your symptoms (e.g., fever, cold, headache):",
            placeholder="Type your symptoms here..."
        )
        
        if user_query:
            disease = find_disease(user_query)
            
            if disease and disease in KNOWLEDGE_BASE:
                st.success(f"✅ Found treatment for **{disease.title()}**")
                
                # Tabs for Medicines, Diet, Precautions
                tab1, tab2, tab3 = st.tabs(["💊 Medicines", "🍎 Diet Recommendations", "⚠️ Precautions"])
                
                with tab1:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("📋 Recommended Medicines")
                    for i, medicine in enumerate(KNOWLEDGE_BASE[disease]["medicines"], 1):
                        st.markdown(f"**{i}.** {medicine}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab2:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.subheader("🥗 Recommended Diet")
                    for i, food in enumerate(KNOWLEDGE_BASE[disease]["diet"], 1):
                        st.markdown(f"**{i}.** {food}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with tab3:
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    st.subheader("🚨 Important Precautions")
                    for i, precaution in enumerate(KNOWLEDGE_BASE[disease]["precautions"], 1):
                        st.markdown(f"**{i}.** {precaution}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Quick Action Buttons
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("📋 Save Consultation", type="primary"):
                        st.balloons()
                        st.success("Consultation saved! Share with your doctor.")
                with col_b:
                    if st.button("🚨 Call Doctor"):
                        st.info("💡 Save this page and show to your doctor")
                with col_c:
                    if st.button("➕ Add Symptoms"):
                        st.rerun()
                        
            else:
                st.warning("❌ No specific treatment found. Common recommendations:")
                st.markdown("""
                **General Advice:**
                - Stay hydrated (2-3L water daily)
                - Rest adequately
                - Eat light home-cooked food
                - Monitor symptoms for 24-48 hours
                - **Consult doctor** for persistent symptoms
                """)
    
    with col2:
        st.markdown('<h3>📊 Quick Access</h3>', unsafe_allow_html=True)
        
        # Quick disease buttons
        for disease in KNOWLEDGE_BASE.keys():
            if st.button(f"💊 {disease.title()}"):
                st.session_state.user_query = disease
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        **✅ Features:**
        - Instant medicine recommendations
        - Diet plans for recovery
        - Safety precautions
        - Doctor consultation reminders
        - Mobile-friendly interface
        """)

if __name__ == "__main__":
    main()
