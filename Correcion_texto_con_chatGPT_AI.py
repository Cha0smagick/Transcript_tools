import openai

# Configuración de la API de OpenAI
openai.api_key = 'TU_CLAVE_DE_API_AQUI'

def mejorar_texto(input_text):
    # Dividir el texto en párrafos
    parrafos = input_text.split('\n\n')

    # Procesar cada párrafo por separado
    parrafos_mejorados = []
    for parrafo in parrafos:
        # Mejorar el párrafo utilizando OpenAI
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=parrafo,
            max_tokens=100  # Ajusta según sea necesario
        )
        parrafo_mejorado = respuesta.choices[0].text.strip()
        parrafos_mejorados.append(parrafo_mejorado)

    # Unir los párrafos mejorados de nuevo en un texto coherente
    texto_mejorado = '\n\n'.join(parrafos_mejorados)

    return texto_mejorado

# Pedir al usuario la ruta del archivo de entrada
ruta_archivo = input("Por favor, ingresa la ruta del archivo de entrada (.txt): ")

# Cargar el texto desde el archivo .txt
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    texto_original = archivo.read()

# Mejorar el texto
texto_mejorado = mejorar_texto(texto_original)

# Guardar el texto mejorado en un nuevo archivo
ruta_salida = 'salida_mejorada.txt'
with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
    archivo_salida.write(texto_mejorado)

print(f"Proceso completado. Texto mejorado guardado en '{ruta_salida}'.")
