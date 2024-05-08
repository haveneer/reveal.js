from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai.api_key)


#
# prompt = f"Ecris moi une conclusion d'un article qui parle de l'utilisation de l'API ChatGPT"
#
# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[{"role": "user", "content": prompt}]
# )
#
# print(completion['choices'][0]['message']['content'])