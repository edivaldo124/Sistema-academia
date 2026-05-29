
import sys, os

from google import genai

from dotenv import load_dotenv



load_dotenv()

client = genai.Client(api_key=os.getenv("AIzaSyDv7Wu_UcTVhxGVwMP37aYung1NEJ4Tcf4"))



def chat():

    model = client.chats.create(model="gemini-2.5-flash")

    print("--- Gemini Chat Iniciado ---")

    while True:

        try:

            msg = input("Você: ")

            if msg.lower() in ['sair', 'exit']: break

            print("Gemini:", model.send_message(msg).text)

        except Exception as e:

            print(f"Erro: {e}")



if __name__ == "__main__":

    if len(sys.argv) > 1:

        # Modo análise rápida: lê um arquivo e envia para a IA

        with open(sys.argv[1], 'r') as f:

            print(client.models.generate_content(

                model='gemini-2.5-flash',

                contents=f"Analise o código abaixo e sugira melhorias:\n{f.read()}"

            ).text)

    else:

        chat()

