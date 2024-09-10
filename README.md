# RFM Pyramid Score - Análise de Clientes com Segmentação e Predição de Churn

© 2024 Renato Menendes. Todos os direitos reservados sob a Licença MIT.

## Descrição

**RFM Pyramid Score** é um pacote para realizar análises avançadas de clientes, incluindo **segmentação RFM (Recência, Frequência e Valor Monetário)**, **elasticidade de preços**, **previsão de churn (cancelamento)** e **corredor de preços**, além de calcular o comportamento de grupos comparáveis ou segmentos de mercado.

## Funcionalidades

- **Análise de RFM e Pyramid Score**: Classificação dos clientes em diferentes segmentos com base em seu valor e comportamento transacional.
- **Elasticidade de Preço**: Cálculo da sensibilidade dos clientes às mudanças de preço com base no histórico de compras.
- **Corredor de Preços**:
  - **Cliente**: Identificação do menor e maior preço pago por um cliente específico.
  - **Grupo Comparável**: Identificação dos limites de preço para grupos de clientes comparáveis, removendo outliers.
- **Previsão de Churn**:
  - Utiliza modelos preditivos para calcular a probabilidade de um cliente cancelar ou se tornar inativo.
  - Identificação de indícios de churn, como quedas na frequência de compra ou valores gastos.

### Ambiente

Este pacote foi desenvolvido com **Python 3.10**.

#### Criando o ambiente virtual

Crie um novo ambiente para rodar o projeto:

```bash
conda create -n rfm_pyramid_score -y python=3.10
```

Para ativar o ambiente, use:
```bash
conda activate rfm_pyramid_score
```

### Instalação das dependências

Para instalar as dependências, execute o seguinte comando dentro do ambiente virtual:

```bash
python -m pip install -r "requirements.txt"
```

## Estrutura do Projeto
```
rfm_pyramid_score/
│
├── rfm_pyramid_score/                # Pacote principal do projeto
│   ├── __init__.py                   # Inicializa os módulos do pacote
│   ├── rfm_pyramid_score.py          # Análise de RFM e Pyramid Score
│   ├── price_elasticity.py           # Cálculo da elasticidade-preço
│   ├── price_corridor.py             # Cálculo do corredor de preços do cliente
│   ├── group_price_corridor.py       # Cálculo do corredor de preços por segmento
│   ├── churn_prediction.py           # Módulo para a previsão de churn
│
├── tests/                            # Testes automatizados
│   ├── test_analysis.py              # Testes para o módulo de análise
│   ├── test_price_elasticity.py      # Testes para elasticidade-preço
│   ├── test_price_corridor.py        # Testes para corredor de preços
│   ├── test_group_price_corridor.py  # Testes para corredor de preços por segmento
│   ├── test_churn_prediction.py      # Testes para o módulo de previsão de churn
│
├── LICENSE                           # Licença do projeto
├── README.md                         # Documentação do projeto
├── setup.py                          # Arquivo de configuração do pacote
├── requirements.txt                  # Dependências do projeto
```

## Rodando Tasks

### Rodando a aplicação

Para usar os módulos de análise, basta importar as classes e executar o código de acordo com suas necessidades. Exemplo:

```python
from rfm_pyramid_score import PyramidScoreAnalysis

# Suponha que já tenhamos um DataFrame com dados de transações
df = ...

# Análise de Pyramid Score
analysis = PyramidScoreAnalysis(df, 'customer_id', 'transaction_date', 'amount')
print(analysis.segment_table)
```

### Rodando testes

Para rodar os testes automatizados, use o seguinte comando:

```bash
python -m unittest discover tests
```

## Exemplo de Uso

Após ativar o ambiente e instalar as dependências, você pode rodar a análise de RFM e calcular a elasticidade de preço, prever o churn ou calcular o corredor de preços para um cliente ou segmento.

Exemplo de cálculo da elasticidade-preço:

```python
from rfm_pyramid_score import PriceElasticity

# Suponha que temos um DataFrame com preços e quantidades
df = ...

elasticity_calc = PriceElasticity(df, 'customer_id', 'price', 'quantity')
elasticity = elasticity_calc.calculate_elasticity('A')
print(elasticity)
```

## Licença

Este projeto é licenciado sob a Licença MIT. Isso significa que você é livre para usar, modificar e distribuir este software, desde que mantenha o aviso de copyright original e a permissão da licença. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

© 2024 Renato Menendes. Todos os direitos reservados sob a Licença MIT.
