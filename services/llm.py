from google import genai
from google.genai import types
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def geminiCall(prompt:str,api_instruct:str)->str:
    response = client.models.generate_content(
        model=st.secrets["GEMINI_MODEL"],
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=api_instruct,
            max_output_tokens=st.secrets["MAXTOKEN"],
            temperature=st.secrets["TEMPERATURE"],
        )
    )
    if not response:
        return 'No SQL Generated'
    
    generated_recipe = response.text
    return generated_recipe
