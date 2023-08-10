import os
import subprocess
import speech_recognition as sr

def convert_to_wav(audio_file):
    wav_file = os.path.splitext(audio_file)[0] + ".wav"
    subprocess.run(["ffmpeg", "-i", audio_file, "-acodec", "pcm_s16le", "-ar", "16000", wav_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_file

def audio_to_text(audio_file):
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

def main():
    audio_file = input("Ingrese la ruta del archivo de audio: ")

    if not os.path.isfile(audio_file):
        print("El archivo no existe")
        return

    # Convertir a formato WAV
    wav_file = convert_to_wav(audio_file)

    # Realizar la transcripción
    transcription = audio_to_text(wav_file)

    # Eliminar el archivo WAV generado
    os.remove(wav_file)

    # Crear el archivo de texto
    txt_file = os.path.splitext(audio_file)[0] + ".txt"
    with open(txt_file, "w") as f:
        f.write(transcription)

    print(f"Transcripción completada. El archivo de texto se encuentra en: {txt_file}")

if __name__ == "__main__":
    main()
