import os
import subprocess
import speech_recognition as sr
from gtts import gTTS
import codecs
import whisper
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style
from gpt4free import you  # Importamos gpt4free
import time  # Importamos la biblioteca time

# Inicializamos colorama
Fore.RESET

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return codecs.decode(response, 'unicode_escape')

# Función para convertir un archivo a .mp3 (admite mp4, mpg y mp3)
def convert_to_mp3(input_file, output_file):
    try:
        if input_file.lower().endswith(('.mp4', '.mpg', '.mp3')):
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format='mp3')
        else:
            print("Formato de archivo no compatible. Se admiten archivos .mp4, .mpg y .mp3.")
            return

        print(f"Conversión exitosa de {input_file} a {output_file}")
    except Exception as e:
        print(f"Error al convertir {input_file} a {output_file}: {str(e)}")

# Función para optimizar archivo MP3
def optimizar_audio_mp3(input_file):
    try:
        # Cargar el archivo MP3
        audio = AudioSegment.from_mp3(input_file)

        # Aumentar el volumen en 10 dB (ajusta según sea necesario)
        audio = audio + 10

        # Amplificar las frecuencias vocales (acentuar la voz)
        audio = audio.high_pass_filter(500)  # Eliminar frecuencias bajas
        audio = audio.low_pass_filter(5000)  # Eliminar frecuencias altas

        # Reproducir el audio optimizado
        play(audio)

        # Guardar el audio optimizado en un nuevo archivo
        output_path = "audio_optimizado.mp3"
        audio.export(output_path, format="mp3")

        print(f"El audio optimizado se ha guardado en {output_path}")

    except Exception as e:
        print(f"Se produjo un error: {e}")

# Función para cargar y formatear una entrevista desde un archivo .txt
def cargar_entrevista(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as entrevista_file:
            entrevista_text = entrevista_file.read()

        # Preparar el texto para la solicitud al bot
        solicitud_bot = (
            'El texto entre comillas sencillas que te doy a continuación es la transcripción de una entrevista entre dos personas.'
            ' Organiza la entrevista y diferencia el entrevistado del entrevistador, diferenciando la linea que cada uno dijo'
            ' No cambies palabras, ni significados. Lo único que se necesita es que diferencies el entrevistado y el entrevistador lo mejor que puedas dentro de la entrevista. esto mediante separacion de los parrafos o lineas de conversacion de cada uno:'
            f'\n\n"{entrevista_text}"'
        )

        while True:  # Agregamos un bucle para reintentar hasta obtener una respuesta
            # Solicitar análisis al bot
            response = you.Completion.create(prompt=solicitud_bot)
            respuesta_bot = decode_response(response.text)

            if respuesta_bot != "Unable to fetch the response, Please try again.":
                break  # Salir del bucle si la respuesta es diferente de "Unable to fetch the response, Please try again."

            print("No se pudo obtener una respuesta. Reintentando en 5 segundos...")
            time.sleep(5)  # Esperar 5 segundos antes de volver a intentar

        # Guardar el resultado formateado en un nuevo archivo
        with open('entrevista_formateada.txt', 'w', encoding='utf-8') as salida_file:
            salida_file.write(respuesta_bot)

        print("La entrevista ha sido formateada y guardada en 'entrevista_formateada.txt'.")

    except FileNotFoundError:
        print("El archivo de entrevista no se encontró.")
    except Exception as e:
        print("Ocurrió un error al procesar la entrevista:", str(e))

# Función principal del programa
def main():
    while True:
        # Diseño ASCII
        print(Fore.CYAN + r"""
        
██╗███╗   ██╗██╗███████╗
██║████╗  ██║██║██╔════╝
██║██╔██╗ ██║██║█████╗  
██║██║╚██╗██║██║██╔══╝  
██║██║ ╚████║██║██║     
╚═╝╚═╝  ╚═══╝╚═╝╚═╝    

    """ + Style.RESET_ALL)

        print(Fore.GREEN + "¡Bienvenido al programa de análisis de encuestas del INIF! Por favor, elige una opción:")
        print(Fore.YELLOW + "1) Convertir a MP3 (MP4, MPG, MP3)")
        print(Fore.BLUE + "2) Optimización de audio para archivos .mp3")
        print(Fore.RED + "3) Audio a Texto")
        print(Fore.MAGENTA + "4) Optimización semántica de entrevistas")
        print(Fore.RED+ "5) Realizar todos los procesos (1, 2, 3, 4)")
        print(Fore.MAGENTA + "6) Salir del programa" + Style.RESET_ALL)

        option = input("Selecciona una opción (1/2/3/4/5/6): ")

        if option == '1':
            input_file = input("Ingrese la ruta del archivo (MP4, MPG o MP3) a convertir a MP3: ")
            if not os.path.isfile(input_file):
                print("El archivo no existe")
                continue
            output_file = input("Ingrese el nombre del archivo de salida MP3: ")
            convert_to_mp3(input_file, output_file)
        elif option == '2':
            audio_file = input("Ingrese la ruta del archivo MP3: ")
            if not os.path.isfile(audio_file):
                print("El archivo no existe")
                continue
            optimizar_audio_mp3(audio_file)
        elif option == '3':
            # Solicitar al usuario la ruta del archivo .mp3
            file_path = input("Por favor, ingresa la ruta del archivo .mp3: ")

            # Cargar el modelo Whisper
            model = whisper.load_model("small")  # tiny, base, small, medium, large

            # Transcribir el archivo de audio
            result = model.transcribe(file_path)

            # Obtener el texto transcribido
            transcribed_text = result["text"]

            # Imprimir el texto transcribido
            print(transcribed_text)

            # Exportar el texto a un archivo .txt
            output_file = "transcripcion.txt"
            with open(output_file, "w") as file:
                file.write(transcribed_text)

            print(f"La transcripción se ha guardado en {output_file}")
        elif option == '4':
            # Solicitar al usuario la ruta del archivo de entrevista
            ruta_archivo_entrevista = input("Por favor, ingrese la ruta completa del archivo de la entrevista (debe estar en formato .txt): ")
            cargar_entrevista(ruta_archivo_entrevista)
        elif option == '5':
            # Realizar todos los procesos consecutivamente
            input_file = input("Ingrese la ruta del archivo (MP4, MPG o MP3) a convertir a MP3: ")
            if not os.path.isfile(input_file):
                print("El archivo no existe")
                continue
            output_file = "audio_optimizado.mp3"
            convert_to_mp3(input_file, output_file)
            optimizar_audio_mp3(output_file)
            transcribed_text = ""
            try:
                # Cargar el modelo Whisper
                model = whisper.load_model("small")  # tiny, base, small, medium, large

                # Transcribir el archivo de audio optimizado
                result = model.transcribe(output_file)

                # Obtener el texto transcribido
                transcribed_text = result["text"]
                print("Transcripción de audio optimizado:")
                print(transcribed_text)
            except Exception as e:
                print("Error al transcribir el audio optimizado:", str(e))

            if transcribed_text:
                with open('transcripcion_optimizada.txt', 'w', encoding='utf-8') as salida_file:
                    salida_file.write(transcribed_text)
                    print("La transcripción optimizada se ha guardado en 'transcripcion_optimizada.txt'.")

            # Realizar optimización semántica de entrevistas
            cargar_entrevista('transcripcion_optimizada.txt')
        elif option == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
