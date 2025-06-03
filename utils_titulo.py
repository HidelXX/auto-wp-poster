import re

def formatar_titulo_bruto(titulo: str) -> str:
    titulo = titulo.strip()

    # Remove "Ref." e tudo que vier após (inclui ponto ou sem)
    titulo = re.sub(r"\bRef\.?\s*\S*", "", titulo, flags=re.IGNORECASE)

    # Remove conteúdo entre parênteses, se houver
    titulo = re.sub(r"\s*\([^)]*\)", "", titulo)

    # Corrige texto entre aspas tipográficas ou normais: “a” → “Tipo A”
    titulo = re.sub(r"[“\"']([a-zA-Z])[”\"']", lambda m: f'“Tipo {m.group(1).upper()}”', titulo)

    # Remove traços com sufixos irrelevantes (ex: "- branco fosco")
    titulo = re.sub(r"\s*-\s*[\w\s,\.]+$", "", titulo)

    # Corrige unidades: 2,30m2 → 2.30m²
    titulo = re.sub(r"(\d+)[,\.]?(\d*)\s*[mM][²2]?", lambda m: f"{m.group(1)}.{m.group(2)}m²" if m.group(2) else f"{m.group(1)}m²", titulo)

    # Corrige dimensões: 60X60 ou 500x300m²m → 60x60, 500x300
    titulo = re.sub(r"(\d+)[xX×](\d+)", r"\1x\2", titulo)
    titulo = re.sub(r"m²m", "m²", titulo, flags=re.IGNORECASE)

    # Capitaliza todas as palavras, exceto abreviações
    especiais = {"HD", "C/", "P/", "Q/", "S/", "A", "O", "BR", "GL"}
    palavras = titulo.split()
    palavras_formatadas = []

    for palavra in palavras:
        palavra_limpa = palavra.upper() if palavra.upper() in especiais else palavra.capitalize()
        palavras_formatadas.append(palavra_limpa)

    return " ".join(palavras_formatadas).strip()