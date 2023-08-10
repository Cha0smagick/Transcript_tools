from gtts import gTTS
import os

def text_to_speech(text, output_file):
    tts = gTTS(text, lang='es')  # 'es' es el código para el idioma español
    tts.save(output_file)
    print(f"El archivo de audio '{output_file}' ha sido creado exitosamente.")

def main():
    txt_file = input("Por favor, introduce la ruta del archivo .txt: ")
    output_file = input("Por favor, introduce el nombre del archivo de audio de salida (ejemplo: output.mp3): ")

    if txt_file.endswith('.txt'):
        with open(txt_file, 'r', encoding='utf-8') as file:
            text = file.read()
            text_to_speech(text, output_file)
    else:
        print("La ruta proporcionada no parece ser un archivo .txt válido.")

if __name__ == "__main__":
    main()
