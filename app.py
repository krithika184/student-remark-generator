import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Automated Student Remark Generator", page_icon="📝")

st.title("📝 Student Remark Generator")
st.write(
    "Upload an image of the grade sheet to automatically generate student remarks."
)

# File uploader for mark sheet images
uploaded_file = st.file_uploader(
    "Upload Grade Sheet Image", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Display uploaded image preview
    image = Image.open(uploaded_file)
    # st.image(image, caption="Uploaded Grade Sheet")

    if st.button("Generate Remarks"):
        with st.spinner("Analyzing grade sheet and writing remarks..."):
            try:
                # Optimized System Prompt hardcoded under the hood
                prompt_instructions = """
Input: Image of gradesheet.
Process: Generate end-of-term remarks for each student.

Strict Output Rules:
1. Format MUST strictly be: Name (Rank) : Remark
2. Keep the exact same row order as in the image sheet.
3. Every remark MUST be a single, complete, grammatically correct sentence.
4. Structure Requirement: Start every remark directly with 'He' or 'She' followed by 'is', 'has', 'needs', or 'demonstrates'.
   - Do NOT use fragment phrases (e.g., avoid "A talented student who...").
   - Use 'He' for boys' names and 'She' for girls' names (or 'He/She' if ambiguous).

Examples:
S. ADITI (II) : She is an enthusiastic learner who consistently scores well.
R. DARAN (XVIII) : He needs to focus more on core subjects to improve his rank.
A. RITHANYA (VII) : She demonstrates strong comprehension and maintains high grades.
"""

                # Call Gemini model with image vision capabilities
                response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=[image, prompt_instructions]
                )

                st.success("Remarks generated successfully!")

                # Output section
                st.subheader("Generated Remarks")
                st.code(response.text, language="text")

                # Download button for teachers
                st.download_button(
                    label="📥 Download Remarks as TXT",
                    data=response.text,
                    file_name="student_remarks.txt",
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
