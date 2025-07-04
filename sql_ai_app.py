#AI SQL Query Generator Text-to-SQL

# Imports
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega o arquivo de variáveis de ambiente
load_dotenv()   

# Carrega a variável de ambiente da API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura a chamada ao modelo via API
genai.configure(api_key=GOOGLE_API_KEY)

# Cria instância do modelo de IA
modelo_ai_dsa = genai.GenerativeModel('gemini-2.0-flash')

# Função para gerar a resposta do modelo de IA
def dsa_gera_resposta_modelo(prompt):
    try:
        response = modelo_ai_dsa.generate_content(prompt)
        return response.text.strip().lstrip("```sql").rstrip("```")
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {str(e)}")
        return None

# Função para download do resultado do modelo
def dsa_download_resultado(sql_query, e_output, explicacao):
    conteudo = f"Consulta SQL:\n{sql_query}\n\nSaída Esperada:\n{e_output}\n\nExplicação:\n{explicacao}"
    st.download_button("📥 Baixar Resultado", conteudo, file_name="dsa_resultado_query.sql", mime="text/plain")

# Função principal
def main():
    # Configuração da página
    st.set_page_config(page_title="Gerador SQL com IA", page_icon=":robot_face:", layout="wide")

    # Sidebar com instruções
    with st.sidebar:
        st.header("📘 Instruções")
        st.markdown("""
        - Descreva claramente o que deseja consultar.
        - Clique no botão **Gerar Query SQL**.
        - A IA vai gerar:
            - O template da consulta SQL
            - Um exemplo da saída
            - Uma explicação da consulta
        - Melhor descrição = melhor resultado!
        - **Importante**: revise sempre o resultado. A IA pode errar.
        """)
        if st.button("📧 Suporte"):
            st.write("Dúvidas? Envie um e-mail para: ulyssespontes82@gmail.com")

    # Título com estilo HTML
    st.markdown(
        """
        <style>
        .titulo-principal {
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f2f6;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
        }
        .titulo-principal h1 {
            color: #004c99;
            font-size: 40px;
            margin-bottom: 10px;
        }
        .titulo-principal h2 {
            color: #336699;
            font-size: 26px;
            margin-bottom: 5px;
        }
        .titulo-principal h3 {
            color: #666666;
            font-size: 18px;
            margin-bottom: 15px;
        }
        .titulo-principal p, ul {
            font-size: 16px;
            color: #333333;
            margin: 10px auto;
            max-width: 700px;
        }
        hr {
            border: none;
            border-top: 1px solid #cccccc;
            margin: 20px 0;
        }
        </style>

        <div class="titulo-principal">
            <h1>Gerador de Queries SQL com IA</h1>
            <h2>Text-to-SQL Automático</h2>
            <h3>por Ulysses Pontes</h3>
            <hr>
            <p>Este app utiliza IA para gerar automaticamente consultas SQL baseadas em descrições em linguagem natural.</p>
            <ul style="text-align: left;">
                <li>🧠 Geração inteligente da consulta SQL</li>
                <li>📊 Exemplo da saída esperada</li>
                <li>🧾 Explicação da sintaxe utilizada</li>
                <li>📥 Download do resultado em .sql</li>
            </ul>
            <hr>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Entrada do usuário
    text_input = st.text_area("📝 Descreva a consulta SQL que deseja:")

    # Botão para gerar query
    submit = st.button(label='⚙️ Gerar Query SQL')

    if submit:
        if len(text_input.strip()) < 10:
            st.warning("Por favor, forneça uma descrição mais detalhada.")
            return

        with st.spinner("🤖 A IA está processando sua solicitação..."):
            sql_query = dsa_gera_resposta_modelo(f"Crie de forma clara, objetiva e profissional, uma consulta SQL baseada neste texto: {text_input}")

            if sql_query:
                e_output = dsa_gera_resposta_modelo(f"Mostre um exemplo da saída esperada para: {sql_query}")
                explicacao = dsa_gera_resposta_modelo(f"Avalie e detalhe a explicação da sintaxe desta consulta SQL, descrevendo cada cláusula e função utilizada: {sql_query}")

                # Abas com os resultados
                tab1, tab2, tab3 = st.tabs(["🧾 Consulta SQL", "📊 Saída Esperada", "📚 Explicação"])

                with tab1:
                    st.code(sql_query, language="sql")
                with tab2:
                    st.markdown(e_output)
                with tab3:
                    st.markdown(explicacao)

                # Botão de download
                dsa_download_resultado(sql_query, e_output, explicacao)

# Executa a aplicação
main()
