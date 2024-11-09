import pandas as pd
from datetime import datetime
from tabulate import tabulate

# Estruturas de dados (DataFrames)
produtos_df = pd.DataFrame(columns=['id_produto', 'nome_produto', 'categoria', 'quantidade', 'preco'])
categorias_df = pd.DataFrame(columns=['id_categoria', 'nome_categoria'])
movimentacoes_df = pd.DataFrame(columns=['id_movimento', 'id_produto', 'tipo', 'quantidade', 'data'])


# Cadastro de Produtos
def cadastrar_produto(nome_produto, id_categoria=None, quantidade=0, preco=0.0):
    global produtos_df
    
    # Verifica se o nome_produto não foi inserido
    if not nome_produto or nome_produto.strip() == "":
        print("Erro: Nome do produto não pode ser vazio.")
        return
    
    # Verifica se o nome_produto já existe
    if nome_produto in produtos_df['nome_produto'].values:
        print(f"Erro: Produto com nome '{nome_produto}' já existe.")
        return

    # Gera automaticamente o próximo ID de produto
    novo_id_produto = len(produtos_df) + 1

    # Verifica se o id_categoria existe, se não, atribui None
    if id_categoria is not None and id_categoria not in categorias_df['id_categoria'].values:
        print(f"Erro: Categoria com ID '{id_categoria}' não encontrada. O produto será cadastrado sem categoria.")
        id_categoria = None

    # Adiciona o novo produto ao DataFrame
    novo_produto = pd.DataFrame({
        'id_produto': [novo_id_produto],
        'nome_produto': [nome_produto],
        'categoria': [id_categoria],
        'quantidade': [quantidade],
        'preco': [preco]
    })

    # Condicional para evitar concatenação de DataFrames vazios
    produtos_df = (
        produtos_df.copy() if novo_produto.empty else
        novo_produto.copy() if produtos_df.empty else
        pd.concat([produtos_df, novo_produto], ignore_index=True, sort=False)
    )
    print(f"Produto '{nome_produto}' cadastrado com sucesso.")


# Cadastro de Categoria
def cadastrar_categoria(nome_categoria):
    global categorias_df
    
    # Verifica se a categoria já existe
    if nome_categoria in categorias_df['nome_categoria'].values:
        print(f"Erro: Categoria '{nome_categoria}' já existe.")
        return
    
    # Adiciona a nova categoria ao DataFrame
    nova_categoria = pd.DataFrame({
        'id_categoria': [len(categorias_df) + 1],
        'nome_categoria': [nome_categoria]
    })
    
    # Condicional para evitar concatenação de DataFrames vazios
    categorias_df = (
        categorias_df.copy() if nova_categoria.empty else
        nova_categoria.copy() if categorias_df.empty else
        pd.concat([categorias_df, nova_categoria], ignore_index=True)
    )
    print(f"Categoria '{nome_categoria}' cadastrada com sucesso.")


# Registra Movimentação de Estoque
def registrar_movimentacao(id_produto, tipo, quantidade):
    global movimentacoes_df
    
    if id_produto not in produtos_df['id_produto'].values:
        print(f"Erro: Produto com ID '{id_produto}' não encontrado.")
        return
    
    nova_movimentacao = pd.DataFrame({
        'id_movimento': [len(movimentacoes_df) + 1],
        'id_produto': [id_produto],
        'tipo': [tipo],
        'quantidade': [quantidade],
        'data': [datetime.now()]
    })
    
    # Condicional para evitar concatenação de DataFrames vazios
    movimentacoes_df = (
        movimentacoes_df.copy() if nova_movimentacao.empty else
        nova_movimentacao.copy() if movimentacoes_df.empty else
        pd.concat([movimentacoes_df, nova_movimentacao], ignore_index=True, sort=False)
    )
    print(f"Movimentação '{tipo}' registrada para o produto ID {id_produto} com quantidade {quantidade}.")


