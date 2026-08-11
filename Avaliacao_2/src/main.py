import os
import shutil
import traceback

from gmail_service import (
    conectar_gmail,
    buscar_solicitacoes,
    obter_mensagem,
    obter_cabecalhos,
    baixar_anexos,
    marcar_como_lida,
    enviar_email
)

from documentos import (
    extrair_cpf_assunto,
    validar_nomes_arquivos,
    encontrar_ficha,
    extrair_dados_ficha,
    validar_dados,
    organizar_documentos
)

from planilha import registrar_aprovado


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOWNLOADS = os.path.join(
    BASE_DIR,
    "Downloads"
)

DOCUMENTOS_OK = os.path.join(
    BASE_DIR,
    "Documentos_OK"
)

DOCUMENTOS_PENDENTES = os.path.join(
    BASE_DIR,
    "Documentos_Pendentes"
)


def processar_solicitacao(service, message_id):

    mensagem = obter_mensagem(
        service,
        message_id
    )

    cabecalhos = obter_cabecalhos(
        mensagem
    )

    assunto = cabecalhos.get(
        "assunto",
        ""
    )

    remetente = cabecalhos.get(
        "remetente",
        ""
    )

    print(f"\nProcessando: {assunto}")
    print(f"Remetente: {remetente}")

    cpf = extrair_cpf_assunto(
        assunto
    )

    if not cpf:

        corpo = (
            "Olá,\n\n"
            "Sua solicitação não pôde ser processada "
            "porque o assunto do e-mail não segue o padrão "
            "'Cadastro Portal Fake - CPF'.\n\n"
            "Por favor, envie uma nova solicitação "
            "seguindo o padrão indicado.\n\n"
            "Portal Fake - RPA"
        )

        enviar_email(
            service,
            remetente,
            "Pendência - Cadastro Portal Fake",
            corpo
        )

        marcar_como_lida(
            service,
            message_id
        )

        return

    pasta_download = os.path.join(
        DOWNLOADS,
        cpf
    )

    os.makedirs(
        pasta_download,
        exist_ok=True
    )

    try:

        arquivos = baixar_anexos(
            service,
            mensagem,
            pasta_download
        )

        print(
            f"{len(arquivos)} anexos baixados."
        )

        erros = validar_nomes_arquivos(
            arquivos,
            cpf
        )

        if erros:

            pasta_final = organizar_documentos(
                arquivos,
                DOCUMENTOS_PENDENTES,
                cpf
            )

            motivo = "\n".join(
                f"- {erro}"
                for erro in erros
            )

            corpo = (
                f"Olá,\n\n"
                f"Sua solicitação de cadastro foi recebida, "
                f"mas está pendente.\n\n"
                f"Motivo(s):\n"
                f"{motivo}\n\n"
                f"Os documentos foram direcionados para análise "
                f"de pendências.\n\n"
                f"Portal Fake - RPA"
            )

            enviar_email(
                service,
                remetente,
                f"Pendência - Cadastro Portal Fake - {cpf}",
                corpo
            )

            marcar_como_lida(
                service,
                message_id
            )

            print(
                f"Solicitação pendente: {pasta_final}"
            )

            return

        ficha = encontrar_ficha(
            arquivos
        )

        if not ficha:
            raise Exception(
                "Ficha de cadastro não encontrada."
            )

        dados = extrair_dados_ficha(
            ficha
        )

        print(
            "Dados extraídos:",
            dados
        )

        erros = validar_dados(
            dados,
            cpf
        )

        if erros:

            organizar_documentos(
                arquivos,
                DOCUMENTOS_PENDENTES,
                cpf
            )

            motivo = "\n".join(
                f"- {erro}"
                for erro in erros
            )

            corpo = (
                f"Olá,\n\n"
                f"Sua solicitação de cadastro está pendente.\n\n"
                f"Foram identificadas as seguintes inconsistências:\n"
                f"{motivo}\n\n"
                f"Portal Fake - RPA"
            )

            enviar_email(
                service,
                remetente,
                f"Pendência - Cadastro Portal Fake - {cpf}",
                corpo
            )

            marcar_como_lida(
                service,
                message_id
            )

            return

        dados["cpf"] = cpf

        organizar_documentos(
            arquivos,
            DOCUMENTOS_OK,
            cpf
        )

        registrar_aprovado(
            dados
        )

        corpo = (
            f"Olá,\n\n"
            f"Sua solicitação de cadastro foi APROVADA.\n\n"
            f"Nome: {dados.get('nome')}\n"
            f"CPF: {cpf}\n"
            f"Data de nascimento: "
            f"{dados.get('data_nascimento')}\n"
            f"Endereço: {dados.get('endereco')}\n\n"
            f"Os dados foram registrados na base "
            f"de cadastros do Portal Fake.\n\n"
            f"Portal Fake - RPA"
        )

        enviar_email(
            service,
            remetente,
            f"Cadastro aprovado - Portal Fake - {cpf}",
            corpo
        )

        marcar_como_lida(
            service,
            message_id
        )

        print(
            f"Cadastro {cpf} aprovado com sucesso."
        )

    except Exception as erro:

        print(
            f"ERRO no processamento do CPF {cpf}: {erro}"
        )

        traceback.print_exc()

        # Tenta mover arquivos para pendentes
        if os.path.exists(pasta_download):

            try:
                organizar_documentos(
                    [
                        os.path.join(
                            pasta_download,
                            arquivo
                        )
                        for arquivo in os.listdir(
                            pasta_download
                        )
                    ],
                    DOCUMENTOS_PENDENTES,
                    cpf
                )
            except Exception:
                pass

        corpo = (
            f"Olá,\n\n"
            f"Não foi possível concluir automaticamente "
            f"o processamento da sua solicitação.\n\n"
            f"O processo foi encerrado de forma controlada "
            f"e a solicitação foi direcionada para análise.\n\n"
            f"Erro identificado: {erro}\n\n"
            f"Portal Fake - RPA"
        )

        try:

            enviar_email(
                service,
                remetente,
                f"Erro no processamento - Portal Fake - {cpf}",
                corpo
            )

        except Exception as erro_email:

            print(
                f"Não foi possível enviar resposta: {erro_email}"
            )

        marcar_como_lida(
            service,
            message_id
        )


def main():

    print("=" * 60)
    print("PORTAL FAKE - AUTOMAÇÃO DE CADASTROS")
    print("=" * 60)

    try:

        print("\nConectando ao Gmail...")

        service = conectar_gmail()

        print(
            "E-mail conectado com sucesso."
        )

        solicitacoes = buscar_solicitacoes(
            service
        )

        print(
            f"Solicitações encontradas: "
            f"{len(solicitacoes)}"
        )

        if not solicitacoes:

            print(
                "Nenhuma nova solicitação encontrada."
            )

            return

        for solicitacao in solicitacoes:

            processar_solicitacao(
                service,
                solicitacao["id"]
            )

        print("\nProcessamento concluído.")

    except Exception as erro:

        print(
            "\nERRO CRÍTICO:"
        )

        print(erro)

        traceback.print_exc()


if __name__ == "__main__":
    main()