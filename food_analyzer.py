import streamlit as st
import google.generativeai as genai
from PIL import Image

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

    return genai.GenerativeModel('gemini-1.5-pro')

def analyze_food_image(model, image):
    prompt = """
    You are a professional nutritionist. Analyze this food image and provide a concise analysis in the following format:
    
    1. Food Items: [List the main foods you see]
    2. Estimated Calories: [Approximate total]
    3. Nutritional Profile:
       • Protein: [estimate in grams]
       • Carbs: [estimate in grams]
       • Fat: [estimate in grams]
    4. write every items names with the number of calories and tell the total number of calories
    5. Health Notes: [Brief nutritional insights]
    """
    
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def main():
    st.set_page_config(page_title="Quick Food Analyzer", layout="wide")
    
    st.markdown("""
        <style>
        .main {padding: 2rem;}
        .stAlert {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        .stImage {
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🍽️ Food Analyzer")
    st.caption("Powered by Gemini 1.5 Pro")
    
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    if api_key:
        try:
            model = configure_gemini(api_key)
            
            uploaded_file = st.file_uploader(
                "Upload a food image",
                type=['jpg', 'jpeg', 'png'],
                help="Take a clear photo of your food for instant analysis"
            )
            
            if uploaded_file:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    image = Image.open(uploaded_file)
                    st.image(image, use_column_width=True, caption="Your Food Image")
                
                with col2:
                    with st.spinner("Analyzing..."):
                        analysis = analyze_food_image(model, image)
                        st.markdown(analysis)
                        
                        # Add a refresh button
                        if st.button("🔄 Analyze Again"):
                            with st.spinner("Regenerating analysis..."):
                                analysis = analyze_food_image(model, image)
                                st.markdown(analysis)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            # Add debugging information
            st.error("Available models:")
            try:
                for m in genai.list_models():
                    st.write(f"- {m.name}")
            except Exception as e:
                st.error(f"Could not list models: {str(e)}")
    else:
        st.info("Please enter your Gemini API key to start analyzing food images.")
        st.markdown("""
        ### Quick Start Guide:
        1. Enter your Gemini API key
        2. Upload a food photo
        3. Get instant nutritional insights
        
        **Tips for Best Results:**
        - Use well-lit photos
        - Center the food in the frame
        - Include the full plate/dish
        """)

if __name__ == "__main__":
    main()
