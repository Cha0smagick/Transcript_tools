import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style
import codecs
import streamlit as st
import whisper
import uuid

# Inicializamos colorama
Fore.RESET

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return codecs.decode(response, 'unicode_escape')

# Función para convertir cualquier formato de audio a .mp3
def convert_to_mp3(input_file):
    try:
        audio = AudioSegment.from_file(input_file)
        
        # Obtener el nombre base del archivo sin la extensión
        base_file_name = os.path.splitext(input_file.name)[0]
        
        # Agregar la extensión .mp3 al nombre base del archivo
        output_file_name = base_file_name + ".mp3"
        
        audio.export(output_file_name, format='mp3')
        st.success(f"Conversión exitosa a {output_file_name}")

        # Botón de descarga
        st.download_button(label=f"Descargar {output_file_name}", data=audio.export(format="mp3").read(),
                           file_name=output_file_name, key='convert_to_mp3')

    except Exception as e:
        st.error(f"Error al convertir el archivo: {str(e)}")

# Función para optimizar archivo MP3
def optimizar_audio_mp3(input_file):
    try:
        # Cargar el archivo MP3
        audio = AudioSegment.from_mp3(input_file.name)

        # Aumentar el volumen en 10 dB (ajusta según sea necesario)
        audio = audio + 10

        # Amplificar las frecuencias vocales (acentuar la voz)
        audio = audio.high_pass_filter(500)  # Eliminar frecuencias bajas
        audio = audio.low_pass_filter(5000)  # Eliminar frecuencias altas

        # Reproducir el audio optimizado
        play(audio)

        # Obtener el nombre base del archivo sin la extensión
        base_file_name = os.path.splitext(input_file.name)[0]

        # Generar un nombre de archivo único para el audio optimizado
        output_file_name = base_file_name + "_optimizado.mp3"
        audio.export(output_file_name, format="mp3")

        st.success(f"El audio optimizado se ha guardado en {output_file_name}")

        # Botón de descarga
        st.download_button(label=f"Descargar {output_file_name}", data=audio.export(format="mp3").read(),
                           file_name=output_file_name, key='optimizar_audio_mp3')

    except Exception as e:
        st.error(f"Se produjo un error: {e}")

# Función para transcribir archivo de audio a texto
def transcribir_audio_a_texto(file_path):
    try:
        # Cargar el modelo Whisper
        model = whisper.load_model("small")  # tiny, base, small, medium, large

        # Transcribir el archivo de audio
        result = model.transcribe(file_path.name)

        # Obtener el texto transcribido
        transcribed_text = result["text"]

        # Imprimir el texto transcribido
        st.text(transcribed_text)

        # Generar un nombre de archivo único para la transcripción
        base_file_name = os.path.splitext(file_path.name)[0]
        output_file_name = base_file_name + "_transcripcion.txt"

        # Exportar el texto a un archivo .txt
        with open(output_file_name, "w") as file:
            file.write(transcribed_text)

        st.success(f"La transcripción se ha guardado en {output_file_name}")

        # Botón de descarga
        st.download_button(label=f"Descargar {output_file_name}", data=transcribed_text.encode("utf-8"),
                           file_name=output_file_name, key='transcripcion')

    except Exception as e:
        st.error(f"Se produjo un error: {e}")

# Función principal del programa
def main():
    st.title("AUDIO2TEXT - Transcripción de archivos Multimedia para INIF")

    # Agregar el logotipo centrado justo arriba del título
    st.image("https://i.ibb.co/2j2gGW1/logo-inif.png", use_column_width=True)

    # Botones en la sidebar
    convert_button = st.sidebar.button("Convertir a MP3")
    optimize_button = st.sidebar.button("Optimización de audio para archivos .mp3")
    transcribe_button = st.sidebar.button("Audio a Texto")

    if convert_button:
        input_file = st.file_uploader("Cargar archivo de audio para convertir a MP3", type=["mp3", "m4a", "wav", "flac", "ogg", "aac"])
        if input_file is not None:
            if st.button("Convertir"):
                convert_to_mp3(input_file)

    elif optimize_button:
        audio_file = st.file_uploader("Cargar archivo MP3 a optimizar", type=["mp3"])
        if audio_file is not None:
            if st.button("Optimizar"):
                optimizar_audio_mp3(audio_file)

    elif transcribe_button:
        file_path = st.file_uploader("Cargar archivo .mp3 para transcribir", type=["mp3"])
        if file_path is not None:
            if st.button("Transcribir"):
                transcribir_audio_a_texto(file_path)

if __name__ == "__main__":
    main()
