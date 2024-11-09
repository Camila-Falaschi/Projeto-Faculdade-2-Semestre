# Sistema de Gerenciamento de Estoque
Este projeto implementa um sistema simples de gerenciamento de estoque, permitindo o cadastro de produtos, movimentações de entrada e saída e geração de relatórios.

## Funcionalidades
- Cadastro de produtos e categorias
- Adição e remoção de quantidades de produtos no estoque
- Registro de movimentações de entrada e saída
- Geração de relatórios de produtos e movimentações

## Tecnologias
- Python
- Pandas
- Tabulate

## Exemplo de uso
```python
# Cadastro de produto
cadastrar_produto("Tablet", id_categoria=None, quantidade=20, preco=2000.00)

# Adicionar quantidade ao estoque
adiciona_quantidade_estoque(1, 10)

# Remover quantidade do estoque
remove_quantidade_estoque(1, 5)

# Gerar relatório de produtos
gerar_relatorio_produtos()

# Gerar relatório de movimentações
gerar_relatorio_movimentacoes()
```
