import os
import streamlit as st
from pydub import AudioSegment
import tempfile
import whisper

# Inicializamos colorama
st.set_option('deprecation.showfileUploaderEncoding', False)

# Función para decodificar la respuesta en texto legible
def decode_response(response):
    return response.decode('unicode_escape')

# Función para convertir un archivo a .mp3 (admite mp4, mpg y mp3)
def convert_to_mp3(input_file, output_file):
    try:
        if input_file.name.lower().endswith(('.mp4', '.mpg', '.mp3')):
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format='mp3')
            st.success(f"Conversión exitosa de {input_file.name} a {output_file}")

            # Botón de descarga
            st.download_button(label="Descargar archivo MP3", data=audio.export(format="mp3").read(),
                               file_name=output_file, key='convert_to_mp3')

        else:
            st.error("Formato de archivo no compatible. Se admiten archivos .mp4, .mpg y .mp3.")
            return

    except Exception as e:
        st.error(f"Error al convertir {input_file.name} a {output_file}: {str(e)}")

# Función para optimizar archivo MP3
def optimizar_audio_mp3(input_file):
    try:
        # Cargar el archivo MP3
        audio = AudioSegment.from_mp3(input_file.read())

        # Aumentar el volumen en 10 dB (ajusta según sea necesario)
        audio = audio + 10

        # Amplificar las frecuencias vocales (acentuar la voz)
        audio = audio.high_pass_filter(500)  # Eliminar frecuencias bajas
        audio = audio.low_pass_filter(5000)  # Eliminar frecuencias altas

        # Reproducir el audio optimizado
        st.audio(audio.export(format="mp3").read(), format="audio/mp3")

        # Guardar el audio optimizado en un nuevo archivo
        output_path = "audio_optimizado.mp3"
        audio.export(output_path, format="mp3")

        st.success(f"El audio optimizado se ha guardado en {output_path}")

        # Botón de descarga
        st.download_button(label="Descargar audio optimizado", data=audio.export(format="mp3").read(),
                           file_name=output_path, key='optimizar_audio_mp3')

    except Exception as e:
        st.error(f"Se produjo un error: {e}")

# Función para transcribir audio a texto
def transcribir_audio(file_path):
    try:
        st.info("Transcribiendo... Esto puede tomar un momento.")
        progress_bar = st.progress(0)  # Barra de progreso inicializada
        progress_text = st.empty()  # Espacio para el texto de progreso

        # Crear un archivo temporal para almacenar el contenido del archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            audio = AudioSegment.from_mp3(file_path.read())
            audio.export(temp_wav.name, format="wav")

            # Cargar el modelo Whisper
            model = whisper.load_model("small")  # Ajusta el tamaño del modelo según sea necesario

            # Transcribir el archivo de audio
            result = model.transcribe(temp_wav.name)

        # Obtener el texto transcribido
        transcribed_text = result["text"]

        # Mostrar el texto transcribido
        st.subheader("Texto Transcrito:")
        st.text(transcribed_text)

        # Exportar el texto a un archivo .txt
        output_file = "transcripcion.txt"
        with open(output_file, "w") as file:
            file.write(transcribed_text)

        st.success(f"La transcripción se ha guardado en {output_file}")

        # Botón de descarga
        st.download_button(
            label="Descargar transcripción",
            data=transcribed_text.encode("utf-8"),
            file_name=output_file,
            key='transcripcion'
        )

    except Exception as e:
        st.error(f"Se produjo un error durante la transcripción: {e}")

    finally:
        progress_text.empty()  # Limpiar el espacio de texto de progreso al finalizar

# Función principal del programa
def main():
    st.title("Programa de Análisis de Encuestas del INIF")

    option = st.sidebar.selectbox("Selecciona una opción", ["Convertir a MP3", "Optimización de audio para archivos .mp3", "Audio a Texto", "Salir del programa"])

    if option == "Convertir a MP3":
        input_file = st.file_uploader("Cargar archivo (MP4, MPG o MP3) a convertir a MP3", type=["mp4", "mpg", "mp3"])
        if input_file is not None:
            output_file = st.text_input("Ingrese el nombre del archivo de salida MP3:")
            if st.button("Convertir"):
                convert_to_mp3(input_file, output_file)

    elif option == "Optimización de audio para archivos .mp3":
        audio_file = st.file_uploader("Cargar archivo MP3 a optimizar", type=["mp3"])
        if audio_file is not None:
            if st.button("Optimizar"):
                optimizar_audio_mp3(audio_file)

    elif option == "Audio a Texto":
        file_path = st.file_uploader("Cargar archivo .mp3 para transcribir", type=["mp3"])
        if file_path is not None:
            if st.button("Transcribir"):
                transcribir_audio(file_path)

    elif option == "Salir del programa":
        st.text("Saliendo del programa.")

if __name__ == "__main__":
    main()
