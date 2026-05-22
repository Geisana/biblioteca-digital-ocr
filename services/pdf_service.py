import pytesseract

# caminho do tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extrair_texto(paginas):

    texto_total = ""

    for pagina in paginas:

        texto = pytesseract.image_to_string(
            pagina,
            lang="por"
        )

        texto_total += texto + "\n\n"

    return texto_total