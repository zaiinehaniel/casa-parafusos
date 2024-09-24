 Casa dos Parafusos - Backend

## Descrição

Esta é a aplicação backend para a **Casa dos Parafusos**, desenvolvida com **FastAPI**. O backend serve como a camada de serviço que gerencia a lógica de negócios, manipulação de dados e comunicação com APIs externas, proporcionando um suporte robusto para a aplicação frontend.

## Funcionalidades

### 1. Controle de Acesso e Autenticação

O backend implementa um sistema de controle de acesso seguro, garantindo que apenas usuários autorizados possam acessar e manipular os dados. A autenticação é realizada por meio de tokens JWT, proporcionando uma experiência segura para os usuários.

### 2. Parametrização da Integração

Assim como no frontend, os usuários podem parametrizar a integração de acordo com suas necessidades. Essa funcionalidade permite que as configurações de como os dados são processados e apresentados sejam ajustadas facilmente.

### 3. Importação da Planilha Mercado Livre

O backend é responsável por processar e armazenar os dados importados de planilhas do Mercado Livre. Isso permite que as informações de vendas e produtos sejam facilmente gerenciadas e utilizadas na aplicação.

### 4. Comunicação com a API do Integrinn

O backend se comunica com a API do **Integrinn** para realizar operações de baixa de títulos e lançamento de transações financeiras. Com base nos dados da planilha importada, a aplicação pode registrar as transações necessárias de forma automatizada, facilitando a gestão financeira.
