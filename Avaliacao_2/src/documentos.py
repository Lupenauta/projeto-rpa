import os
import re
import shutil

from pypdf import PdfReader


ARQUIVOS_OBRIGATORIOS = [
    "ficha",
    "documento",
    "comprovante"
]


def extrair_cpf_assunto(assunto):
    padrao = r"Cadastro Portal Fake\s*-\s*(\d{11})"

    resultado = re.search(
        padrao,
        assunto,
        re.IGNORECASE
    )

    if resultado:
        return resultado.group(1)

    return None


def validar_nomes_arquivos(arquivos, cpf):
    encontrados = {
        "ficha": False,
        "documento": False,
        "comprovante": False
    }

    erros = []

    for caminho in arquivos:
        nome = os.path.basename(caminho).lower()

        if cpf not in nome:
            erros.append(
                f"Arquivo não pertence ao CPF {cpf}: {os.path.basename(caminho)}"
            )
            continue

        if "ficha_cadastro" in nome:
            encontrados["ficha"] = True

        elif "documento_foto" in nome:
            encontrados["documento"] = True

        elif "comprovante_residencia" in nome:
            encontrados["comprovante"] = True

    for tipo, encontrado in encontrados.items():
        if not encontrado:
            erros.append(
                f"Documento obrigatório ausente: {tipo}"
            )

    return erros


def extrair_texto_pdf(caminho):
    texto = ""

    try:
        reader = PdfReader(caminho)

        for pagina in reader.pages:
            texto += pagina.extract_text() or ""

    except Exception as erro:
        raise Exception(
            f"Erro ao ler PDF {os.path.basename(caminho)}: {erro}"
        )

    return texto


def encontrar_ficha(arquivos):
    for caminho in arquivos:
        nome = os.path.basename(caminho).lower()

        if "ficha_cadastro" in nome:
            return caminho

    return None


def extrair_dados_ficha(caminho):
    texto = extrair_texto_pdf(caminho)

    if not texto.strip():
        raise Exception(
            "A ficha de cadastro não possui texto legível."
        )

    # Normaliza espaços e quebras de linha
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n+", "\n", texto)

    dados = {}

    padroes = {
        "nome": r"Nome\s*:\s*(.*?)(?=\s+CPF\s*:)",
        "cpf": r"CPF\s*:\s*([\d.\-]+)",
        "data_nascimento": r"Data\s+de\s+Nascimento\s*:\s*(\d{2}/\d{2}/\d{4})",
        "endereco": r"Endereço\s*:\s*(.*?)(?=\s+E-mail\s*:)",
        "email": r"E-mail\s*:\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        "telefone": r"Telefone\s*:\s*([\d\s\(\)\-]+)"
    }

    for campo, padrao in padroes.items():

        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE | re.DOTALL
        )

        if resultado:
            dados[campo] = resultado.group(1).strip()
            if campo == "email":
                dados[campo] = re.sub(
                    r"^\[|\]\(mailto:.*\)$",
                    "",
                    dados[campo]
                )

    return dados

def validar_dados(dados, cpf):
    erros = []

    campos_obrigatorios = [
        "nome",
        "cpf",
        "data_nascimento",
        "endereco",
        "email",
        "telefone"
    ]

    for campo in campos_obrigatorios:

        if not dados.get(campo):
            erros.append(
                f"Campo ausente na ficha: {campo}"
            )

    if dados.get("cpf"):

        cpf_ficha = re.sub(
            r"\D",
            "",
            dados["cpf"]
        )

        if cpf_ficha != cpf:
            erros.append(
                f"CPF divergente: assunto={cpf}, ficha={cpf_ficha}"
            )

    return erros


def organizar_documentos(
    arquivos,
    destino,
    cpf
):
    pasta = os.path.join(
        destino,
        cpf
    )

    os.makedirs(
        pasta,
        exist_ok=True
    )

    for arquivo in arquivos:

        destino_arquivo = os.path.join(
            pasta,
            os.path.basename(arquivo)
        )

        shutil.move(
            arquivo,
            destino_arquivo
        )

    return pasta