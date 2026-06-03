import pytesseract
import platform
import time

if platform.system() == "Windows":

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extrair_texto(paginas):

    texto_total = ""

    tempo_total = 0

    for pagina in paginas:

        inicio = time.time()

        texto = pytesseract.image_to_string(
            pagina,
            lang="por"
        )

        fim = time.time()

        tempo_total += (
            fim - inicio
        )

        texto_total += texto + "\n\n"

    tempo_medio = (
        tempo_total /
        len(paginas)
    )

    return {

        "texto": texto_total,

        "tempo_total": round(
            tempo_total,
            2
        ),

        "tempo_medio": round(
            tempo_medio,
            2
        )
    }