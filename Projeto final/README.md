# Sistema de Gerenciamento de Biblioteca

Este projeto é um sistema web para gerenciamento de uma biblioteca, contendo uma API robusta e uma interface web interativa. O sistema permite o cadastro e gerenciamento de livros, autores e categorias, além de possuir um sistema de autenticação para usuários administradores.

Toda a aplicação é containerizada e pode ser orquestrada facilmente usando o Docker Compose.

---

## Tecnologias Utilizadas

O projeto é dividido em três serviços principais, orquestrados via Docker:

1. **Backend (API)**: Desenvolvido em Python utilizando o framework **FastAPI**, com **SQLAlchemy** (ORM) e autenticação via **JWT** (JSON Web Tokens).
2. **Banco de Dados**: **PostgreSQL 15**, responsável por armazenar todos os dados relacionais do sistema.
3. **Frontend**: Desenvolvido com **Flask** (Python) e **Jinja2** para renderização de templates HTML, utilizando CSS/JS puro para interatividade e comunicação com a API via chamadas assíncronas (`fetch`).
4. **Testes**: Conjunto de testes unitários desenvolvidos com **Pytest**, rodando em um banco SQLite em memória.

---

## Como Executar o Projeto

Certifique-se de ter o **Docker** e o **Docker Compose** (ou Docker Desktop) instalados em sua máquina.

1. **Clone o repositório** ou navegue até a pasta raiz do projeto.
2. **Configure as variáveis de ambiente**:
   - Faça uma cópia do arquivo `.env.example` e renomeie para `.env`.
   - Caso deseje, altere as senhas e chaves secretas dentro do arquivo `.env` gerado.
3. **Inicie os serviços** utilizando o Docker Compose:

   ```bash
   docker-compose up --build
   ```

   *Dica: Adicione a flag `-d` no final se quiser rodar em background (detached mode).*

3. O Docker irá realizar o build das imagens, instalar as dependências e iniciar 4 containers:
   - `biblioteca_db`: O banco de dados PostgreSQL.
   - `biblioteca_api`: A API FastAPI rodando na porta **8000**.
   - `biblioteca_frontend`: A interface web Flask rodando na porta **3002**.
   - `biblioteca_tests`: Container que executa automaticamente a suíte de testes usando Pytest na inicialização.

### Acessando a Aplicação

- **Interface Web (Frontend)**: [http://localhost:3002](http://localhost:3002)
- **Documentação da API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentação Alternativa (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Boas Práticas e Fluxo de Uso

Para garantir a integridade relacional do banco de dados e o funcionamento correto do sistema, siga as instruções abaixo:

### 1. Primeiros Passos: Autenticação
Todo o acesso de escrita no sistema (criação, edição e exclusão) requer que você esteja autenticado.
- Ao acessar o frontend, você será direcionado para a página de **Login / Registro**.
- Se for seu primeiro acesso, alterne para **Registro**, crie um usuário, e depois faça o **Login**.

### 2. Cadastro Base (Categorias e Autores)
O sistema exige que um livro pertença a pelo menos uma **Categoria**. Além disso, é boa prática que ele possua um **Autor**.
> **IMPORTANTE:** Não é possível cadastrar um livro sem antes ter pelo menos uma Categoria cadastrada no sistema.

*Vá para a página **Gerenciar** no menu superior.*
- **Passo A (Categorias)**: Cadastre as categorias literárias desejadas (ex: Romance, Fantasia, Tecnologia). O sistema já faz um *seed* automático de algumas categorias iniciais na primeira inicialização, mas você pode adicionar mais.
- **Passo B (Autores)**: Cadastre os autores dos livros que você deseja inserir no sistema.

### 3. Cadastro de Livros
Somente após realizar o Passo 2, proceda com o cadastro de livros.
- Na seção **Livros** (ainda na página de Gerenciamento), preencha os dados do livro.
- Selecione o Autor na lista suspensa.
- Selecione **uma ou mais** Categorias.
- Clique em Cadastrar.

### 4. Gestão e Pesquisa
- Utilize o **Dashboard** para visualizar a lista completa de livros.
- A barra de pesquisa permite filtrar rapidamente por título do livro, nome do autor ou categoria específica.
- Ao clicar no nome de um Autor na lista, você será levado para uma página detalhada com informações do autor e todos os seus livros.
- Você pode editar as informações de um livro ou excluí-lo diretamente pela página de **Gerenciar**.

---

## Executando os Testes Unitários

O projeto possui mais de 15 testes unitários (escritos em Pytest) garantindo o funcionamento da API (autenticação, crud de livros, autores e categorias).

Como o `docker-compose.yml` foi configurado com um container dedicado de testes (`biblioteca_tests`), os testes rodam automaticamente toda vez que você sobe a aplicação.

Para visualizar o resultado da execução dos testes:
1. Pelo terminal (caso não tenha rodado em detached mode), você verá os logs do container de testes indicando o progresso e o número de testes passados.
2. Pelo **Docker Desktop**, acesse o container `biblioteca_tests` e visualize a aba "Logs".

*(O container de testes roda uma vez, reporta os resultados e então é finalizado, sem consumir recursos contínuos, enquanto o banco, API e frontend permanecem ativos).*
