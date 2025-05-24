from datetime import date
from datetime import datetime

def titulo(msg: str) -> str:
    '''
    Formata o texto digita para um padroa de titulo
    '''
    titulo: str
    titulo = f'{"="*54} \n{msg:^54} \n{"="*54}'
    return titulo


def linha() -> str:
    '''
    Retorna uma linha de 54 caracteres.
    '''
    return '-' * 54

def vericaint(msg: str) -> int | None:
    '''
    Verifica se o valor digitado é um numero inteito maior que zero.
    '''
    num: int | None = None
    while num is None:
        try:
            num = int(input(f'{msg}'))
        except ValueError:
            print('\33[0;31mO valor digitado nao foi um número inteiro.\33[m')
        except KeyboardInterrupt:
            print('\n\33[0;31mO usuario preferiu nao digitar o numero.\033[m')
            return None
        except Exception as Erro:
            print(f'\33[0;31mOcorreu um erro inesperado: {Erro.__class__.__name__}\033[m')
            continue
        else:
            if num < 0:
                print('\33[0;31mEntrada inválida, digite um número positivo.\33[m')
                num = None
            else:
                return num


def verifcpf(msg: str) -> str | None:
    '''
    Verifica se o valor digitado possui 11 dugutos tal como um cpf, esta funcao nao verifica a veracidade do cpf nem se ele possui validade.
    '''
    cpf: str | None = None
    while True:
        try:
            cpf = input(f'{msg}')
            if cpf.isdigit():
                if len(cpf) == 11:
                    return cpf
                else:
                    print('\n\33[0;31mCPF inválido. O CPF precisa conter 11 digitos\033[m')
                    continue
            else:
                print('\33[0;31mCPF inválido. Digite somente números.\033[m')
                continue
        except KeyboardInterrupt:
            print('\n\33[0;31mO usuario preferiu nao digitar o numero.\033[m')
            return None
        except Exception as erro:
                        print(f'\33[0;31mOcorreu um erro inesperado: {erro.__class__.__name__}\033[m')

def verifcnpj(msg: str) -> str | None:
    '''
    Verifica se o valor digitado possui 14 dugutos tal como um cnpj, esta funcao nao verifica a veracidade do cnpj nem se ele possui validade.
    '''
    cnpj: str | None = None
    while True:
        try:
            cnpj = input(f'{msg}')
            if cnpj.isdigit():
                if len(cnpj) == 14:
                    return cnpj
                else:
                    print('\33[0;31mCNPJ inválido. O CNPJ precisa conter 14 digitos\033[m')
                    continue
            else:
                print('\33[0;31mCNPJ inválido. Digite somente números.\033[m')
                continue
        except KeyboardInterrupt:
            print('\n\33[0;31mO usuario preferiu nao digitar o numero.\033[m')
            return None
        except Exception as erro:
                        print(f'\33[0;31mOcorreu um erro inesperado: {erro.__class__.__name__}\033[m')


def verifnome(msg: str) -> str | None:
    '''
    Verifica se o valor digitado é um nome valido, nao permitindo a entrada de números ou caracteres especiais. Retornando o nome com a primeira letra de cada palavra em maiusculo.
    '''
    while True:
        try:
            nome_digitado = input(msg)
            if not nome_digitado.strip():
                print('\33[0;31mValor inválido. O nome não pode ser vazio. Tente novamente.\33[m')
                continue  # Volta para o início do loop

            for c in nome_digitado:
                if not c.isalpha() and not c.isspace():
                    print('\33[0;31mValor inválido. Somente letras e espaços são permitidos. Tente novamente.\33[m')
                    break  # Sai do loop interno (for)

                elif c.isdigit():
                    print('\33[0;31mValor inválido. Somente letras são permitidas. Tente novamente.\33[m')
                    break  # Sai do loop interno (for)

            else:  # Executado se o loop for completo sem breaks
                return nome_digitado.title().strip()

        except KeyboardInterrupt:
            print('\n\33[0;31mO usuário preferiu não digitar.\33[m')
            return None
        except Exception as erro:
            print(f"\33[0;31mOcorreu um erro inesperado: {erro.__class__.__name__}\033[m")
            return None
        
def verifEstado():
    estados_brasil = ["AC", "AL", "AP", "AM", "BA", "CE", "ES", "GO", "MA",
                      "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                      "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    while True:
        Estado = input('Digite  a sigla do estado [ex: SP]: ')
        if Estado.upper() in estados_brasil:
            return Estado
        else:
            print('\33[0;31mEstado inválido.\033[m')
            continue

def verif_data_nascimento(msg: str) -> date | None: 
    while True:
        try:
            data_str = input(msg).strip()
            if not data_str:
                print('\33[0;31mData de nascimento não pode ser vazia.\033[m')
                continue

            data_obj = datetime.strptime(data_str, '%d/%m/%Y').date() 
            
            hoje = datetime.now().date()
            idade = hoje.year - data_obj.year - ((hoje.month, hoje.day) < (data_obj.month, data_obj.day))
            if idade < 18:
                print('\33[0;31mO cliente deve ter no mínimo 18 anos.\033[m')
                continue

            return data_obj
        
        except ValueError:
            print('\33[0;31mFormato de data inválido ou data inexistente. Use DD/MM/AAAA.\033[m')

        except KeyboardInterrupt:
            print('\n\33[0;31mOperação cancelada pelo usuário.\033[m')
            return None
        
        except Exception as erro:
            print(f"\33[0;31mOcorreu um erro inesperado na validação da data: {erro.__class__.__name__}\033[m")
            return None
    

def menu() -> int | None: 
    # Imprime o título usando a função e printando
    print(titulo('Bem vindo ao Caixa Eletronico'))
    print("\nDigite uma das opções para continuar:\n\n"
          "1 - Saque\n"
          "2 - Depósito\n"
          "3 - Extrato\n"
          "4 - Criar cliente\n"
          "5 - Criar conta\n"
          "6 - Listar Contas\n" \
          "7 - Listar detalhes da conta\n" 
          "8 - Sair")

    while True:
        opc = vericaint("\nOpção desejada: ")
        if opc is None:
            return None
        if opc in [1, 2, 3, 4, 5, 6, 7, 8]:
            return opc
        else:
            print('\33[0;31mOpção inválida. Tente Novamente.\033[m')