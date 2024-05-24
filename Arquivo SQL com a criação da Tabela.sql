CREATE TABLE dadosProduto (
    codigo INT NOT NULL,
    nome VARCHAR(50),
    descricao VARCHAR(100),
    custo FLOAT(10, 2),          
    custo_prc FLOAT(5, 2),       
    custo_fixo FLOAT(10, 2),    
    fixo_prc FLOAT(5, 2),        
    comissao FLOAT(10, 2),      
    comissao_prc FLOAT(5, 2),   
    impostos FLOAT(10, 2),       
    impostos_prc FLOAT(5, 2),    
    rentabilidade FLOAT(10, 2),
    rentabilidade_reais FLOAT(10, 2),
    preco_venda FLOAT(10, 2),   
    PRIMARY KEY (codigo)
);
