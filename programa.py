"""
    __author__ = "Ennio Gomide"
    __version__ = "1.0.0"
    -*- coding: utf-8 -*-
    Programa de controle bancário criado segundo os requisitos, utlizando funçóes.
    Construido segundo os requisistos apresentados: desafio - otimizando o sistema bancário com funçoes python
    Manter as funcionalidade atua: depositar, sacar, extrato e sair e limite de saque diário e quantidade de saques.
    
    Ajustar:
        - Funções para cada operação: depositar, sacar, exibir extrato e sair, criando funçóes.
            função saque: 
                argumento  chamada: keyword only saldo, valor, extrato, limite, numero_saques, limite_saques
                retorno: saldo, extrato

            função depositar:
                argumento chamada: posicional saldo, valor, extrato
                retorno: saldo, extrato

            função exibir_extrato:
                argumento chamada: posicinal e nome.
                posicionais: saldo, nomeados: extrato
                retorno: None

    Criar duas novas funções:
        - Criar usuário (cliente no banco) com nome, cpf e data de nascimento.
        - Criar conta corrente para o usuário com número da conta, saldo inicial, limite de saque e número de saques realizados. Vinculada ao usuário criado.

        criar usuário:
            argumento chamada: nome, cpf, data_nascimento
            retorno: dicionário com os dados do usuário

        criar conta corrente:
            argumento chamada: usuário, saldo_inicial, limite_saque, numero_saques

        listar contas:

        Usuarios: armazenar em uma lista. (nome, data de nascimento, cpf e endereço (string no formato
                   "logradouro, número - bairro - cidade/estado - cep"))
                CPF: armazenar somente números sem formatação, como string.
                Data de nascimento: armazenar como string no formato "dd/mm/aaaa".

                Não pode ser cadastrado dois usuários com o mesmo CPF.

        Conta corrente: 
            armazenar em uma lista. (agência, número da conta e usuario (cliente), saldo, limite de saque, número de saques realizados)
            conta é sequencia, começando em 1, e incrementando a cada nova conta criada.
            a agencias será fixa 1000/nnnnnn onde n é o numero da conta corrente

"""
import os

# CONSTANTES
LIMITE_SAQUES = 3

# variáveis
agencia = "1000"
ultima_conta = 0

# ************************************************************
# **** apresentação do menu de opções do sistema bancário ****
# ************************************************************


def menu():
    menu = """

[d] Depositar
[s] Sacar
[e] Extrato

[u] Criar cliente
[c] Criar Conta Corrente
[l] Listar contas

[q] Sair

=>"""
    os.system("cls" if os.name == "nt" else "clear")
    print(menu)

# ************************************************************
# **** Funcão fazer depósito na conta corrente            ****
# ************************************************************


def depositar_na_conta(saldo, valor, extrato):

    if valor <= 0:
        mensagem = "O valor informado é inválido."
    else:
        saldo += valor
        extrato += f"Depósito....: R$ {valor:8.2f}\n"
        mensagem = "Depósito realizado com sucesso! Saldo atual:" \
            + f" R$ {saldo:8.2f}"
    return saldo, extrato, mensagem

# ************************************************************
# **** Funcão para fazer o saque na conta corrente        ****
# ************************************************************


def sacar_da_conta(saldo=0,
                   valor=0,
                   extrato="",
                   limite=0,
                   numero_saques=0,
                   limite_saques=LIMITE_SAQUES):

    if valor <= 0:
        print("")
        sucesso_operacao = False
        mensagem = "Erro! Informe o valor a ser sacado maior que zero."

    elif numero_saques >= limite_saques:
        sucesso_operacao = False
        mensagem = "Limite de saques atingido. "\
            "Você não pode realizar mais saques hoje."

    elif valor > limite:
        sucesso_operacao = False
        mensagem = "Erro: Não é possível sacar mais " \
            "que o limite de R$ {limite:.2f}."

    elif valor > saldo:
        sucesso_operacao = False
        mensagem = "Erro: Não é possível sacar." \
            " Valor solicitado maior que saldo disponível."

    else:
        saldo -= valor
        extrato += f"Saque.......: R$ {valor:8.2f}\n"
        numero_saques += 1
        sucesso_operacao = True
        mensagem = f"Saque realizado com sucesso! Saldo atual: R$ {saldo:.2f}"

    return saldo, extrato, numero_saques, sucesso_operacao, mensagem

# ************************************************************
# **** Funcão exibir o extrato da conta corrente          ****
# ************************************************************


def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo.......: R$ {saldo:8.2f}")
    print("\n=========================================\n")


# ************************************************************
# **** Funçoes para criação da conta de cliente           ****
# ************************************************************


def informar_cpf(clientes):
    cpf_valido = False
    cpf = ""
    while not cpf_valido:
        cpf = input("Informe o CPF do cliente (somente números): ").strip()
        # Validar CPF
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Deve conter apenas números e ter 11 dígitos.")
            input()
            continue
        # Verificar se o CPF já está cadastrado
        cliente = clientes.get(cpf)
        if cliente:
            print(f"CPF {cpf} já cadastrado para o cliente {cliente['nome']}.")
            input()
            continue
        else:
            cpf_valido = True
    return cpf

