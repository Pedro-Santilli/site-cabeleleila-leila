# Documentação do Sistema de Agendamento

# Sistema de Agendamento - Documentação

## Visão Geral

Este é um sistema de agendamento desenvolvido em Flask, utilizando Pandas para manipulação de dados. O sistema permite que usuários façam login, se cadastrem, realizem agendamentos e visualizem ou editem seus agendamentos existentes. Também inclui funcionalidades administrativas para gerenciar todos os agendamentos.

## Estrutura do Código

O código está organizado em várias rotas Flask, cada uma responsável por uma funcionalidade específica do sistema.

### Rotas Principais

- **/ (GET, POST)**: Rota de login
    - Verifica as credenciais do usuário
    - Redireciona para a página de agendamento ou admin conforme o tipo de usuário
- **/cadastro (GET, POST)**: Rota para cadastro de novos usuários
    - Verifica se o email já está em uso
    - Adiciona novo usuário ao banco de dados
- **/agendamento (GET, POST)**: Rota para realizar agendamentos
    - Exibe formulário de agendamento (GET)
    - Processa novo agendamento (POST)
- **/ver-agendamentos**: Exibe os agendamentos do usuário logado
- **/edit (GET, POST)**: Permite edição de agendamentos
    - Exibe formulário de edição (GET)
    - Processa a edição do agendamento (POST)
- **/ver-agendamentos-admin**: Exibe todos os agendamentos (acesso administrativo)
- **/edit-admin (GET, POST)**: Permite que o admin edite qualquer agendamento
    - Exibe formulário de edição (GET)
    - Processa a edição do agendamento (POST)

## Funcionalidades Principais

### 1. Autenticação de Usuários

O sistema utiliza sessões Flask para manter o estado de login do usuário. A rota de login verifica as credenciais contra um DataFrame de usuários.

### 2. Cadastro de Usuários

Novos usuários podem se cadastrar fornecendo nome de usuário, senha e email. O sistema verifica duplicatas de email antes de adicionar um novo usuário.

### 3. Agendamentos

Usuários autenticados podem criar novos agendamentos. O sistema verifica conflitos de horário antes de confirmar um novo agendamento.

### 4. Visualização e Edição de Agendamentos

Usuários podem ver seus próprios agendamentos e editá-los, desde que a data do agendamento seja mais de dois dias no futuro.

### 5. Funcionalidades Administrativas

Um usuário admin pode ver e editar todos os agendamentos no sistema.

## Manipulação de Dados

O sistema utiliza Pandas para manipular dados, armazenando informações em arquivos Excel:

- Usuários são armazenados em 'database\usuariosdb.xlsx'
- Agendamentos são armazenados em 'database\servico.xlsx'

## Segurança

O sistema implementa verificações básicas de segurança:

- Verificação de credenciais no login
- Verificação de conflitos de agendamento
- Restrição de edição de agendamentos próximos

## Melhorias Futuras

- Implementar criptografia de senhas
- Adicionar validação mais robusta de entradas do usuário
- Implementar um sistema de banco de dados mais robusto
- Adicionar logging para melhor rastreamento de atividades
