from abc import ABC
from typing import List
from datetime import datetime, date
import funcoes_adicionais as funcoes

#Criando estrutura de classe

class Historico:
    def __repr__(self):
        return str (self.transacoes)
    
    def __init__(self):
        self.transacoes: List['Transacao'] = []

    def adicionar_transacao(self, transacao: 'Transacao'):
        self.transacoes.append(transacao)


class Conta:
    def __repr__(self):
        return str(self.numero)
    
    def __init__(self, _saldo: float, _numero: str, _agencia: str, _cliente: 'Cliente'):
        self._saldo: float = _saldo
        self.numero: str = _numero
        self.agencia: str = _agencia
        self.cliente: 'Cliente' = _cliente
        self.historico: 'Historico' = Historico()

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: str) -> 'Conta':
        return cls(0.0, numero, '0001', cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    def sacar(self, valor: float) -> bool:
        if self._saldo < valor:
            print('Saldo insuficiente!')
            return False
        else:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print('Valor invalido!')
            return False
        else:
            self._saldo += valor
            print('Deposito realizado com sucesso!')
            return True

class ContaCorrente(Conta):
    def __str__(self):
            return f'Conta Corrente: {self.numero}/{self.agencia}'

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: str) -> 'Conta':
        return cls(0.0, numero, '0001', cliente,)


    def __init__(self, _saldo: float, _numero: str, _agencia: str, _cliente: 'Cliente', _saques_realizados = 0, _limite_por_saque: float = 1000, _limites_saques: int = 3):
        super().__init__(_saldo, _numero, _agencia, _cliente, )
        self.limite_por_saque: float = _limite_por_saque
        self.limites_saques: int = _limites_saques
        self.saques_realizados: int = _saques_realizados

    
    def sacar(self, valor: float) -> bool:

        if valor <= 0:
            print('\033[0;31mO valor do saque deve ser maior que zero.\033[m')
        
        elif self._saldo < valor:
            print('\033[0;31mSaldo insuficiente!\033[m')
            return False

        elif valor > self.limite_por_saque:
            print(f'\033[0;31mO valor do saque não pode exceder R${self.limite_por_saque:.2f}.\033[m')
            return False
        
        elif self.saques_realizados >= self.limites_saques:
            print(f'\033[0;31mO limite de saques diários ({self.limites_saques}) foi excedido.\033[m')
            return False
        
        else:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            self.saques_realizados += 1
            return True


class Transacao(ABC):
    def registrar(self, conta: 'Conta'):
        pass

    def __repr__(self):
        return f"{self.__class__:<20}| {self.valor:<10}\n"


class Deposito(Transacao):
    def __init__ (self, valor: float, saldo: float):
        self.valor: float = valor
        self.saldo: float = saldo
    
    def __repr__(self):
        return f"{str(self.__class__.__name__):<22}|{'+ R$' + f'{self.valor:.2f}':>14}|{' R$' + f'{self.valor:.2f}':>14}|"
            

    def registrar(self, conta: 'Conta'):
        if conta.depositar(self.valor):
            self.saldo = conta.saldo
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__ (self, valor: float, saldo:float):
        self.valor: float = valor
        self.saldo: float = saldo
    
    def __repr__(self):
        return f"{str(self.__class__.__name__):<22}|{'- R$' + f'{self.valor:.2f}':>14}|{' R$' + f'{self.valor:.2f}':>14}|"
    

    def registrar(self, conta: 'Conta'):
        if conta.sacar(self.valor):
            self.saldo = conta.saldo
            conta.historico.adicionar_transacao(self)


