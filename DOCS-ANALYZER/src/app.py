import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import detect_credit_card_info

def configure_interface():
    st.title("pload de Arquivo DIO - Desafio 1 - Azure  - Fake Docs")
    uploaded_file =  st.file_uploader("Escolha um arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        fileName = uploaded_file.name
        # Enviar para o blob storage
        blob_url = upload_blob(uploaded_file.getvalue(), fileName) # adicionei .getvalue()
        if blob_url:
            st.write(f"Arquivo {fileName} enviado com sucesso para o Azure Blob Storage")
            credit_cards_info = detect_credit_card_info(blob_url)
            show_image_and_validation(blob_url, credit_cards_info)
        else:
            st.write(f"Erro ao enviar o arquivo {fileName} para o Azure Blob Storage")

def show_image_and_validation(blob_url, credit_cards_info):
    st.image(blob_url, caption="Imagem enviada", use_column_width=True)
    st.write("Resultado da validação:")
    if credit_cards_info and credit_cards_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Cartão Válido</h1>", unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_cards_info["card_name"]}")
        st.write(f"Banco Emissor: {credit_cards_info["bank_name"]}")
        st.write(f"Data de Validade: {credit_cards_info["expiry_date"]}")
    else: 
        st.markdown(f"<h1 style='color: red;'>Cartão Inválido</h1>", unsafe_allow_html=True)
        st.write("Este não é um cartão de crédito válido:")

if __name__ == "__main__":
    configure_interface()
