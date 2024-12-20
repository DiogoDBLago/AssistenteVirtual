import speech_recognition as sr
import re
import pyttsx3
from dotenv import load_dotenv
import os
import mysql.connector
import threading

# Carrega variáveis de ambiente
load_dotenv(dotenv_path='config/.env')

# Variáveis globais
ativo = False
lock = threading.Lock()

def esta_ouvindo():
    global ativo
    return ativo

def salvar_nome(nome):
    """Salva o nome no banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome) VALUES (%s)", (nome,))
        conexao.commit()
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conexao.close()

def ouvir_assistente():
    global ativo
    with lock:
        if not ativo:
            ativo = True
            thread = threading.Thread(target=processo_de_ouvir)
            thread.start()

def parar_assistente():
    global ativo
    with lock:
        ativo = False

def processo_de_ouvir():
    global ativo
    engine = pyttsx3.init()
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.luciana")
    nome = ""

    while ativo:
        mic = sr.Recognizer()
        with sr.Microphone() as source:
            mic.adjust_for_ambient_noise(source)
            print("Assistente ouvindo...")
            try:
                audio = mic.listen(source)
                frase = mic.recognize_google(audio, language='pt-BR')
                print(f"Você falou: {frase}")

                if re.search(r'\bajudar\b', frase, re.IGNORECASE):
                    engine.say("Como posso te ajudar?")
                elif re.search(r'\bmeu nome é\b', frase, re.IGNORECASE):
                    match = re.search(r'meu nome é (.*)', frase, re.IGNORECASE)
                    nome = match.group(1).strip() if match else ""
                    salvar_nome(nome)
                    engine.say(f"Prazer em conhecê-lo, {nome}")
                elif re.search(r'\bparar\b', frase, re.IGNORECASE):
                    engine.say("Até mais. Estarei aqui se precisar.")
                    parar_assistente()
                    break
                engine.runAndWait()
            except sr.UnknownValueError:
                print("Não entendi o que foi dito.")
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de fala: {e}")

if __name__ == "__main__":
    ouvir_assistente()
