import streamlit as st
import google.generativeai as genai

# Load API key
'''
with open(r"C:\Users\vamsh\OneDrive\Desktop\sridhar\innomatics\API_KEYS\api key.txt") as f:
    key = f.read()
genai.configure(api_key=key)
'''
# Retrieve the API key from Streamlit secrets
api_key = st.secrets["API_KEY"]

# Configure the Generative AI API with the API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro",
    system_instruction="""You are an expert code reviewer and Python developer.
When given Python code, analyze it for potential bugs, errors, or areas of improvement.
Provide detailed feedback on the code along with suggestions for fixes and improvements.
If there is any issue, provide a corrected version of the code.
Also, provide a simple, easy-to-understand explanation of the feedback for beginners."""
)

st.title("AI Code Reviewer")

# Input section for code
user_prompt = st.text_area("Paste your Python Code here:", placeholder="Type your code here...")

# Button to initiate code review
btn_click = st.button("Review Code")

# Handle button click
if btn_click:
    if user_prompt.strip() == "":
        st.warning("Please enter some code for review.")
    else:
        try:
            # Generate response from the model
            response = model.generate_content(user_prompt)

            # Access content safely
            if response and response.candidates and hasattr(response.candidates[0], 'content'):
                detailed_feedback = response.candidates[0].content.parts[0].text  # Accessing the actual text part

                # Display the detailed feedback with code
                st.write("## Review and Suggestions:")
                st.code(detailed_feedback)

                # Provide a plain-English explanation for beginners
                st.write("### Plain-English Explanation:")
                beginner_friendly_explanation = """
                Here are the main takeaways from the feedback:
                1. **Code Quality and Readability**: Suggestions on how to make the code more readable, like using clear variable names, comments, and avoiding complex logic where possible.
                2. **Security Enhancements**: Avoid storing sensitive information, such as API keys, directly in the code. Instead, use environment variables to keep it secure.
                3. **Error Handling**: Include robust error handling to gracefully handle issues that might arise during execution. This improves user experience and makes the code more reliable.
                4. **Functionality Optimization**: Tips on reducing redundant code or improving efficiency.
                5. **Code Structure and Organization**: Recommendations on organizing code in a way that is easier to understand and maintain.

                In summary, the feedback points out any bugs or areas of improvement and provides suggestions for writing cleaner and safer Python code.
                """
                st.write(beginner_friendly_explanation)

                # Style suggestions for improving the app's design
                st.write("### Additional Style Suggestions:")
                st.write("""
                1. **Add a Sidebar**: Move options to a sidebar for a cleaner layout.
                2. **Use Background Colors or Themes**: Use Streamlit's theme options for better visual appeal.
                3. **Improved Button Styling**: Adjust the button size, color, or alignment for emphasis.
                4. **Output Formatting**: Use Markdown or other formatting options for clearer output sections.
                """)
                
                # Code to implement suggested styling changes
                st.write("Here's an example code to apply some of these style improvements:")

                st.code("""
# Example of adding a sidebar and theme settings
import streamlit as st

st.set_page_config(page_title="AI Code Reviewer", layout="wide", initial_sidebar_state="expanded")

# Sidebar for additional options
with st.sidebar:
    st.title("AI Code Reviewer Options")
    st.button("Review Code")  # You can add more options in the sidebar

# Main layout adjustments
st.markdown("<style>body { background-color: #f4f4f4; }</style>", unsafe_allow_html=True)
st.title("AI Code Reviewer with Enhanced Style")
st.write("Use `st.markdown` for formatted text output.")
                """, language="python")

            else:
                st.warning("The model did not provide a response. Please try again or rephrase your code.")

        except Exception as e:
            st.error("Error while processing your request. Please try again later.")
            st.error(str(e))
