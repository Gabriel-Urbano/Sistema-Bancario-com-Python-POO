from abc import ABC
from typing import List

class Historico:
    def __init__(self):
        self.transacoes: List['Transacao'] = []

    def adicionar_transacao(self, transacao: 'Transacao'):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, _saldo: float, _numero: str, _agencia: str, _cliente: 'Cliente', _historico: Historico):
        self.saldo: float = _saldo
        self.numero: str = _numero
        self.agencia: str = _agencia
        self.cliente: 'Cliente' = _cliente
        self.historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: str) -> 'Conta':
        return cls(0.0, numero, '0001', cliente)

    def saldo(self) -> float:
        return self.saldo

    def sacar(self, valor: float) -> bool:
        if self.saldo < valor:
            print('Saldo insuficiente!')
            return False
        else:
            self.saldo -= valor
            print('Saldo realizado com sucesso!')
            return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print('Valor invalido!')
            return False
        else:
            self.saldo += valor
            print('Deposito realizado com sucesso!')
            return True

class Conta_corrente(Conta):
    def __init__(self, _saldo: float, _numero: str, _agencia: str, _cliente: 'Cliente', _historico: Historico, _limite: float, _limites_saques: int):
        super().__init__(_saldo, _numero, _agencia, _cliente, _historico)
        self.limite: float = _limite
        self.limites_saques: int = _limites_saques

class Transacao(ABC):
    def registrar(self, conta: 'Conta'):
        pass

class Deposito(Transacao):
    def __init__ (self, valor: float):
        self.valor: float = valor

    def registrar(self, conta: 'Conta'):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__ (self, valor: float):
        self.valor: float = valor

    def registrar(self, conta: 'Conta'):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Cliente:
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

class PessoaFisica(Cliente):
    def __init__ (self, _endereco: str, _contas: List['Conta'], _cpf: str, _nome: str, _data_nascimento: str):
        super().__init__(_endereco, _contas)
        self.cpf: str = _cpf
        self.nome: str = _nome
        self.data_nascimento: str = _data_nascimento

def main():
    print('Teste')








if __name__ == '__main__':
    main()