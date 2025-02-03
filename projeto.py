import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar
from tkinter.ttk import Treeview
import mysql.connector
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

def linhas():
    print('-'*190)

def obtemConexaoComMySQL():
    servidor = os.getenv("DB_HOST")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    bd = os.getenv("DB_NAME")

    try:
        conexao = mysql.connector.connect(
            host=servidor,
            user=usuario,
            passwd=senha,
            database=bd
        )
        linhas()
        print("Conexão ao banco de dados MySQL bem-sucedida!")
        linhas()
        return conexao
    except mysql.connector.Error as e:
        print("Erro ao conectar ao banco de dados MySQL:", e)
        return None

def comandoSQL(comando, select=False):
    conexao = obtemConexaoComMySQL()
    resultado = None
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(comando)

            if select:
                dadosSelecionados = cursor.fetchall()
                if dadosSelecionados:
                    colunas = [i[0] for i in cursor.description]
                    resultado = (colunas, dadosSelecionados)
                else:
                    resultado = "Nenhum dado encontrado na tabela."
            else:
                conexao.commit()
                resultado = "Operação bem-sucedida!"
            
        except mysql.connector.Error as e:
            resultado = f"Erro ao executar comando SQL: {e}"

        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
                linhas()
                print("Conexão ao banco de dados MySQL fechada.")
                linhas()
    return resultado

