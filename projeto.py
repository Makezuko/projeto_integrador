import mysql.connector
# SQL Connector é uma biblioteca usada para conectar o SQL ao Python.
# Ao definiar uma função, facilitamos o processo de escrever repetidamente os comandos. Uma função pode ter vários comandos;
# Neste caso, a função linhas() facilita a inserção de linhas de separação, ajudando no entendimento das informações no console.
def linhas():
    print('-'*190)

def obtemConexaoComMySQL(servidor, usuario, senha, bd):
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

# Função para executar comandos SQL
def comandoSQL(comando, select=False):
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "rootroot", "bd080324190")
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            
            if select:
                dadosSelecionados = cursor.fetchall()
                if dadosSelecionados:
                    colunas = [i[0] for i in cursor.description] # Acessamos a propriedade description do cursor, que é uma sequência de tuplas. Cada tupla representa uma coluna na tabela.
                    # Definindo larguras das colunas
                    larguras = [max(len(str(dado)) for dado in coluna) for coluna in zip(colunas, *dadosSelecionados)] # Calculamos a largura necessária da coluna a partir da quantidade de caracteres no nome da Coluna. Essas larguras são armazenadas na lista larguras.
                    # Imprimindo cabeçalho da tabela
                    print(" | ".join("{:{}}".format(coluna, largura) for coluna, largura in zip(colunas, larguras))) # Utilizamos "{:{}}" na string de formatação para garantir que cada coluna seja impressa com a largura apropriada.
                    # Imprimindo linha de separação
                    linhas()
                    # Imprimindo os dados
                    for linha in dadosSelecionados:
                        print(" | ".join("{:{}}".format(dado, largura) for dado, largura in zip(linha, larguras))) # A cada linha de informação é printado o dado com o espaçamento necessário.
                else:
                    print("Nenhum dado encontrado na tabela.")
            else:
                conexao.commit()
                linhas()
                print("Operação bem-sucedida!")
                
        except mysql.connector.Error as e:
            print("Erro ao executar comando SQL:", e)
            
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
                linhas()
                print("Conexão ao banco de dados MySQL fechada.")

# A função inserirDados() pede ao usuário os dados que serão inseridos, sendo acessível através do menu.
def inserirDados():
    while True:
        try:
            linhas()
            primary_key = int(input('Insira o código do produto: '))
            break
        except ValueError:
            linhas()
            print('Erro! Você deve inserir o código do produto usando valores numéricos.')

    while True:
        linhas()
        product_name = input('Insira o nome do produto: ')
        product_description = input('Insira a descrição do produto: ')
        if product_name.strip() and product_description.strip():
            break
        else:
            linhas()
            print('Erro! Você deve dar um nome e uma descrição ao produto a ser calculado, para isso você deve inserir pelo menos um caracter.')

    while True:
        try:
            linhas()
            product_price = float(input('Insira o custo do produto: '))
            fixed_price = float(input('Insira o percentual do custo fixo: '))
            commision = float(input('Insira o percentual da comissão de vendas: '))
            taxes = float(input('Insira o percentual de impostos: '))
            rentability = float(input('Insira o percentual de rentabilidade desejado: '))
            break
        except ValueError:
            linhas()
            print('Erro! Você deve inserir o custo do produto usando ponto como vírgula; As porcentagens só devem aceitar valores numéricos (sem "%")')

    # Calculando valores derivados
    sale_price = (product_price / (1 - (fixed_price + commision + taxes + rentability) / 100))
    receita_bruta = sale_price - product_price
    fixed_price_reais = sale_price * (fixed_price / 100)
    commision_reais = sale_price * (commision / 100)
    taxes_reais = sale_price * (taxes / 100)
    rentability_reais = receita_bruta - (fixed_price_reais + commision_reais + taxes_reais)
    product_price_percentage = (product_price / sale_price) * 100

    # Verificar se todos os valores estão presentes
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

    print("Valores a serem inseridos:", valores)

    comandoSQL("INSERT INTO dadosproduto VALUES ({}, '{}', '{}', {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f})".format(
        *valores
    ))
# Esta função tem que ser completamente mudada.

def verTabela():
    comandoSQL('SELECT * FROM dadosproduto;', select= True)


def apagarDados():
    linhas()
    valor = int(input('Insira o Codigo do produto que deseja apagar: '))
    comandoSQL('DELETE FROM dadosproduto WHERE codigo = {}'.format(valor))

def opcaoEscolhida(opcoes):
    linhas()
    opcoesValidas = []
    posicao = 0
    while posicao < len(opcoes):
        print(posicao + 1, ') ', opcoes[posicao], sep='')
        opcoesValidas.append(str(posicao + 1))
        posicao += 1
    opcao = input("Escolha uma opção: ")
    if opcao in opcoesValidas:
        return int(opcao)
    else:
        print("Opção inválida.")
        return 0

opcoes = [
    "Ver tabela",
    "Inserir dados",
    "Apagar dados",
    "Sair"
]

def menu():
    opcao = 0
    while opcao != 5:
        opcao = opcaoEscolhida(opcoes)
        if opcao == 1:
            verTabela()
        elif opcao == 2:
            inserirDados()
        elif opcao == 3:
            apagarDados()
        elif opcao == 4:
            break

menu()