# Adicionar quantidade ao estoque de um produto
def adiciona_quantidade_estoque(id_produto, quantidade):
    global produtos_df
    
    if id_produto not in produtos_df['id_produto'].values:
        print(f"Erro: Produto com ID '{id_produto}' não encontrado.")
        return
    
    produtos_df.loc[produtos_df['id_produto'] == id_produto, 'quantidade'] += quantidade
    print(f"Quantidade adicionada: {quantidade} ao produto ID {id_produto}. Estoque atualizado.")
    
    # Registrar a movimentação de entrada
    registrar_movimentacao(id_produto, 'entrada', quantidade)


# Remover quantidade do estoque de um produto
def remove_quantidade_estoque(id_produto, quantidade):
    global produtos_df
    
    if id_produto not in produtos_df['id_produto'].values:
        print(f"Erro: Produto com ID '{id_produto}' não encontrado.")
        return
    
    estoque_atual = produtos_df.loc[produtos_df['id_produto'] == id_produto, 'quantidade'].values[0]
    if estoque_atual < quantidade:
        print(f"Erro: Quantidade insuficiente em estoque para o produto ID {id_produto}.")
        return
    
    produtos_df.loc[produtos_df['id_produto'] == id_produto, 'quantidade'] -= quantidade
    print(f"Quantidade removida: {quantidade} do produto ID {id_produto}. Estoque atualizado.")
    
    # Registrar a movimentação de saída
    registrar_movimentacao(id_produto, 'saida', quantidade) 


# Gerar relatório de todos os produtos em estoque
def gerar_relatorio_produtos():
    if produtos_df.empty:
        print("Nenhum produto cadastrado no estoque.")
        return
    
    relatorio_produtos = produtos_df[['id_produto', 'nome_produto', 'categoria', 'quantidade', 'preco']]
    print("\nRelatório de Produtos em Estoque:")
    print(tabulate(relatorio_produtos, headers='keys', tablefmt='fancy_grid', showindex=False))


# Gerar um relatório de todas as movimentações
def gerar_relatorio_movimentacoes():
    if movimentacoes_df.empty:
        print("Nenhuma movimentação registrada.")
        return

    relatorio_movimentacoes = movimentacoes_df[['id_movimento', 'id_produto', 'tipo', 'quantidade', 'data']]
    print("\nRelatório de Movimentações de Estoque:")
    print(tabulate(relatorio_movimentacoes, headers='keys', tablefmt='fancy_grid', showindex=False))


# Teste 1: Cadastro de Produto
print("\nTeste 1: Cadastro de Produto")
cadastrar_produto("Tablet", id_categoria=None, quantidade=20, preco=2000.00)
cadastrar_produto("Smartphone", id_categoria=None, quantidade=50, preco=1500.00)
cadastrar_produto("TV", id_categoria=None, quantidade=10, preco=5000.00)

print("\nTeste 1: Tentar cadastrar produto com nome vazio")
cadastrar_produto("", id_categoria=None, quantidade=30, preco=1000.00)

print("\nTeste 1: Cadastro de Produto com Categoria")
cadastrar_categoria("Eletrônicos")
cadastrar_produto("Fone de Ouvido", id_categoria=1, quantidade=25, preco=300.00)


# Teste 2: Adicionar quantidade ao estoque
print("\nTeste 2: Adicionar Quantidade ao Estoque")
adiciona_quantidade_estoque(1, 10)
adiciona_quantidade_estoque(2, 5)
adiciona_quantidade_estoque(999, 20)


# Teste 3: Remover quantidade do estoque
print("\nTeste 3: Remover Quantidade do Estoque")
remove_quantidade_estoque(1, 5)
remove_quantidade_estoque(2, 3)

print("\nTeste 3: Tentar remover mais do que o estoque disponível")
remove_quantidade_estoque(1, 50)

print("\nTeste 3: Tentar remover quantidade de produto inexistente")
remove_quantidade_estoque(999, 10)


# Teste 4: Registrar Movimentação de Estoque
print("\nTeste 4: Registrar Movimentação de Estoque")
registrar_movimentacao(1, "entrada", 10)


# Teste 5: Gerar Relatório de Produtos em Estoque
print("\nTeste 5: Gerar Relatório de Produtos em Estoque")
gerar_relatorio_produtos()


# Teste 6: Gerar Relatório de Movimentações
print("\nTeste 6: Gerar Relatório de Movimentações")
gerar_relatorio_movimentacoes()
