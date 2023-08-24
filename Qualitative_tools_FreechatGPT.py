import os
import subprocess
import speech_recognition as sr
from gtts import gTTS
import codecs
from gpt4free import you
from bardapi import Bard
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play

bard_api_token = 'TU_TOKEN_DE_API_BARD'

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return codecs.decode(response, 'unicode_escape')

def audio_to_text_and_transcribe(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No se pudo reconocer el audio"
        except sr.RequestError as e:
            return f"Error al solicitar el servicio de Google: {e}"

# Función texto a audio
def text_to_speech(text, output_file):
    tts = gTTS(text, lang='es')
    tts.save(output_file)
    print(f"El archivo de audio '{output_file}' ha sido creado exitosamente.")

# Función para mejorar texto con ChatGPT
def mejorar_texto_with_openai(input_text):
    parrafos = input_text.split('\n\n')
    parrafos_mejorados = []

    # chatbot
    chat = []

    for parrafo in parrafos:
        # Solicitar la mejora al modelo ChatGPT
        response = you.Completion.create(
            prompt=parrafo,
            chat=chat
        )
        parrafo_mejorado = decode_response(response.text).strip()
        parrafos_mejorados.append(parrafo_mejorado)

        # Agregar la respuesta al chat
        chat.append({"role": "system", "content": "You: " + parrafo})
        chat.append({"role": "system", "content": "ChatGPT: " + parrafo_mejorado})

    texto_mejorado = '\n\n'.join(parrafos_mejorados)
    return texto_mejorado

# Función para mejorar texto con Bard
def mejorar_texto_with_bard(input_file_path):
    bard = Bard(token_from_browser=True)
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()
    res = bard.get_answer(input_text)
    corrected_text = res['text']
    output_file_path = os.path.splitext(input_file_path)[0] + "_corregido.txt"
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(corrected_text)
    return output_file_path

# Función para convertir un archivo a .wav (admite mp4, mpg y mp3)
def convert_to_wav(input_file, output_file):
    try:
        if input_file.lower().endswith(('.mp4', '.mpg')):
            video = VideoFileClip(input_file)
            audio = video.audio
            audio.write_audiofile(output_file, codec='pcm_s16le')
        elif input_file.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(input_file)
            audio.export(output_file, format='wav')
        else:
            print("Formato de archivo no compatible. Se admiten archivos .mp4, .mpg y .mp3.")
            return

        print(f"Conversión exitosa de {input_file} a {output_file}")
    except Exception as e:
        print(f"Error al convertir {input_file} a {output_file}: {str(e)}")

# Función para optimizar archivo WAV
def optimizar_audio_wav(input_file):
    try:
        # Cargar el archivo WAV
        audio = AudioSegment.from_wav(input_file)

        # Aumentar el volumen en 10 dB (ajusta según sea necesario)
        audio = audio + 10

        # Amplificar las frecuencias vocales (acentuar la voz)
        audio = audio.high_pass_filter(500)  # Eliminar frecuencias bajas
        audio = audio.low_pass_filter(5000)  # Eliminar frecuencias altas

        # Reproducir el audio optimizado
        play(audio)

        # Guardar el audio optimizado en un nuevo archivo
        output_path = "audio_optimizado.wav"
        audio.export(output_path, format="wav")

        print(f"El audio optimizado se ha guardado en {output_path}")

    except Exception as e:
        print(f"Se produjo un error: {e}")

# Función principal del programa
def main():
    while True:
        print("¡Bienvenido al programa de análisis de encuestas del INIF! Por favor, elige una opción:")
        print("1) Convertir a WAV (MP4, MPG, MP3)")
        print("2) Optimización de audio para archivos .wav")
        print("3) Audio a Texto")
        print("4) Optimización Semántica")
        print("5) BONUS: Texto a Audio")
        print("6) Salir del programa")

        option = input("Selecciona una opción (1/2/3/4/5/6): ")

        if option == '1':
            input_file = input("Ingrese la ruta del archivo (MP4, MPG o MP3) a convertir a WAV: ")
            if not os.path.isfile(input_file):
                print("El archivo no existe")
                continue
            output_file = input("Ingrese el nombre del archivo de salida WAV: ")
            convert_to_wav(input_file, output_file)
        elif option == '2':
            audio_file = input("Ingrese la ruta del archivo WAV: ")
            if not os.path.isfile(audio_file):
                print("El archivo no existe")
                continue
            optimizar_audio_wav(audio_file)
        elif option == '3':
            audio_file = input("Ingrese la ruta del archivo WAV: ")
            if not os.path.isfile(audio_file):
                print("El archivo no existe")
                continue
            transcription = audio_to_text_and_transcribe(audio_file)
            txt_file = os.path.splitext(audio_file)[0] + ".txt"
            with open(txt_file, "w") as f:
                f.write(transcription)
            print(f"Transcripción completada. El archivo de texto se encuentra en: {txt_file}")
        elif option == '4':
            print("Selecciona el motor de optimización semántica:")
            print("1) ChatGPT")
            print("2) Bard AI")
            sub_option = input("Selecciona una opción (1/2): ")
            if sub_option == '1':
                input_file_path = input("Ingresa la ruta del archivo .txt: ")
                if not os.path.isfile(input_file_path):
                    print("El archivo no existe")
                    continue
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    input_text = file.read()
                improved_text = mejorar_texto_with_openai(input_text)
                output_file_path = os.path.splitext(input_file_path)[0] + "_optimizado_chatgpt.txt"
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(improved_text)
                print(f"Texto optimizado por ChatGPT y guardado en: {output_file_path}")
            elif sub_option == '2':
                input_file_path = input("Ingresa la ruta del archivo .txt: ")
                if not os.path.isfile(input_file_path):
                    print("El archivo no existe")
                    continue
                output_file_path = mejorar_texto_with_bard(input_file_path)
                print(f"Texto corregido por Bard AI y guardado en: {output_file_path}")
            else:
                print("Opción no válida.")
        elif option == '5':
            txt_file = input("Por favor, introduce la ruta del archivo .txt: ")
            output_file = input("Por favor, introduce el nombre del archivo de audio de salida: ")
            if txt_file.endswith('.txt'):
                with open(txt_file, 'r', encoding='utf-8') as file:
                    text = file.read()
                    text_to_speech(text, output_file)
                print(f"Archivo de audio '{output_file}' ha sido creado exitosamente.")
            else:
                print("La ruta proporcionada no parece ser un archivo .txt válido.")
        elif option == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