# informar o nome do cliente


def informar_nome():
    nome_valido = False
    nome = ""
    while not nome_valido:
        nome = input("Informe o nome do cliente: ").strip()
        if not nome and len(nome) <= 20:
            print("Nome inválido."
                  "O nome não pode ser vazio. Deve ter mais de 20 caracteres.")
            input()
            continue
        nome_valido = True
    return nome

# informar a data de nascimento do cliente


def informar_data_nascimento():
    data_nascimento = ""
    data_valida = False
    while not data_valida:
        data_nascimento = input("Informe a data de nascimento "
                                "(dd/mm/aaaa): ").strip()
        # Validar formato da data
        if not data_nascimento or len(data_nascimento) != 10 or \
           data_nascimento[2] != '/' or data_nascimento[5] != '/':
            print("Data inválida. Use o formato dd/mm/aaaa.")
            input()
            continue
        # Verificar se a data é válida (básico, sem validação de dias)
        try:
            dia, mes, ano = map(int, data_nascimento.split('/'))
            if (dia < 1 or dia > 31) or \
                (mes < 1 or mes > 12) or \
                (ano < 1900 or ano > 2025):
                raise ValueError
            data_valida = True
        except ValueError:
            print("Data inválida. Verifique os valores informados.")
            input()
            continue
    return data_nascimento

# informar o endereco do cliente


def informar_endereco():
    endereco_valido = False
    endereco = ""
    while not endereco_valido:
        endereco = input("Informe o endereço do cliente (logradouro, "
                         "número - bairro - cidade/estado - cep): ").strip()
        if not endereco or len(endereco) < 20:
            print("Endereço inválido. Deve ter mais de 20 caracteres.")
            input()
            continue
        # Verificar se o endereço contém os componentes necessários
        if "," not in endereco or "-" not in endereco or " " not in endereco:
            print("Endereço inválido. Verifique o formato informado.")
            input()
            continue
        endereco_valido = True
    return endereco

# Criar o registro do clientes na lista clientes


def criar_registro_cliente(nome, cpf, data_nascimento, endereco, clientes):
    clientes[cpf] = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
        }
    return clientes

# ************************************************************
# **** Criar a conta do cliente                           ****
# ************************************************************


def criar_cliente(clientes):
    # solicitar CPF do cliente
    cpf = informar_cpf(clientes)
    # Solicitar nome e data de nascimento
    nome = informar_nome()
    # Solicitar data de nascimento
    data_nascimento = informar_data_nascimento()
    # solicitar endereço
    endereco = informar_endereco()
    # Criar dicionário com os dados do cliente
    clientes = criar_registro_cliente(nome, cpf, data_nascimento,
                                      endereco, clientes)
    return clientes

# ************************************************************
# **** Criar a conta do cliente                           ****
# ************************************************************

# selecionar cliente


def selecionar_cliente(clientes):
    cpf_valido = False
    cpf = ""
    while not cpf_valido:
        cpf = input("Informe o CPF do cliente para criar a conta: ").strip()
        # Validar CPF
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Deve conter apenas números e ter 11 dígitos.")
            input()
            continue
        # Verificar se o CPF já está cadastrado
        cliente = clientes.get(cpf)
        if not cliente:
            print(f"CPF {cpf} - Não existe cliente cadastrado.")
            input()
            continue
        else:
            cpf_valido = True
    return cpf

# Informar saldo inicial (depósito de abertura de conta)


def informar_saldo_inicial():
    saldo_inicial_valido = False
    while not saldo_inicial_valido:
        saldo_inicial = input("Informe deposito inicial: ")
        try:
            saldo_inicial = float(saldo_inicial)
        except ValueError:
            print("Valor inválido. Por favor, informe um valor.")
            print("pressione <enter> para continuar...")
            input()
        if saldo_inicial <= 0:
            print("Depósito inical tem que ser maior que zero.")
            print("pressione <enter> para continuar...")
            input()
        else:
            saldo_inicial_valido = True
    return saldo_inicial

# Informar o limite (quantidade) de saques diários


def informar_limite_saque_diario():
    limite_saque_valido = False
    while not limite_saque_valido:
        limite_saque_diario = input("Informe limite de saques diário: ")
        try:
            limite_saque_diario = float(limite_saque_diario)
        except ValueError:
            print("Valor inválido. Por favor, informe um valor numérico.")
            print("pressione <enter> para continuar...")
            input()
        if 0 < limite_saque_diario <= 10:
            print("Limite de saques inválido. Entre 1 e 10")
            print("pressione <enter> para continuar...")
            input()
        else:
            limite_saque_valido = True
    return limite_saque_diario

# Criação do registor de conta do cliente no contas_correntes


