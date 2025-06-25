# Import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure GenAI
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Apply safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System prompt with section headers
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital.

Please provide your response under the following **four clear headings**:

1. **Detailed Analysis**: Describe any abnormalities or health concerns.
2. **Findings Report**: Bullet points summarizing what is seen.
3. **Recommendations and Next Steps**: Suggest further tests or consultations.
4. **Treatment Suggestions**: Outline any initial treatments if appropriate.

Important:
- Respond only if image pertains to human health.
- If image quality is poor, mention: 'Unable to determine based on the provided image.'
- End with this disclaimer: "**Consult with a Doctor before making any decisions.**"
"""

# Model configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon="🧠", layout="centered")

# Custom styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f2f9ff;
        }

        .custom-report h1,
        .custom-report h2,
        .custom-report h3,
        .custom-report h4,
        .custom-report strong,
        .custom-report p,
        .custom-report {
            color: #00264d !important;
            font-size: 1.05rem;
            line-height: 1.6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.image("Screenshot 2025-04-27 054229.png", width=150)
st.markdown("""
    <h1 style='color: #00264d; font-size: 2.5rem;'>🩺 Vital ❤️ Image 📸 Analytics</h1>
    <h3 style='color: #003366; font-weight: normal;'>An AI-powered tool to help analyze medical images for potential issues</h3>
""", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader("📤 Upload a medical image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview of Uploaded Image", width=300)

# Submit Button
submit_button = st.button("🧪 Generate the Analysis")

# Handle Analysis Logic
if submit_button:
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()

        # Create prompt input
        prompt_parts = [
            {"mime_type": "image/jpeg", "data": image_data},
            system_prompt,
        ]

        # Generate content
        with st.spinner("Analyzing the image..."):
            try:
                response = model.generate_content(prompt_parts)
                output_text = response.text

                st.success("✅ Analysis complete.")

                # Diagnostic Report Section
                st.markdown("""
                    <div class='custom-report'>
                        <h3>🧾 Diagnostic Report</h3>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div class='custom-report' style='background-color: #ffffff; padding: 1.25rem; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05);'>
                        {output_text}
                    </div>
                """, unsafe_allow_html=True)

                # Styled Disclaimer
                st.markdown("---", unsafe_allow_html=True)
                st.markdown("""
                    <div style='color: #00264d; font-size: 0.95rem; margin-top: 1rem;'>
                        🔒 <strong>Disclaimer:</strong> Consult with a certified medical professional before taking any action based on this report.
                    </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please upload a valid medical image.")