class Cliente(ABC):
    _lista_de_clientes = []

    def __init__ (self, _endereco: str, _contas: List['Conta']):
        self.endereco: str = _endereco
        self.contas: List['Conta'] = _contas

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print(f"A conta {conta.numero} não pertence a este cliente.")

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)

    @classmethod
    def adicionar_na_lista(cls, cliente: "Cliente"):
        cls._lista_de_clientes.append(cliente)

    @classmethod
    def verificar_cpf(cls, cpf: str) -> 'PessoaFisica':
        '''
        Verifica se o CPF digitado ja existe nalista de clientes
        '''

        for cliente in cls._lista_de_clientes:
            if isinstance(cliente, PessoaFisica) and cpf == cliente.cpf:
                return cliente
        return None


    @classmethod
    def verificar_cnpj(cls, cnpj: str) -> 'PessoaJuridica':
        '''
        Verifica se o CPF digitado ja existe nalista de clientes
        '''

        for cliente in cls._lista_de_clientes:
            if isinstance(cliente, PessoaJuridica) and cnpj == cliente.cnpj:
                return cliente
        return None
    

class PessoaFisica(Cliente):
    def __repr__(self):
        contas_formatadas = "\n".join([f"    - {str(conta)}" for conta in self.contas])

        return (f'<Nome: {self.nome}\n'
                f'CPF: {self.cpf}\n'
                f'Data de Nascimento: {self.data_nascimento}\n'
                f'Contas:\n{contas_formatadas}\n'
                f'Endereço: {self.endereco}>')
    
            
    def __init__ (self, _endereco: str, _contas: List['Conta'], _cpf: str, _nome: str, _data_nascimento: date):
        super().__init__(_endereco, _contas)
        self.cpf: str = _cpf
        self.nome: str = _nome
        self.data_nascimento: date = _data_nascimento

    @classmethod
    def criar_cliente_pf(cls, nome: str, cpf: str, data_nascimento: date, endereco: str) -> 'PessoaFisica':
        return cls(_nome = nome, _cpf = cpf, _data_nascimento = data_nascimento, _endereco = endereco, _contas = [])


class PessoaJuridica(Cliente):
    def __repr__(self):
        contas_formatadas = "\n".join([f"    - {str(conta)}" for conta in self.contas])

        return (f'Nome: {self.nome}\n'
                f'Nome fantaisa: {self.nome_fantasia}\n'
                f'CNPJ: {self.cnpj}\n'
                f'Contas:\n{contas_formatadas}\n'
                f'Endereço: {self.endereco}')        
    
    def __init__ (self, _endereco: str, _contas: List['Conta'], _cnpj: str, _nome_fantasia: str, _nome: str):
        super().__init__(_endereco, _contas)
        self.cnpj: str = _cnpj
        self.nome: str = _nome
        self.nome_fantasia: str = _nome_fantasia

    @classmethod
    def crir_cliente_pj(cls, nome: str, nome_fantasia: str, cnpj: str, endereco: str) -> 'PessoaJuridica':
        return cls(_nome = nome, _nome_fantasia = nome_fantasia, _cnpj = cnpj, _endereco = endereco, _contas = [])


#Corpo do codigo 
def criar_pessoa_fisica() -> PessoaFisica:
    while True:
        print('\n')
        print(funcoes.titulo('Cadastro de Pessoa Física'))
        novo_cpf = funcoes.verifcpf('Digite o CPF do cliente: ')
        if novo_cpf is None:
            print('Operação cancelada.')
            return None
        
        cliente_existente = Cliente.verificar_cpf(novo_cpf)

        if cliente_existente:
            print(f'\33[0;31mErro: Já existe um cliente com o CPF {novo_cpf} cadastrado '
                    f'({cliente_existente.nome}).\033[m')
            resp = input('Deseja tentar outro CPF? [S/N]\n').upper()
            if resp != 'S':
                print("Cadastro cancelado.")
                return None
            else:
                continue
        break

    novo_nome = funcoes.verifnome('Digite o nome do cliente: ')
    if novo_nome is None:
        print('Operação cancelada.')

    print('Digite os seguintes dados do endereço do cliente:')
    endereco = input('Digite o logradouro: \n').title()
    nro = funcoes.vericaint('Digite o número: \n')
    bairro = funcoes.verifnome ('Digite o bairro: \n').title()
    cidade =funcoes.verifnome('Digite o nome da cidade: ').title()
    estado = funcoes.verifEstado()
    novo_endereco = endereco + ' - ' + str(nro) + ' - ' + bairro + ' - ' + cidade + '/' + estado.upper()

    novo_dt_nascimento = funcoes.verif_data_nascimento("DIgite a data de nascimento: ")

    print(f'\nCliente {novo_nome} cadastrado com sucesso!')

    return PessoaFisica.criar_cliente_pf(
    nome=novo_nome,
    cpf=novo_cpf,
    data_nascimento=novo_dt_nascimento,
    endereco=novo_endereco
    )


