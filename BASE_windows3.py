import os
import subprocess
import speech_recognition as sr
from gtts import gTTS
import codecs
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style
from gpt4free import you  # Importamos gpt4free
import time  # Importamos la biblioteca time
import whisper

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return codecs.decode(response, 'unicode_escape')

# Función para convertir un archivo a .mp3 (admite mp4, mpg y mp3)
def convert_to_mp3(input_file, output_file):
    try:
        if os.path.isfile(input_file) and input_file.lower().endswith(('.mp4', '.mpg', '.mp3')):
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format='mp3')
            print(f"Conversión exitosa de {input_file} a {output_file}")
        else:
            print("Formato de archivo no compatible. Se admiten archivos .mp4, .mpg y .mp3.")
    except Exception as e:
        print(f"Error al convertir {input_file} a {output_file}: {str(e)}")

# Función para optimizar archivo MP3
def optimizar_audio_mp3(input_file):
    try:
        if os.path.isfile(input_file) and input_file.lower().endswith('.mp3'):
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
            audio.export("audio_optimizado.mp3", format="mp3")

            print(f"El audio optimizado se ha guardado en audio_optimizado.mp3")

        else:
            print("Formato de archivo no compatible. Se admite solo un archivo .mp3.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

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
        print(Fore.MAGENTA + "4) Salir del programa" + Style.RESET_ALL)

        option = input("Selecciona una opción (1/2/3/4): ")

        if option == '1':
            input_file = input("Ingrese la ruta del archivo (MP4, MPG o MP3) a convertir a MP3: ")
            output_file = input("Ingrese el nombre del archivo de salida MP3: ")
            convert_to_mp3(input_file, output_file)
        elif option == '2':
            audio_file = input("Ingrese la ruta del archivo MP3: ")
            optimizar_audio_mp3(audio_file)
        elif option == '3':
            # Solicitar al usuario la ruta del archivo .mp3
            file_path = input("Por favor, ingresa la ruta del archivo .mp3: ")
            model = whisper.load_model("small")  # tiny, base, small, medium, large
            result = model.transcribe(file_path)
            transcribed_text = result["text"]
            print(transcribed_text)
            output_file = "transcripcion.txt"
            with open(output_file, "w") as file:
                file.write(transcribed_text)
            print(f"La transcripción se ha guardado en {output_file}")
        elif option == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
