from bardapi import Bard

# Pide al usuario la ruta del archivo .txt
file_path = input("Introduce la ruta del archivo .txt: ")

# Lee el contenido del archivo en una variable
file_content = open(file_path).read()

# Crea una instancia de Bard
bard = Bard(token_from_browser=True)

# Obtén la respuesta de Bard
res = bard.get_answer("Corrige la coherencia semantica, puntuacion y diccion del siguiente texto, sin cambiar ni agregar ninguna palabra nueva. tambien realiza la separacion por parrafos y corrige ortografia y gramatica. no me respondas, limitate a hacer lo que te digo. no inventes nada, solo haz lo que te digo. no extiendas el texto de ninguna manera." + file_content)

# Imprime la respuesta de Bard
print(res)
