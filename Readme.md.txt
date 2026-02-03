# 🛒 Armazenando dados de um E-Commerce na Cloud  
Bootcamp Microsoft Azure Cloud Native 2026

## 📌 Sobre o Projeto
Este projeto foi desenvolvido como parte do Bootcamp **Microsoft Azure Cloud Native 2026**.  
O objetivo é criar uma aplicação de **cadastro e listagem de produtos de um e-commerce**, utilizando **Azure Blob Storage** para armazenar imagens e **Azure SQL Database** para persistir os dados.  
A interface foi construída com **Streamlit**, permitindo interação direta via navegador.

---

## 🚀 Funcionalidades
- Cadastro de produtos com nome, preço, descrição e imagem
- Armazenamento de imagens no **Azure Blob Storage**
- Persistência dos dados no **Azure SQL Database**
- Listagem dos produtos em formato de **cards**
- Limpeza automática dos campos após salvar

---

## 🛠️ Tecnologias Utilizadas
- Python 3.10+
- Streamlit
- Azure Blob Storage
- Azure SQL Database
- PyODBC
- dotenv

---

## 📷 Prints da Aplicação 

### Banco de Dados - Microsoft SQL Server ![Banco de Dados](images/banco.png) 
### Cadastro de Produto - Atualizado ![Cadastro de Produto Atualizado](images/cadastro-atualizado.png) 
### Cadastro de Produto ![Cadastro de Produto](images/cadastro.png) 
### Listar Produtos ![Listar Produtos](images/listar.png)

## 💡 Insights e Aprendizados
- Como integrar **Blob Storage** com banco relacional.
- Uso de **session_state** no Streamlit para controlar estados.
- Organização do código em funções para maior clareza.
- Importância de variáveis de ambiente para segurança.

---

## 🔮 Possibilidades Futuras
- Autenticação de usuários.
- Filtros e busca de produtos.
- Design customizado com CSS.
- Edição e exclusão de produtos pela interface.

---

## ▶️ Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/ecommerce-azure-cloud.git
