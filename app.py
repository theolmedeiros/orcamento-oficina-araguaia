import streamlit as st
from fpdf import FPDF
from datetime import datetime

class OrcamentoPDF(FPDF):
    def header(self):
        self.image("logo_araguaia.png", 10, 8, 33)  # logo deve estar na mesma pasta
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "OFICINA ARAGUAIA - ORÇAMENTO DE SERVIÇOS", ln=True, align="C")
        self.ln(10)

    def add_cliente_info(self, cliente):
        self.set_font("Arial", size=10)
        for campo, valor in cliente.items():
            self.cell(0, 8, f"{campo}: {valor}", ln=True)
        self.ln(5)

    def add_itens(self, itens):
        self.set_font("Arial", "B", 10)
        self.cell(80, 8, "Descrição", 1)
        self.cell(30, 8, "Qtd", 1)
        self.cell(40, 8, "Valor Unit. (R$)", 1)
        self.cell(40, 8, "Total (R$)", 1)
        self.ln()

        total = 0
        self.set_font("Arial", size=10)
        for item in itens:
            desc = item['descricao']
            qtd = item['quantidade']
            valor = item['valor']
            subtotal = qtd * valor
            total += subtotal

            self.cell(80, 8, desc, 1)
            self.cell(30, 8, str(qtd), 1, align="C")
            self.cell(40, 8, f"{valor:.2f}", 1, align="R")
            self.cell(40, 8, f"{subtotal:.2f}", 1, align="R")
            self.ln()

        return total

    def add_resumo(self, total, desconto):
        self.set_font("Arial", "B", 10)
        self.cell(150, 8, "Subtotal (R$)", 1)
        self.cell(40, 8, f"{total:.2f}", 1, align="R")
        self.ln()
        self.cell(150, 8, "Desconto (R$)", 1)
        self.cell(40, 8, f"{desconto:.2f}", 1, align="R")
        self.ln()
        self.cell(150, 8, "TOTAL GERAL (R$)", 1)
        self.cell(40, 8, f"{total - desconto:.2f}", 1, align="R")
        self.ln(10)

    def add_observacoes(self, obs):
        self.set_font("Arial", size=10)
        self.multi_cell(0, 8, f"Observações: {obs}")
        self.ln(5)

    def add_footer(self, numero):
        self.set_font("Arial", size=10)
        self.cell(0, 8, f"Número do Orçamento: {numero}", ln=True)
        self.cell(0, 8, f"Data: {datetime.today().strftime('%d/%m/%Y')}", ln=True)
        self.ln(10)
        self.cell(0, 8, "Assinatura do responsável técnico: ___________", ln=True)

def gerar_orcamento_pdf(dados_cliente, itens, desconto, observacoes, numero):
    pdf = OrcamentoPDF()
    pdf.add_page()
    pdf.add_cliente_info(dados_cliente)
    total = pdf.add_itens(itens)
    pdf.add_resumo(total, desconto)
    pdf.add_observacoes(observacoes)
    pdf.add_footer(numero)
    nome_arquivo = f"orcamento_{numero}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo

# Streamlit UI
st.set_page_config(page_title="Gerador de Orçamentos - Oficina Araguaia")
st.title("📄 Gerador de Orçamentos - Oficina Araguaia")

with st.form("form_orcamento"):
    st.subheader("Informações do Cliente e Veículo")
    nome = st.text_input("Cliente")
    telefone = st.text_input("Telefone")
    endereco = st.text_input("Endereço")
    veiculo = st.text_input("Veículo")
    placa = st.text_input("Placa")
    chassi = st.text_input("Chassi")
    cor = st.text_input("Cor")

    st.subheader("Itens do Orçamento")
    qtd_itens = st.number_input("Quantos itens deseja inserir?", min_value=1, step=1)
    itens = []
    for i in range(int(qtd_itens)):
        st.markdown(f"*Item {i+1}*")
        desc = st.text_input(f"Descrição {i+1}", key=f"desc_{i}")
        qtd = st.number_input(f"Quantidade {i+1}", min_value=1, key=f"qtd_{i}")
        valor = st.number_input(f"Valor Unitário {i+1} (R$)", min_value=0.0, step=0.01, key=f"val_{i}")
        itens.append({"descricao": desc, "quantidade": qtd, "valor": valor})

    desconto = st.number_input("Desconto (R$)", min_value=0.0, step=0.01)
    observacoes = st.text_area("Observações")
    numero = st.text_input("Número do Orçamento")

    gerar
