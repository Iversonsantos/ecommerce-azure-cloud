import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pyodbc
import uuid
from dotenv import load_dotenv

load_dotenv()

BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountName = os.getenv("BLOB_ACCOUNT_NAME")    

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")


# Função para salvar imagem no Azure Blob Storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url


# Função para salvar produto no banco
def salvar_produto(product_name, product_price, product_description, product_image):
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={SQL_DATABASE};'
            f'UID={SQL_USER};'
            f'PWD={SQL_PASSWORD}'
        )
        cursor = connection.cursor()

        image_url = upload_blob(product_image)

        sql = "INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (product_name, product_price, product_description, image_url))

        connection.commit()
        cursor.close()
        connection.close()

        return True

    except Exception as e:
        st.error(f"Erro ao inserir produto: {e}")
        return False


# Função para listar produtos do banco
def list_products():
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SQL_SERVER};'
            f'DATABASE={SQL_DATABASE};'
            f'UID={SQL_USER};'
            f'PWD={SQL_PASSWORD}'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT nome, descricao, preco, imagem_url FROM Produtos")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append({
                "nome": row[0],
                "descricao": row[1],
                "preco": row[2],
                "imagem_url": row[3]
            })

        cursor.close()
        connection.close()
        return products

    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []


# Função para exibir os produtos na tela
def list_produtos_screen():
    products = list_products()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["imagem_url"]:
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto cadastrado ainda.")

# ---------------- INTERFACE STREAMLIT ----------------

st.title('Cadastro de Produtos')

# Limpa os campos ANTES de renderizar os inputs
if "limpar_campos" in st.session_state and st.session_state.limpar_campos:
    st.session_state.update({
        "product_name": "",
        "product_price": 0.0,
        "product_description": "",
        "limpar_campos": False
    })
    # não mexe em product_image, o usuário troca manualmente

# Campos com chave para controle
product_name = st.text_input('Nome do Produto', key="product_name")
product_price = st.number_input('Preço do Produto', min_value=0.0, format="%.2f", key="product_price")
product_description = st.text_area('Descrição do Produto', key="product_description")
product_image = st.file_uploader('Imagem do Produto', type=['jpg', 'jpeg', 'png'], key="product_image")

# Botão de salvar
if st.button('Salvar Produto'):
    sucesso = salvar_produto(product_name, product_price, product_description, product_image)
    if sucesso:
        st.success("Produto salvo com sucesso!")
        st.session_state.limpar_campos = True  # ativa a flag para limpar na próxima execução

# Seção de produtos cadastrados
st.header('Produtos Cadastrados')

if st.button('Listar Produtos'):
    list_produtos_screen()
