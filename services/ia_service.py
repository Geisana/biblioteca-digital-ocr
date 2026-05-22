import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

modelo = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def gerar_resumo(texto):

    prompt = f"""
    Resuma o texto abaixo:

    {texto[:15000]}
    """

    try:
        resposta = modelo.generate_content(prompt)
        return resposta.text

    except Exception as e:
        return f"Erro IA: {e}"