import streamlit as st
import google.generativeai as genai

f=open(r"C:\Users\vamsh\OneDrive\Desktop\sridhar\innomatics\API_KEYS\api key.txt")
key=f.read()

genai.configure(api_key=key)
""" for m in genai.list_models():
    print(m.name)""" #to see all available models in the vault

model=genai.GenerativeModel(model_name="models/gemini-1.5-pro",
                            system_instruction="""You are an expert code reviewer and Python developer.
When given Python code, analyze it for potential bugs, errors, or areas of improvement.
Provide detailed feedback on the code along with suggestions for fixes and improvements.
If there is any issue, provide a corrected version of the code. 
Also, provide a simple, easy-to-understand explanation of the feedback for beginners.""")
user_prompt=st.text_area("Paste your Python Code here:",
                         placeholder="Type your code here...")
st.title("AI Code Reviewer")
btn_click=st.button("Review Code")
if btn_click:
    if user_prompt.strip()=="":
        st.warning("Please enter some code for review.")
    else:
        try:
            response=model.generate_content(user_prompt)
            st.write("## Review and Suggestions: ")
            st.write(response)
            
        except Exception as e:
            st.error("Error while processing your request. Please try again later.")
            st.error(str(e))