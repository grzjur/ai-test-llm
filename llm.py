from Config import Config
from openai import OpenAI
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

import json
import anthropic

def generate_response(stable, model, chat_history, local_model_path=None):
    try:
        if stable == 'openai':
            messages = [{"role": "user","content": chat_history}]
            llm = OpenAI()
            response = llm.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        elif stable == 'groq':
            prompt = [{"role": "user", "content": chat_history}]
            client = Groq()
            completion = client.chat.completions.create(
                model=model,
                messages=prompt,
                stream=False,
            )
            return completion.choices[0].message.content
        elif stable == "anthropic":
            prompt = [{"role": "user","content":[{"type": "text","text": chat_history}]}]
            client = anthropic.Anthropic(
                api_key=Config.ANTHROPIC_API_KEY,
            )
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=prompt
            )
            return message.content[0].text
        elif stable == 'ollama':
            template = "{question}"
            prompt = ChatPromptTemplate.from_template(template)
            llm = OllamaLLM(model=model)
            chain = prompt | llm
            return chain.invoke({"question": chat_history})
        else:
            raise ValueError("Unsupported response generation model")
    except Exception as e:
        print(f"Failed to generate response: {e}")

def rate_reply(question, modelAnswer, correctAnswer: str):
    messages = [
        {"role": "system",
         "content": """
Jesteś ekspertem oceniającym poprawność odpowiedzi. W danych wejściowych otrzymujesz:
- modelAnswer - odpowiedź jaką udzielił model llm
- correctAnswer - prawidłowa odpowiedź jaką powinien udzielić model

Jeśli odpowiedź modelu (modelAnswer) zgadza się z prawidłową odpowiedzią (correctAnswer) przyznajesz {"correctness":"1"}. Jeśli się nie zgadza przyznajesz {"correctness":"0"}
Odpowiedź podajesz w formacie JSON: {"correctness":"1"} lub {"correctness":"0"}
            """},
        {"role":"user",
         "content": correctAnswer.replace("{modelAnswer}", modelAnswer)
         }
    ]

    #print(messages)
    content=""
    if Config.SUPERVISOR_STABLE == 'openai':
        llm = OpenAI()
        response = llm.chat.completions.create(
            model=Config.SUPERVISOR_MODEL,
            messages=messages
        )
        content = response.choices[0].message.content
    elif Config.SUPERVISOR_STABLE == 'ollama':
        llm = OllamaLLM(model=Config.SUPERVISOR_MODEL, format='json')
        content = llm.invoke(messages)

    #print(content)
    jsonContent = json.loads(content)
    return int(jsonContent['correctness'])
