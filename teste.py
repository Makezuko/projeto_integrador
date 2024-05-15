import mysql.connector

def obtemConexaoComMySQL(servidor, usuario, senha, bd): 
    try:
        conexao = mysql.connector.connect(
            host=servidor,
            user=usuario,
            passwd=senha,
            database=bd
        )
        print("Conexão ao banco de dados MySQL bem-sucedida!")
        return conexao
    except mysql.connector.Error as e:
        print("Erro ao conectar ao banco de dados MySQL:", e)
        return None

def comandoSQL(comando, select=False):
    conexao = obtemConexaoComMySQL("127.0.0.1", "root", "rootroot", "bd080324190")
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            
            if select:
                # Se for uma consulta SELECT, retorna os resultados
                dadosSelecionados = cursor.fetchall()
                for linha in dadosSelecionados:
                    print(linha)

            else:
                # Se for outro tipo de comando, como INSERT, UPDATE, DELETE, etc., apenas confirma e imprime uma mensagem
                conexao.commit()
                print("Operação bem-sucedida!")
                
        except mysql.connector.Error as e:
            print("Erro ao executar comando SQL:", e)
            
        finally:
            # Fechando a conexão
            if conexao.is_connected():
                cursor.close()
                conexao.close()
                print("Conexão ao banco de dados MySQL fechada.")

# Inserindo dados
comandoSQL("INSERT INTO dadosproduto (codigo, nome) VALUES (23232323, 'Neusa')")

# Selecionando dados
resultados = comandoSQL("SELECT * FROM dadosproduto WHERE codigo=23232323", select=True)