def criar_pessoa_juridica() -> PessoaJuridica:
    while True:
        print('\n')
        print(funcoes.titulo('Cadastro de Pessoa Juridica'))
        novo_cnpj = funcoes.verifcnpj('Digite o CNPJ do cliente: ')
        if novo_cnpj is None:
            print('Operação cancelada.')
            return None
        
        cliente_existente = Cliente.verificar_cnpj(novo_cnpj)

        if cliente_existente:
            print(f'\33[0;31mErro: Já existe um cliente com o CNPJ {novo_cnpj} cadastrado '
                    f'({cliente_existente.nome}).\033[m')
            resp = input('Deseja tentar outro CNPJ? [S/N]\n').upper()
            if resp != 'S':
                print("Cadastro cancelado.")
                return None  
            else:
                continue  
        break

    novo_nome = funcoes.verifnome('Digite o nome do cliente: ')
    if novo_nome is None:
        print('Operação cancelada.')
    
    novo_nome_fantasia = funcoes.verifnome('Digite o nome fantasia do cliente: ')
    if novo_nome_fantasia is None:
        print('Operação cancelada.')

    print('Digite os seguintes dados do endereço do cliente:')
    endereco = input('Digite o logradouro: \n').title()
    nro = funcoes.vericaint('Digite o número: \n')
    bairro = funcoes.verifnome ('Digite o bairro: \n').title()
    cidade =funcoes.verifnome('Digite o nome da cidade: ').title()
    estado = funcoes.verifEstado()
    novo_endereco = endereco + ' - ' + str(nro) + ' - ' + bairro + ' - ' + cidade + '/' + estado.upper()

    print(f'\nCliente {novo_nome} cadastrado com sucesso!')

    return PessoaJuridica.crir_cliente_pj(
    nome = novo_nome,
    nome_fantasia = novo_nome_fantasia,
    cnpj = novo_cnpj,
    endereco = novo_endereco
    )

