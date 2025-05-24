# Sistema de Banco (CLI) 💵
## Este é um projeto desenvolvido em Python que simula um sistema bancário simples via interface de linha de comando (CLI). O objetivo principal é demonstrar conceitos de Programação Orientada a Objetos (POO), como classes, herança, polimorfismo e encapsulamento, além de funcionalidades básicas de um banco como depósitos, saques e extrato.

# Funcionalidades Implementadas 🚀
O sistema oferece as seguintes operações:

- Depósito: Permite adicionar fundos a uma conta existente.=Saque: Permite retirar fundos de uma conta existente, com validações de saldo, limite por saque e limite diário de saques.
- Extrato: Exibe o histórico de transações de uma conta, mostrando o tipo de operação (saque/depósito), o valor e o saldo da conta após cada transação.
- Criação de Clientes:
  - Pessoa Física (PF): Permite cadastrar novos clientes do tipo pessoa física, com validação de CPF único.
  - Pessoa Jurídica (PJ): Permite cadastrar novos clientes do tipo pessoa jurídica, com validação de CNPJ único.
- Criação de Contas: Permite associar novas contas bancárias a clientes PF ou PJ já existentes. As contas são do tipo Conta Corrente.
- Listagem de Clientes: Exibe todos os clientes cadastrados, podendo filtrar por tipo (PF, PJ ou todos).
- Detalhes da Conta: Permite selecionar uma conta e exibir detalhes específicos, incluindo agência, número, proprietário, limites de saque e o histórico completo de transações.

# Estrutura do Projeto 📦
O projeto é modularizado e organizado em classes para melhor manutenção e compreensão:

- Historico: Responsável por armazenar as transações de uma conta.
- Conta: Classe base para tipos de contas, definindo comportamentos comuns como sacar e depositar.
  - ContaCorrente: Herda de Conta, implementando regras específicas para contas correntes (limite de saque, limite diário de saques).
- Transacao: Classe abstrata que define a interface para operações de transação.
- Deposito: Herda de Transacao, representa uma operação de depósito.
- Saque: Herda de Transacao, representa uma operação de saque.
- Cliente: Classe base abstrata para clientes, com métodos para realizar transações e adicionar contas. Gerencia uma lista estática de todos os clientes cadastrados e métodos para verificar CPF/CNPJ.
  - PessoaFisica: Herda de Cliente, representando um cliente pessoa física (com CPF, nome e data de nascimento).
  - PessoaJuridica: Herda de Cliente, representando um cliente pessoa jurídica (com CNPJ, nome e nome fantasia).
- funcoes_adicionais.py: Módulo separado para funções utilitárias como validação de CPF/CNPJ, inputs seguros, formatação de títulos, etc.
- main.py: O script principal que contém o loop do menu e orquestra a interação entre as classes e as funções utilitárias.

# Como Usar 🛠️ 
## Pré-requisitos: Certifique-se de ter o Python 3 instalado em seu sistema.
### Execução:
- Salve o código principal como main.py e o módulo de funções adicionais como funcoes_adicionais.py no mesmo diretório.
- Abra o terminal ou prompt de comando.
- Navegue até o diretório onde os arquivos foram salvos.
- Execute o comando:
```
python main.py
```
- Interação: Siga as instruções do menu apresentadas no terminal para realizar operações bancárias. O sistema iniciará com um cliente e uma conta já cadastrados para facilitar os testes.