def criar_registro_conta_correntes(
        contas_correntes,
        agencia,
        ultima_conta,
        cpf,
        saldo_inicial,
        limite_saque_diario,
        numero_saques_no_dia):
    ultima_conta += 1
    numero_conta = "000000"[0:6-len(str(ultima_conta))] + str(ultima_conta)
    conta_cliente = cpf + "/" + agencia + "/" + numero_conta
    contas_correntes[conta_cliente] = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "cliente": cpf,
        "saldo_inicial": saldo_inicial,
        "limite_saque_diario": limite_saque_diario,
        "numero_saques_no_dia": numero_saques_no_dia
    }
    return conta_cliente, contas_correntes


def criar_conta_corrente(agencia, ultima_conta, clientes, contas_correntes):
    # solicitar CPF do cliente
    cpf = selecionar_cliente(clientes)
    # Solicitar nome e data de nascimento
    saldo_inicial = informar_saldo_inicial()
    # Solicitar data de nascimento
    limite_saque_diario = informar_limite_saque_diario()
    # solicitar endereço
    numero_saques = 0
    # Criar dicionário com os dados do cliente
    conta_cliente, contas_correntes = criar_registro_conta_correntes(
        contas_correntes,
        agencia,
        ultima_conta,
        cpf,
        saldo_inicial,
        limite_saque_diario,
        numero_saques
    )
    inserir_lancamento_extrato(cpf,
                               conta_cliente,
                               contas_correntes,
                               "Depósito inicial",
                               saldo_inicial)
    return contas_correntes
# ************************************************************
# **** Funcão main para controle geral do app             ****
# ************************************************************


def __main__():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    clientes = {}  # Dicionário para armazenar clientes
    contas_correntes = {}  # Dicionário para armazenar contas correntes

    while True:
        menu()
        opcao = input().strip().lower()

        # validar o informado com as opçoes disponíveis
        if opcao not in ["d", "s", "e", "c", "u", "l", "q"]:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            print("pressione <enter> para continuar...")
            input()
            continue

        # para sair da aplicação usa o opcao "q"
        if opcao == "q":
            print("Obrigado por utilizar nossos serviços!")
            print("Saindo...")
            print("-------------------------------------------")
            break

        # opção para fazer o depósito
        elif opcao == "d":
            valor = input("Informe o valor a depositar: ")
            try:
                valor = float(valor)
            except ValueError:
                print("Valor inválido. Por favor, informe um valor.")
                print("pressione <enter> para continuar...")
                input()
                continue

            saldo, extrato, mensagem = depositar_na_conta(
                saldo, valor, extrato
            )

            print(mensagem)
            print("pressione <enter> para continuar...")
            input()

        # fazer o saque na conta corrente
        elif opcao == "s":

            valor = input("Informe o valor do saque: ")
            try:
                valor = float(valor)
            except ValueError:
                print("Valor inválido. Por favor, informe um número.")
                print("pressione <enter> para continuar...")
                input()
                continue

            saldo, extrato, numero_saques, sucesso_operacao, mensagem = \
                sacar_da_conta(
                    saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                    numero_saques=numero_saques, limite_saques=LIMITE_SAQUES
                )

            print(mensagem)
            print("pressione <enter> para continuar...")
            input()

        # opção para exibir o extrato da conta corrente
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
            print("pressione <enter> para continuar...")
            input()
        # opção criar cliente
        elif opcao == "u":
            clientes = criar_cliente(clientes)
        # opção criar Conta corrente
        elif opcao == "c":
            contas_correntes = criar_conta_corrente(
                agencia,
                ultima_conta,
                clientes,
                contas_correntes
            )
            print(contas_correntes)
            print("pressione <enter> para continuar...")
            input()


__main__()

# saldo = 0
# limite = 500
# extrato = ""
# numero_saques = 0


# while True:
#     opcao = input(menu).strip().lower()

#     if opcao == "d":
#         valor = float(input("Informe o valor a depositar: "))
#         if valor > 0:
#             saldo += valor
#             extrato += f"Depósito: R$ {valor:.2f}\n"
#         else:
#             print("O valor informado é inválido.")

#     elif opcao == "s":
#         if numero_saques == LIMITE_SAQUES:
#             print("Limite de saques atingido. Você não pode realizar mais saques hoje.")
#             continue

#         valor = float(input("Informe o valor do saque: "))
#         if valor > limite:
#             print(f"Erro: Não é possível sacar mais que o limite de R$ {limite:.2f}.")
#             continue

#         if valor > saldo:
#             print("Erro: Não é possível sacar. Valor solicitado maior que saldo disponível.")
#             continue

#         if valor > 0:
#             saldo -= valor
#             extrato += f"Saque: R$ {valor:.2f}\n"
#             numero_saques += 1
#         else:
#             print("Erro! Informe o valor a ser sacado maior que zero.")

#     elif opcao == "e":
#         print("\n================ EXTRATO ================\n")
#         print("Não foram realizadas movimentações." if not extrato else extrato)
#         print(f"\nSaldo: R$ {saldo:.2f}")
#         print("\n=========================================\n")

#     elif opcao == "q":
#         print("Obrigado por utilizar nosso sistema!")
#         break

#     else:
#         print("Opção inválida! Por favor, escolha uma opção válida.")