def criar_conta(nrconta: str) -> str:
    print(funcoes.titulo('Criacao de nova conta'))
    while True:
        print('\nSelecione o tipo de cliente\n' \
        '[1] Pessoa Física.\n' \
        '[2] Pessoa Juridica.\n' \
        '[0] Sair.')

        tipo = funcoes.vericaint('Opção desejada: ')
        if tipo is None or tipo == 0:
            print("\033[0;31mOperação de criação de conta cancelada.\033[m")
            return nrconta

        if tipo == 1:
            while True:
                cpf = funcoes.verifcpf('\nDigite o CPF do cliente: ')

                if cpf is None:
                    print("Operação cancelada.")
                    cliente = None
                    break

                cliente = Cliente.verificar_cpf(cpf)
                if cliente:
                    print(f'\nCliente PF {cliente.nome} encontrado.')
                    break
                          
                else:
                    print('\n\33[0;31mCliente não encontrado.\033[m\n')
                    resp = input('Deseja tentar outro CPF? [S/N]\n').upper()
                    if resp != 'S':
                        print("Cadastro cancelado.")
                        cliente = None
                        break
        
        elif tipo == 2:
            while True:
                cnpj = funcoes.verifcnpj('Digite o CNPJ do cliente: ')
                if cnpj is None:
                    print("Operação cancelada.")
                    cliente = None
                    break
                cliente = Cliente.verificar_cnpj(cnpj)
                if cliente:
                    print(f'\nCliente PJ {cliente.nome} encontrado.')
                    break
                else:
                    print('\n\33[0;31mCliente não encontrado.\033[m\n')
                    resp = input('Deseja tentar outro CNPJ? [S/N]\n').upper()
                    if resp != 'S':
                        print("Cadastro cancelado.")
                        cliente = None
                        break
        else: 
            print('Opção inválida.')
            continue

        if cliente:
            while True:
                print('\nSelecione o tipo de conta\n' \
                      '[1] Conta corrente.\n' \
                      '[0] Voltar ao Menu Anterior.\n') 
                
                opcao = funcoes.vericaint('Opção desejada: ')
                
                if opcao is None or opcao == 0:
                    print("\033[0;31mCriação de conta cancelada.\033[m")
                    return nrconta
                
                if opcao == 1:
                    novo_nrconta_int = int(nrconta) + 1
                    novo_nrconta = f'{novo_nrconta_int:03d}'
                    
                    nova_conta = ContaCorrente.nova_conta(cliente, novo_nrconta)
                    print(f'\n\033[0;32mConta: {novo_nrconta} criada com sucesso em nome de {cliente.nome}!\033[m')
                    cliente.adicionar_conta(nova_conta)
                    return novo_nrconta # Retorna o NOVO número da conta e sai da função
                
                else: # Opção de tipo de conta inválida
                    print('\033[0;31mOpção de conta inválida. Tente novamente.\033[m')
        else:
            return nrconta # Retorna o número da conta original


def listar_clientes():
    while True:
        print('\nSelecione o tipo de cliente\n' \
            '[1] Pessoa Física.\n' 
            '[2] Pessoa Juridica.\n' \
            '[3] Todas.\n' 
            '[0] Sair.\n')
        
        encontrou_cliente = False
        tipo = funcoes.vericaint('Opção selecionada: ')

        if tipo is None or tipo == 0:
            print("\033[0;31mOperação de listagem de conta cancelado.\033[m")
            break

        elif tipo == 1:
            print(funcoes.titulo('Lista de clientes PF'))
            for c in Cliente._lista_de_clientes:
                if isinstance  (c, PessoaFisica):
                    print(funcoes.linha())
                    print(c)
                    print(funcoes.linha())
                    encontrou_cliente = True
                if not encontrou_cliente:
                    print("\033[0;33mNenhum cliente Pessoa Física encontrado.\033[m")

        elif tipo == 2:
            print(funcoes.titulo('Lista de clientes PJ'))
            for c in Cliente._lista_de_clientes:
                if isinstance  (c, PessoaJuridica):
                    print(funcoes.linha())
                    print(c)
                    print(funcoes.linha())
                    encontrou_cliente = True
            if not encontrou_cliente:
                print("\033[0;33mNenhum cliente Pessoa Jurídica encontrado.\033[m")

        elif tipo == 3:
            print(funcoes.titulo('Lista de Todos os Clientes'))
            if not Cliente._lista_de_clientes:
                print("\033[0;33mNenhum cliente cadastrado no sistema.\033[m")
            else:
                for c in Cliente._lista_de_clientes:
                    print(funcoes.linha())
                    print(c)
                    print(funcoes.linha())
                    encontrou_cliente = True
                if not encontrou_cliente:
                    print("\033[0;33mNenhum cliente encontrado.\033[m")
        
        else: 
            print('\033[0;31mOpção inválida. Por favor, digite 1, 2, 3 ou 0 para sair.\033[m')
            continue


