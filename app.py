import streamlit as st
import json

st.set_page_config(page_title="Validador TCESP", layout="wide")

st.title("Validador de JSON - Prestação de Contas TCESP")
st.write("Faça o upload do seu arquivo JSON para checar documentos com rateio em 100% ou encargos iguais/superiores ao valor bruto.")

# Dicionário para converter o número do mês no nome em português
NOME_DOS_MESES = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Março",
    "04": "Abril", "05": "Maio", "06": "Junho",
    "07": "Julho", "08": "Agosto", "09": "Setembro",
    "10": "Outubro", "11": "Novembro", "12": "Dezembro"
}

arquivo = st.file_uploader("Arraste ou selecione o arquivo JSON", type=["json"])

if arquivo is not None:
    try:
        dados = json.load(arquivo)
        st.success("✅ Arquivo carregado e lido com sucesso!")

        st.subheader("Análise de Inconsistências nos Documentos Fiscais")
        erros_encontrados = []

        # Varredura do bloco de documentos fiscais
        documentos = dados.get("documentos_fiscais", [])
        
        for i, doc in enumerate(documentos):
            percentual = doc.get("rateio_percentual")
            tipo_rateio = doc.get("rateio_proveniente_tipo", "Não informado")
            
            # Capturando os dados de valores
            valor_bruto = doc.get("valor_bruto", 0.0)
            valor_encargos = doc.get("valor_encargos", 0.0)
            
            # Captura e formata o mês da data_emissao
            data_emissao = doc.get("data_emissao", "")
            nome_mes = "Não informado"
            if data_emissao and len(data_emissao) >= 7:
                numero_mes = data_emissao[5:7] 
                nome_mes = NOME_DOS_MESES.get(numero_mes, "Inválido")
            
            # 1. Busca por rateio igual a 100
            erro_rateio = percentual in [100, 100.0, "100", "100.0", "100.00", "100,00"]
            
            # 2. Busca por encargos iguais ou maiores que o valor bruto
            erro_encargos = False
            try:
                # Converte para float para garantir precisão na matemática
                v_bruto = float(valor_bruto)
                v_encargos = float(valor_encargos)
                # O manual do TCESP exige que encargos seja estritamente MENOR que o valor bruto
                if v_encargos >= v_bruto and v_bruto > 0:
                    erro_encargos = True
            except (ValueError, TypeError):
                pass # Ignora caso os campos venham vazios ou com texto não numérico

            # Se falhou em alguma das regras, adiciona à lista
            if erro_rateio or erro_encargos:
                motivos = []
                if erro_rateio: motivos.append("Rateio 100%")
                if erro_encargos: motivos.append("Encargos ≥ Valor Bruto")

                num_doc = doc.get("numero", "Não informado")
                descricao = doc.get("descricao", "Sem descrição")
                
                erros_encontrados.append({
                    "Índice JSON": i,
                    "Motivo do Erro": " + ".join(motivos),
                    "Nº Doc": num_doc,
                    "Mês": nome_mes,
                    "Descrição": descricao,
                    "Valor Bruto": valor_bruto,
                    "Valor Encargos": valor_encargos,
                    "Tipo Rateio": tipo_rateio,
                    "% Rateio": percentual
                })

        # Exibição dos resultados
        if erros_encontrados:
            st.error(f"❌ Encontramos {len(erros_encontrados)} documento(s) com inconsistências.")
            st.dataframe(erros_encontrados, use_container_width=True)
            st.info("💡 **Ação recomendada:** No JSON, remova o campo `rateio_percentual` caso seja 100. Para os encargos, garanta que `valor_encargos` não seja uma cópia do valor bruto; se não houve retenção extra, o valor de encargos deve ser 0.")
        else:
            st.success("🎉 Nenhum documento com rateio igual a 100% ou encargos inconsistentes foi encontrado.")

    except json.JSONDecodeError:
        st.error("O arquivo selecionado não é um JSON válido. Verifique a formatação.")