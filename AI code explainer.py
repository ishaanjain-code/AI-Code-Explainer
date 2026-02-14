import streamlit as st
import os
import google.generativeai as genai
def configure_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring API: {e}")
        return False
def get_explanation(code_snippet, language):
    model=genai.GenerativeModel('gemini-2.5-flash')
    prompt= prompt = f"""
    You are an expert programming instructor.P1ease explain the following {language} code snippet clearly and concisely.
    Structure your response exactly as follows:

    l.  **summary**: A 1-2 sentence high level overview of what the code does.

    2.  ** line by line breakdown* :Go through the code and explain each significant line is doing. Use bullet points

    3.   *'Key Concepts" :BriefIy list the main programming concepts used(eg., loops, recursion, list comprehensions).

    code snippet:
    ```
    {code_snippet}

    ``` 
    
    """
    try :
        with st.spinner("analyzing code ..."):
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating explanation: {e}"

st.set_page_config(
    page_icon="♠️",
    layout="wide",
)                
def main():
    with st.sidebar:
        st.header("⚙️ settings")
        default_key=os.getenv("GENAI_API_KEY", "")
        api_key=st.text_input(
            "Enter your Google Gemini API Key",
            value= default_key,
            type="password",
            help="Get your key from https://aistudio.google.com/app/apikey"
        )
        st.markdown("---")
        st.markdown(
            "built with [Streamlit] (https://stream.io) and "
            "[Google Gemini](https://deepmind.google/technologies/gemini)."
        )
    st.title("♠️ AI Code Explainer")
    st.markdown("paste a snippet of code below and I'll explain how it works line by line.")
    col1,col2=st.columns([1,1])
    with col1:
        st.subheader("input code")
        language=st.selectbox(
            "select language (optional header)",
            ["Python", "JavaScript", "Java", "C++", "HTML/CSS","SQL", "Other"])
        code_input=st.text_area(
            "paste your code here :",
            height=400,
            placeholder="def hello_world():\n    print('Hello, Streamlit!')"
        )
        analyze_button=st.button("🔍 explain code", type="primary", use_container_width=True)
    with col2:
        st.subheader("code explanation")
        if analyze_button:
            if not api_key:
                st.warning("⚠ Please enter your Gemini API key in the sidebar to proceed.")
            elif not code_input:
                st.warning("⚠ Please paste a code to analyze.")
            else:
                if configure_api_key(api_key):
                    explanation = get_explanation(code_input, language)
                    st.markdown(explanation)


if __name__ == "__main__":
    main()