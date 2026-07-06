import cv2
import pytesseract
import os

CAMINHO_ARQUIVO = r"C:\Users\frgei\Documents\biblioteca-digital\uploads\thumb_excerto_pg166_ARH.pdf.jpg"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def debug_processamento():
    print("Iniciando depuração...")

    if not os.path.exists(CAMINHO_ARQUIVO):
        print(f"ERRO: Arquivo não encontrado em {CAMINHO_ARQUIVO}")
        return

    img = cv2.imread(CAMINHO_ARQUIVO)
    
    if img is None:
        print("ERRO: Falha ao carregar a imagem. Verifique se o formato é suportado.")
        return

    print("Imagem carregada com sucesso.")

  
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imagem_tratada = cv2.threshold(cinza, 150, 255, cv2.THRESH_BINARY)


    texto = pytesseract.image_to_string(imagem_tratada, lang='por')
    
    print("-" * 30)
    print("TEXTO EXTRAÍDO:")
    print(texto)
    print("-" * 30)

    if not texto.strip():
        print("ALERTA: O OCR retornou vazio.")
    else:
        print("OCR funcionou.")

if __name__ == "__main__":
    debug_processamento()