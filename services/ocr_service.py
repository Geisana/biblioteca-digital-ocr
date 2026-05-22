import pytesseract

def extrair_texto(paginas):

    texto_total = ""

    for pagina in paginas:

        texto = pytesseract.image_to_string(
            pagina,
            lang="por"
        )

        texto_total += texto + "\n\n"

    return texto_total