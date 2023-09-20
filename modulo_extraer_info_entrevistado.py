import time
import codecs
from gpt4free import you

# Función para obtener una respuesta sin "Unable to fetch the response, Please try again."
def obtener_respuesta(prompt, chat):
    while True:
        response = you.Completion.create(
            prompt=prompt,
            chat=chat
        )
        text = response.text.strip()
        if text != "Unable to fetch the response, Please try again.":
            return text

        time.sleep(5)  # Espera 5 segundos antes de intentar nuevamente

# Inicializar el chat vacío
chat = []

# Pedir al usuario la ruta del archivo .txt
archivo_txt = input("Por favor, ingresa la ruta del archivo .txt: ")

try:
    with open(archivo_txt, "r", encoding="utf-8") as archivo_entrada:
        contenido = archivo_entrada.read()
except FileNotFoundError:
    print("El archivo especificado no se encontró.")
    exit()

# Agregar el contenido del archivo al chat
chat.append({"question": contenido, "answer": ""})

# Filtrar el contenido eliminando las líneas del entrevistador
contenido_filtrado = "\n".join([linea for linea in contenido.splitlines() if not linea.strip().startswith("Entrevistador:")])

# Obtener respuesta del modelo
respuesta_bot = obtener_respuesta("Actúa como un experto en formateo de entrevistas. Voy a darte un texto de una entrevista a continuacion con labels de entrevistado y entrevistador. relee la entrevista. elimina todo el texto relacionado con el entrevistador y devuelve solo el texto relacionado con el entrevistado, sin etiquetas y en un parrafo de seguido. el texto con el que debes hacer esto es el siguiente: ", chat)

# Imprimir la respuesta formateada en la consola
respuesta_bot_legible = codecs.decode(respuesta_bot, 'unicode_escape')
print("Bot:", respuesta_bot_legible)

# Guardar la respuesta en un archivo de salida con el formato adecuado
with codecs.open("respuestas.txt", "w", "utf-8") as archivo_respuestas:
    archivo_respuestas.write(f"Entrada:\n{contenido}\n")
    archivo_respuestas.write(f"Salida:\n{respuesta_bot_legible}\n")

print("Conversación guardada en 'respuestas.txt'")