def listar_detalhes_conta():
    print(funcoes.titulo('Detalhes da Conta'))
    conta_selecionada = selecao_de_conta() 

    if conta_selecionada:
        if isinstance(conta_selecionada, ContaCorrente):
            print(funcoes.linha())
            print(f'Número da conta: {conta_selecionada.numero}/{conta_selecionada.agencia}\n'
                  f'Tipo de conta: {conta_selecionada.__class__.__name__}\n'
                  f'Proprietário: {conta_selecionada.cliente.nome}\n'
                  f'Limite de saques diário: {conta_selecionada.limites_saques}\n'
                  f'Valor máximo disponível para saque: R${conta_selecionada.limite_por_saque:.2f}\n'
                  f'Saques disponíveis: {conta_selecionada.limites_saques - conta_selecionada.saques_realizados}\n'
                  f'Saldo disponível: R${conta_selecionada.saldo:.2f}')

            #Verificação de segurança
            if hasattr(conta_selecionada, 'historico') and hasattr(conta_selecionada.historico, 'transacoes'):
                print("\nHistórico de Transações:")
                print(funcoes.linha())
                print(f'{"|TRANSAÇÃO":<23}|{"VALOR":>14}|{"SALDO":>14}|')
                print(funcoes.linha())
                if conta_selecionada.historico.transacoes:
                    for item in conta_selecionada.historico.transacoes:
                        print(f"|{item}")
                    print(funcoes.linha())
                    print(f"{'|Saldo:':<10} {'R$' + f'{conta_selecionada.saldo:.2f}':>42}|")    
                else:
                    print("Nenhuma transação registrada nesta conta.")
            print(funcoes.linha())
        else:
            print("\033[0;33mTipo de conta não suportado para exibição detalhada neste momento.\033[m")
    else:
        print("\033[0;31mNenhuma conta foi selecionada.\033[m")

def selecao_de_conta() -> 'Conta':
        while True:
            print('\nSelecione o tipo de cliente\n' 
                '[1] Pessoa Física.\n' 
                '[2] Pessoa Jurídica.\n'
                '[0] Sair.\n')
            
            tipo = funcoes.vericaint('Opção selecionada: ')

            if tipo is None or tipo == 0:
                print("\033[0;31mOperação de listagem de conta cancelada.\033[m")
                return None

            cliente_encontrado = None

            if tipo == 1:
                cpf = funcoes.verifcpf('Digite o CPF do cliente: ')
                if cpf is None:
                    print("Busca cancelada.")
                    continue
                cliente_encontrado = Cliente.verificar_cpf(cpf)
            elif tipo == 2:
                cnpj = funcoes.verifcnpj('Digite o CNPJ do cliente: ')
                if cnpj is None:
                    print("Operação cancelada.")
                    continue
                cliente_encontrado = Cliente.verificar_cnpj(cnpj)
            else:
                print('\033[0;31mOpção inválida. Por favor, digite 1, 2 ou 0 para sair.\033[m')
                continue

            if not cliente_encontrado:
                print("\033[0;33mCliente não encontrado ou busca de cliente cancelada.\033[m")
                continue 
            
            #Cliente encontrado
            print(f'\nLista de contas de {cliente_encontrado.nome}:')
            if not cliente_encontrado.contas:
                print("\033[0;33mEste cliente não possui contas cadastradas.\033[m")
                continue 
            
            for i, cta in enumerate(cliente_encontrado.contas):
                print(f"  {i+1} - Agência: {cta.agencia}, Número: {cta.numero}, Saldo: R${cta.saldo:.2f}")
                print()

            while True:
                num_digitado = funcoes.vericaint('Selecione o NÚMERO da conta que deseja ver os detalhes (ou 0 para sair): ')

                if num_digitado is None or num_digitado == 0:
                    print("\033[0;31mOperação de detalhes de conta cancelada.\033[m")
                    return None
                
                conta_procurada_str = f'{num_digitado:03d}' 
                conta_encontrada_obj = None 

                for cta in cliente_encontrado.contas:
                    if cta.numero == conta_procurada_str:
                        conta_encontrada_obj = cta
                        break

                if conta_encontrada_obj:
                    return conta_encontrada_obj
                else:
                    print("\033[0;33mNúmero da conta inválido ou não pertence a este cliente. Tente novamente.\033[m")



