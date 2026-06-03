from jiwer import cer, wer


def calcular_metricas(
    ground_truth,
    texto_ocr
):

    ground_truth = ground_truth.strip()

    texto_ocr = texto_ocr.strip()

    valor_cer = cer(
        ground_truth,
        texto_ocr
    )

    valor_wer = wer(
        ground_truth,
        texto_ocr
    )

    taxa_sucesso = (
        1 - valor_cer
    ) * 100

    return {

        "cer": round(
            valor_cer * 100,
            2
        ),

        "wer": round(
            valor_wer * 100,
            2
        ),

        "sucesso": round(
            taxa_sucesso,
            2
        )
    }