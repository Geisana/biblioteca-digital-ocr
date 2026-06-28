# preprocessamento/filtros.py
import cv2
import numpy as np

def para_cinza(img):
    img = np.array(img)
    if len(img.shape) == 2:
        return img  
    if img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    return img

def binarizar(img_cinza):
    """Transforma tudo em preto ou branco absoluto (ótimo para texto apagado)"""
    # Usando o método de Otsu para encontrar o limite perfeito automaticamente
    _, img_bin = cv2.threshold(img_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_bin

def remover_ruido(img):
    """Remove pontinhos e sujeiras da imagem escaneada"""
    return cv2.medianBlur(img, 3)

def aumentar_resolucao(img, escala=1.5):
    """Aumenta o tamanho da imagem para o Tesseract enxergar melhor letras pequenas."""
    largura = int(img.shape[1] * escala)
    altura = int(img.shape[0] * escala)
    # INTER_CUBIC é um algoritmo excelente para manter a borda das letras suaves
    return cv2.resize(img, (largura, altura), interpolation=cv2.INTER_CUBIC)

def aumentar_contraste(img_cinza):
    """Melhora a legibilidade de textos desbotados."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(img_cinza)

def remover_ruido_bilateral(img):
    """
    Remove ruído preservando as bordas das letras.
    d: Diâmetro da vizinhança de pixel.
    sigmaColor: Filtro de cor (maior = mais mistura de cores).
    sigmaSpace: Filtro de coordenadas (maior = pixels distantes influenciam uns aos outros).
    """
    return cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)


def extrair_coordenadas(scores, geometry, min_confidence):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        # Aqui o seu modelo só tem 4 canais, logo índices 0, 1, 2, 3
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]

        for x in range(0, numCols):
            if scoresData[x] < min_confidence:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            
            # Cálculo simplificado (sem ângulo)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            
            startX = int(offsetX - xData3[x])
            startY = int(offsetY - xData0[x])
            
            rects.append((startX, startY, int(w), int(h)))
            confidences.append(float(scoresData[x]))

    # O resto da função com o NMS permanece igual
    indices = cv2.dnn.NMSBoxes(rects, confidences, min_confidence, 0.4)
    caixas_finais = []
    if len(indices) > 0:
        for i in indices.flatten():
            caixas_finais.append(rects[i])
            
    return caixas_finais


def detectar_caixas_texto(img, min_confidence=0.1):
    # Carrega o modelo (caminho para o seu arquivo .pb)
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")
    for i, name in enumerate(net.getLayerNames()):
        print(f"Camada {i}: {name}")
    
    # Prepara a imagem para a rede (formato blob)
    blob = cv2.dnn.blobFromImage(img, 1.0, (320, 320), (123.68, 116.78, 103.94), True, False)
    net.setInput(blob)
    
    # Camadas de saída necessárias para o EAST
    layer_names = ["feature_fusion/Conv_7/Sigmoid", 
                    "feature_fusion/Conv_8/Sigmoid"]
    (scores, geometry) = net.forward(layer_names)
    
    # Aqui entraria a lógica para converter 'scores' e 'geometry' 
    # em coordenadas de caixas [x, y, w, h] usando cv2.dnn.NMSBoxes
    # (Vou simplificar para o foco ser a estrutura)
    caixas = extrair_coordenadas(scores, geometry, min_confidence)
    
    return caixas