def inserirDados():
    def submit():
        try:
            primary_key = int(entry_codigo.get())
            product_name = entry_nome.get().strip()
            product_description = entry_descricao.get().strip()
            product_price = float(entry_custo.get())
            fixed_price = float(entry_custo_fixo.get())
            commision = float(entry_comissao.get())
            taxes = float(entry_impostos.get())
            rentability = float(entry_rentabilidade.get())

            sale_price = (product_price / (1 - (fixed_price + commision + taxes + rentability) / 100))
            receita_bruta = sale_price - product_price
            fixed_price_reais = sale_price * (fixed_price / 100)
            commision_reais = sale_price * (commision / 100)
            taxes_reais = sale_price * (taxes / 100)
            rentability_reais = receita_bruta - (fixed_price_reais + commision_reais + taxes_reais)
            product_price_percentage = (product_price / sale_price) * 100

            valores = [
                primary_key,
                product_name,
                product_description,
                product_price,
                product_price_percentage,
                fixed_price_reais,
                fixed_price,
                commision_reais,
                commision,
                taxes_reais,
                taxes,
                rentability,
                rentability_reais,
                sale_price
            ]

            comando = f"""
                INSERT INTO dadosproduto 
                VALUES (
                    {primary_key}, '{product_name}', '{product_description}', {product_price}, {product_price_percentage}, 
                    {fixed_price_reais}, {fixed_price}, {commision_reais}, {commision}, 
                    {taxes_reais}, {taxes}, {rentability}, {rentability_reais}, {sale_price}
                )
            """
            result = comandoSQL(comando)
            messagebox.showinfo("Resultado", result)
            inserir_janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Erro! Verifique os valores inseridos.")

    inserir_janela = Toplevel()
    inserir_janela.title("Inserir Dados")

    labels = [
        "Código do produto", "Nome do produto", "Descrição do produto",
        "Custo do produto", "Percentual do custo fixo", "Percentual da comissão de vendas",
        "Percentual de impostos", "Percentual de rentabilidade desejado"
    ]

    entries = []

    for i, label in enumerate(labels):
        tk.Label(inserir_janela, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(inserir_janela)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    entry_codigo, entry_nome, entry_descricao, entry_custo, entry_custo_fixo, entry_comissao, entry_impostos, entry_rentabilidade = entries

    tk.Button(inserir_janela, text="Inserir", command=submit).grid(row=len(labels), columnspan=2, pady=10)

def classificarRentabilidade(rentabilidade):
    if rentabilidade > 20:
        return "Alto Lucro"
    elif 10 < rentabilidade <= 20:
        return "Lucro Médio"
    elif 0 < rentabilidade <= 10:
        return "Lucro Baixo"
    elif rentabilidade == 0:
        return "Equilíbrio"
    else:
        return "Prejuízo"

def exibirClassificacoesRentabilidade(rentabilidade):
    classificacoes_janela = Toplevel()
    classificacoes_janela.title("Classificações de Rentabilidade")

    tk.Label(classificacoes_janela, text=f"Rentabilidade do Produto: {rentabilidade:.2f}%").pack(pady=10)

    classificacoes = [
        ("> 20%", "Alto Lucro", rentabilidade > 20),
        ("10% - 20%", "Lucro Médio", 10 < rentabilidade <= 20),
        ("0% - 10%", "Lucro Baixo", 0 < rentabilidade <= 10),
        ("= 0%", "Equilíbrio", rentabilidade == 0),
        ("< 0%", "Prejuízo", rentabilidade < 0)
    ]

    for faixa, descricao, destaque in classificacoes:
        label_text = f"{faixa}: {descricao}"
        label = tk.Label(classificacoes_janela, text=label_text)
        if destaque:
            label.config(fg="red")
        label.pack(pady=2)

def exibirDetalhesProduto(produto):
    detalhes_janela = Toplevel()
    detalhes_janela.title("Detalhes do Produto")
    
    colunas = ["Descrição", "Valor", "%"]
    receita_bruta = float(produto[13]) - float(produto[3])
    detalhes = [
        ("Preço de Venda", produto[13], "100%"),
        ("Custo de Aquisição (Fornecedor)", produto[3], f"{float(produto[4]):.2f}%"),
        ("Receita Bruta (A-B)", f"{receita_bruta:.2f}", f"{100 - float(produto[4]):.2f}%"),
        ("Custo Fixo/Administrativo", produto[5], f"{float(produto[6]):.2f}%"),
        ("Comissão de Vendas", produto[7], f"{float(produto[8]):.2f}%"),
        ("Impostos", produto[9], f"{float(produto[10]):.2f}%"),
        ("Outros custos (D+E+F)", float(produto[5]) + float(produto[7]) + float(produto[9]), f"{float(produto[6]) + float(produto[8]) + float(produto[10]):.2f}%"),
        ("Rentabilidade (C-G)", produto[12], f"{float(produto[11]):.2f}%")
    ]

    tree = Treeview(detalhes_janela, columns=colunas, show='headings')
    tree.pack(side='left', fill='both', expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor='w', width=200)

    for detalhe in detalhes:
        tree.insert("", "end", values=detalhe)

    scrollbar = Scrollbar(detalhes_janela, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Adicionar evento de clique na rentabilidade
    def rentabilidadeClick(event):
        item = tree.selection()
        if item:
            valor = tree.item(item[0])['values']
            if valor[0].startswith("Rentabilidade"):
                rentabilidade = float(produto[11])
                exibirClassificacoesRentabilidade(rentabilidade)

    tree.bind("<Double-1>", rentabilidadeClick)

    # Adicionar botão de alteração
    alterar_btn = tk.Button(detalhes_janela, text="Alterar Dados", command=lambda: alterarDados(produto[0]))
    alterar_btn.pack(pady=10)

def verTabela():
    resultado = comandoSQL("SELECT * FROM dadosproduto", select=True)
    
    if isinstance(resultado, tuple):
        colunas, dadosSelecionados = resultado

        tabela_janela = Toplevel()
        tabela_janela.title("Tabela de Produtos")
        tree = Treeview(tabela_janela, columns=colunas, show='headings')
        tree.pack(side='left', fill='both', expand=True)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor='w', width=100)

        for linha in dadosSelecionados:
            tree.insert("", "end", values=linha)

        scrollbar = Scrollbar(tabela_janela, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        def itemSelecionado(event):
            item = tree.selection()
            if item:
                produto = tree.item(item[0])['values']
                exibirDetalhesProduto(produto)

        tree.bind("<<TreeviewSelect>>", itemSelecionado)

# Função para alterar dados na tabela
def alterarDados(codigo):
    def submit():
        try:
            product_name = entry_nome.get().strip()
            product_description = entry_descricao.get().strip()
            product_price = float(entry_custo.get())
            fixed_price = float(entry_custo_fixo.get())
            commision = float(entry_comissao.get())
            taxes = float(entry_impostos.get())
            rentability = float(entry_rentabilidade.get())

            sale_price = (product_price / (1 - (fixed_price + commision + taxes + rentability) / 100))
            receita_bruta = sale_price - product_price
            fixed_price_reais = sale_price * (fixed_price / 100)
            commision_reais = sale_price * (commision / 100)
            taxes_reais = sale_price * (taxes / 100)
            rentability_reais = receita_bruta - (fixed_price_reais + commision_reais + taxes_reais)
            product_price_percentage = (product_price / sale_price) * 100

            comando = f"""
                UPDATE dadosProduto
                SET 
                    nome = '{product_name}', 
                    descricao = '{product_description}', 
                    custo = {product_price}, 
                    custo_prc = {product_price_percentage}, 
                    custo_fixo = {fixed_price_reais}, 
                    fixo_prc = {fixed_price}, 
                    comissao = {commision_reais}, 
                    comissao_prc = {commision}, 
                    impostos = {taxes_reais}, 
                    impostos_prc = {taxes}, 
                    rentabilidade = {rentability}, 
                    rentabilidade_reais = {rentability_reais}, 
                    preco_venda = {sale_price}
                WHERE codigo = {codigo}
            """

            result = comandoSQL(comando)
            messagebox.showinfo("Resultado", result)
            alterar_janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Erro! Verifique os valores inseridos.")
            
    alterar_janela = Toplevel()
    alterar_janela.title("Alterar Dados")

    labels = [
        "Nome do produto", "Descrição do produto",
        "Custo do produto", "Percentual do custo fixo", "Percentual da comissão de vendas",
        "Percentual de impostos", "Percentual de rentabilidade desejado"
    ]

    entries = []

    for i, label in enumerate(labels):
        tk.Label(alterar_janela, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(alterar_janela)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    entry_nome, entry_descricao, entry_custo, entry_custo_fixo, entry_comissao, entry_impostos, entry_rentabilidade = entries

    tk.Button(alterar_janela, text="Alterar", command=submit).grid(row=len(labels), columnspan=2, pady=10)

# Função para apagar dados da tabela
def apagarDados():
    def submit():
        try:
            valor = int(entry_codigo.get())
            result = comandoSQL(f'DELETE FROM dadosproduto WHERE codigo = {valor}')
            messagebox.showinfo("Resultado", result)
            apagar_janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Erro! Verifique os valores inseridos.")
    
    apagar_janela = Toplevel()
    apagar_janela.title("Apagar Dados")

    tk.Label(apagar_janela, text="Código do produto").grid(row=0, column=0, padx=10, pady=5)
    entry_codigo = tk.Entry(apagar_janela)
    entry_codigo.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(apagar_janela, text="Apagar", command=submit).grid(row=1, columnspan=2, pady=10)

# Função principal para criar a interface gráfica
def criarJanela():
    janela = tk.Tk()
    janela.title("Gerenciador de Produtos")
    janela.geometry("300x200")

    tk.Button(janela, text="Ver Tabela", width=20, command=verTabela).pack(pady=10)
    tk.Button(janela, text="Inserir Dados", width=20, command=inserirDados).pack(pady=10)
    tk.Button(janela, text="Apagar Dados", width=20, command=apagarDados).pack(pady=10)
    tk.Button(janela, text="Sair", width=20, command=janela.quit).pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    criarJanela()
