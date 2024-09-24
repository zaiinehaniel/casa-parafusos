# Casa dos Parafusos - Projeto Integrado

## Descrição

O projeto **Casa dos Parafusos** é uma aplicação integrada que consiste em um frontend desenvolvido em **Angular** e um backend em **FastAPI**. O sistema é projetado para gerenciar e integrar dados de vendas e produtos, com foco em uma interface amigável e um backend robusto.

## Funcionalidades

### Frontend (Angular)

- **Controle de Acesso e Autenticação**: Sistema de autenticação seguro utilizando tokens JWT.
- **Parametrização da Integração**: Permite ajustes nas configurações de integração.
- **Importação da Planilha Mercado Livre**: Processa dados de vendas e produtos a partir de planilhas do Mercado Livre.

### Backend (FastAPI)

- **Controle de Acesso e Autenticação**: Gerencia usuários e suas permissões.
- **Parametrização da Integração**: Configurações ajustáveis para integração.
- **Importação da Planilha Mercado Livre**: Armazena e processa dados importados.
- **Comunicação com a API do Integrinn**: Realiza baixa de títulos e lançamentos financeiros com base nos dados importados.

## Pré-requisitos

- Docker e Docker Compose instalados em sua máquina.

## Instruções para Execução

### 1. Clone o Repositório

Clone o repositório para sua máquina local:

```bash
git clone <URL do repositório>
cd casa-parafusos
docker-compose up --build
