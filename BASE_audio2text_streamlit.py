import os
import codecs
import tempfile
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style
from moviepy.editor import VideoFileClip
import whisper

# Inicializamos colorama
Fore.RESET

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return codecs.decode(response, 'unicode_escape')

# Función para convertir cualquier formato de audio o video a .mp3
def convert_to_mp3(input_file):
    try:
        # Guardar el archivo subido en una ubicación temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.name)[1]) as tmp_file:
            tmp_file.write(input_file.getvalue())
            tmp_file_path = tmp_file.name

        # Determinar si el archivo es de video o audio y procesarlo
        if any(tmp_file_path.endswith(ext) for ext in ["mp4", "avi", "mov", "flv", "mkv"]):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_tmp_file:
                video = VideoFileClip(tmp_file_path)
                video.audio.write_audiofile(audio_tmp_file.name)
                audio = AudioSegment.from_wav(audio_tmp_file.name)
        else:
            audio = AudioSegment.from_file(tmp_file_path)

        base_file_name = os.path.splitext(input_file.name)[0]
        output_file_name = base_file_name + ".mp3"
        audio.export(output_file_name, format='mp3')
        st.success(f"Conversión exitosa a {output_file_name}")
        st.download_button(label=f"Descargar {output_file_name}", data=audio.export(format="mp3").read(),
                           file_name=output_file_name, key='convert_to_mp3')
    except Exception as e:
        st.error(f"Error al convertir el archivo: {str(e)}")

# Función para optimizar archivo MP3
def optimizar_audio_mp3(input_file):
    try:
        audio = AudioSegment.from_mp3(input_file.name)
        audio = audio + 10
        audio = audio.high_pass_filter(500)
        audio = audio.low_pass_filter(5000)
        play(audio)
        base_file_name = os.path.splitext(input_file.name)[0]
        output_file_name = base_file_name + "_optimizado.mp3"
        audio.export(output_file_name, format="mp3")
        st.success(f"El audio optimizado se ha guardado en {output_file_name}")
        st.download_button(label=f"Descargar {output_file_name}", data=audio.export(format="mp3").read(),
                           file_name=output_file_name, key='optimizar_audio_mp3')
    except Exception as e:
        st.error(f"Se produjo un error: {e}")

# Función principal del programa
def main():
    st.title("AUDIO2TEXT - Transcripción de archivos Multimedia para INIF")
    st.image("https://i.ibb.co/2j2gGW1/logo-inif.png", use_column_width=True)

    option = st.sidebar.selectbox("Selecciona una opción", ["Convertir a MP3", "Optimización de audio para archivos .mp3", "Audio a Texto"])

    if option == "Convertir a MP3":
        input_file = st.file_uploader("Cargar archivo de audio o video para convertir a MP3", type=["mp3", "m4a", "wav", "flac", "ogg", "aac", "mp4", "avi", "mov", "flv", "mkv"])
        if input_file is not None:
            if st.button("Convertir"):
                convert_to_mp3(input_file)

    elif option == "Optimización de audio para archivos .mp3":
        audio_file = st.file_uploader("Cargar archivo MP3 a optimizar", type=["mp3"])
        if audio_file is not None:
            if st.button("Optimizar"):
                optimizar_audio_mp3(audio_file)

    elif option == "Audio a Texto":
        file_path = st.file_uploader("Cargar archivo .mp3 para transcribir", type=["mp3"])
        if file_path is not None:
            if st.button("Transcribir"):
                try:
                    # Guardar el archivo en una ubicación temporal
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        tmp_file.write(file_path.getvalue())
                        audio_file_path = tmp_file.name

                    # Cargar y transcribir el audio
                    model = whisper.load_model("small")
                    result = model.transcribe(audio_file_path)
                    transcribed_text = result["text"]
                    st.text(transcribed_text)

                    # Guardar la transcripción en un archivo
                    base_file_name = os.path.splitext(file_path.name)[0]
                    output_file_name = base_file_name + "_transcripcion.txt"
                    with open(output_file_name, "w") as file:
                        file.write(transcribed_text)
                    st.success(f"La transcripción se ha guardado en {output_file_name}")
                    st.download_button(label=f"Descargar {output_file_name}", data=transcribed_text.encode("utf-8"),
                                       file_name=output_file_name, key='transcripcion')
                except Exception as e:
                    st.error(f"Se produjo un error al transcribir el audio: {e}")

if __name__ == "__main__":
    main()
