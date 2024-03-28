# Ao definiar uma função, facilitamos o processo de escrever repetidamente os comandos. Uma função pode ter vários comandos;
# Neste caso, a função linhas() facilita a inserção de linhas de separação, ajudando no entendimento das informações no console.
def linhas():
    print('-'*130)

# O loop 'while' recebe uma condição, neste caso a condição booleana True;
# Enquanto a condição for mantida, o loop continuará; Caso a condição seja alterada, o loop será interrompido.
# A estrutura de controle 'if' recebe condições; 
# A estrutura 'and' delimita que ambas as condições tenham que ser atendidas para seguir os comandos.
# A estrutura 'else' delimita que em condições adversas às mencionadas, certos comandos sejam acionados.
while True:
    linhas()
    product_name = input('Insira o nome do produto: ')                                      #PN
    product_description = input('Insira a descrição do produto: ')                          #PD
    if product_name.strip() and product_description.strip():                                # .strip() é usado para tirar os espaços em branco.
        break                                                                               # break é utilizado para quebrar o loop.
    else:
        linhas()
        print('Erro! Você deve dar um nome e uma descrição ao produto a ser calculado, para isso você deve inserir pelo menos um caracter.')

while True:
    try:
        linhas()
        primary_key = int(input('Insira o código do produto: '))                            #PK
        break
    except ValueError:
        linhas()
        print('Erro! Você deve inserir o código do produto usando valores numéricos.')

while True:
    try:
        linhas()
        product_price = float(input('Insira o custo do produto: '))                         #CP
        fixed_price = float(input('Insira o percentual do custo fixo: '))                   #CF
        commision = float(input('Insira o percentual da comissão de vendas: '))             #CV
        taxes = float(input('Insira o percentual de impostos: '))                           #IV
        rentability = float(input('Insira o percentual de rentabilidade desejado: '))       #ML
        break
    except ValueError:
        linhas()
        print('Erro! Você deve inserir o custo do produto usando ponto como virgula; As porcentagens só devem aceitar valores numéricos (sem "%")')

sale_price = (product_price / (1 - (fixed_price + commision + taxes + rentability) / 100))      #Fórmula do preço de venda
receita_bruta = sale_price - product_price                                                      #Fórmula da receita bruta
fixed_price_reais = sale_price * (fixed_price/100)                                              #Fórmula para calcular o custo fixo em reais
commision_reais = sale_price * (commision/100)                                                  #Fórmula para calcular a comissão em reais
taxes_reais = sale_price * (taxes/100)                                                          #Fórmula para calcular impostos em reais
other_costs_reais = fixed_price_reais + commision_reais + taxes_reais                           #Fórmula para somar os custos em reais
other_costs = fixed_price + commision + taxes                                                   #Fórmula para somar os custos em porcentagem
rentability_reais = receita_bruta - other_costs_reais                                           #fórmula para calcular a rentabilidade em reais
product_price_percentage = (product_price/sale_price)*100                                       #Fórmula para calcular o valor do produto em percentagem
receita_bruta_percentage = (receita_bruta/sale_price)*100                                       #Fórmula para calcular a receita bruta em porcentagen

# Podemos definir matrizes para fazer tabelas no python.

tabela_valores = [
    ['Descrição',          'Valores',                            'Porcentagens'],
    ['Preço de venda',     'R${:.2f}'.format(sale_price),        '100.00%'],
    ['Custo de Aquisição', 'R${:.2f}'.format(product_price),     '{:.2f}%'.format(product_price_percentage)],  
    ['Receita bruta',      'R${:.2f}'.format(receita_bruta),     '{:.2f}%'.format(receita_bruta_percentage)], 
    ['Custo Fixo',         'R${:.2f}'.format(fixed_price_reais), '{:.2f}%'.format(fixed_price)],
    ['Comissão de vendas', 'R${:.2f}'.format(commision_reais),   '{:.2f}%'.format(commision)],
    ['Impostos',           'R${:.2f}'.format(taxes_reais),       '{:.2f}%'.format(taxes)],
    ['Outros custos',      'R${:.2f}'.format(other_costs_reais), '{:.2f}%'.format(other_costs)],
    ['Rentabilidade',      'R${:.2f}'.format(rentability_reais), '{:.2f}%'.format(rentability)],
]

linhas()
# Loop onde cada coluna da matriz será printada no console.
for item in tabela_valores:
    print(':',
        item[0],' '*(18-len(item[0])) + ':',                                                    # (x - len(item[y])) é uma fórmula que calcula quantos espaços em branco devem ser printados    
        item[1],' '*(7-len(item[1]))  + ':',                                                    # sendo 'x' o tamanho máximo da coluna, 'y' o index number da coluna da matriz a ser formatada
        item[2],' '*(12-len(item[2])) + ':')                                                    # e o comando len() serve para receber o tamanho da string e usá-lo na fórmula.

tabela_lucros = [
    ['Classificação', 'Lucro'],
    ['Alto', '> 20%'],
    ['Médio', '>  10% ; <= 20%'],
    ['Baixo', '>  0% ; <= 10%'],
    ['Equilíbrio', '=  0%'],
    ['Prejuízo', '<  0%'],
]

linhas()

print('Seguindo a seguinte tabela de lucros: ')

linhas()

for item in tabela_lucros:
    print(':',
          item[0],' '*(13-len(item[0])) + ':',
          item[1],' '*(15-len(item[1])) + ':'
          )

if rentability > 20:
    lucro = 'alto'
if rentability > 10 and rentability <= 20:
    lucro = 'médio'
if rentability > 0 and rentability <= 10:
    lucro = 'baixo'
if rentability == 0:
    lucro = 'nulo'
if rentability < 0:
    lucro = 'prejuízo'
    
linhas() 

print('O lucro do produto {} é classificado como {}.'.format(product_name.capitalize(), lucro))

linhas()