def main():
    nrconta = '000'
    cliente1 = PessoaFisica(
    _endereco='Rua teste',
    _contas=[],
    _cpf='12345678900',
    _nome='Gabriel de Souza',
    _data_nascimento=datetime.strptime('14/09/2002', '%d/%m/%Y').date()
)
    Cliente.adicionar_na_lista(cliente1)
    conta1 = ContaCorrente.nova_conta(cliente1, '001')
    cliente1.adicionar_conta(conta1)

    while True:
        opcao = funcoes.menu()

        if opcao == 1:
            conta_atual = selecao_de_conta()

            if conta_atual:
                while True:
                    valor = funcoes.vericaint('\nDigite o valor que deseja sacar [0 para cancelar].\nR$')

                    if valor is None:
                        print('Operação cancelada.')
                        break

                    if valor < 0:
                        print('\n\33[0;31mValor digitado é invalido.\033[m\n')
                        continue

                    elif valor == 0:
                        print('Operação cancelada.')
                        break

                    else:
                        saque = Saque(valor, conta_atual.saldo)
                        saque.registrar(conta_atual)
                        break
            else:
                print("\033[0;31mNenhuma conta foi selecionada.\033[m")

        elif opcao == 2:
            conta_atual = selecao_de_conta()

            if conta_atual:
                while True:
                    valor = funcoes.vericaint('\nDigite o valor que deseja depositar [0 para cancelar].\nR$')

                    if valor is None:
                        print('Operação cancelada.')
                        break

                    if valor == 0:
                        print('Operação cancelada.')
                        break

                    else:
                        deposito = Deposito(valor, conta_atual.saldo)
                        deposito.registrar(conta_atual)
                        break
            else:
                print("\033[0;31mNenhuma conta foi selecionada.\033[m")


        elif opcao == 3:
            conta_atual = selecao_de_conta()

            if conta_atual:
                    print('\n')
                    print(funcoes.titulo('EXTRATO'))
                    print(f'{"|TRANSAÇÃO":<23}|{"VALOR":>14}|{"SALDO":>14}|')
                    print(funcoes.linha())
                    for item in conta_atual.historico.transacoes:
                        print(f"|{item}")

                    print(funcoes.linha())
                    print(f"{'|Saldo:':<10} {'R$' + f'{conta_atual.saldo:.2f}':>42}|")
                    print(funcoes.linha())
            else:
                print("\033[0;31mNenhuma conta foi selecionada.\033[m")

        elif opcao == 4:

            while True:

                print('\nSelecione o tipo de cliente\n' \
                '[1] Pessoa Física.\n'
                '[2] Pessoa Juridica.\n'
                '[0] Sair.\n')

                tipo = funcoes.vericaint('Opção desejada: ')
                if tipo is None or tipo == 0:
                    print("\033[0;31mOperação de criação de conta cancelada.\033[m")
                    break

                if tipo == 1:
                    novo_cliente = criar_pessoa_fisica()
                    Cliente.adicionar_na_lista(novo_cliente)
                    break

                elif tipo == 2:
                    novo_cliente = criar_pessoa_juridica()
                    Cliente.adicionar_na_lista(novo_cliente)
                    break

                else:
                    print('Opção inválida.')

        elif opcao == 5:
            nrconta = criar_conta(nrconta)

        elif opcao == 6:
            listar_clientes()
                
        elif opcao == 7:
            listar_detalhes_conta()

        elif opcao == 8:
            print(funcoes.titulo('Obrigado por utilizar nossos serviços. Volte Sempre!'))
            break

        resp = input('\nDeseja realizar outra operação? [S/N]\n').upper()
        while resp not in 'NS':
            resp = input('\n\33[0;31mResposta invalida.\033[m\n'
                         'Deseja realizar outra operação? [S/N]\n').upper()
        if resp == 'N':
            print(funcoes.titulo('Obrigado por utilizar nossos serviços. Volte Sempre!'))
            break


if __name__ == '__main__':
    main()
