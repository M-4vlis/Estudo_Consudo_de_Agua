# 💧 Consumo de Água: Análise Comparativa Anual

Dashboard interativo para análise comparativa de consumo de água e volume faturado entre os anos de 2023 e 2024. O projeto visa facilitar o acompanhamento de dados operacionais, evidenciar discrepâncias entre volume medido e faturado, e promover insights que subsidiem ações de controle, economia e sustentabilidade.

## Visão Geral

O sistema apresenta:

- Comparativo mensal do consumo de água entre dois anos consecutivos
- Diferença percentual entre volume medido e volume faturado
- Comparativo de valores pagos
- Análise gráfica com visualização clara e objetiva
- Insights estratégicos extraídos automaticamente dos dados

> A aplicação foi desenvolvida com foco em visualização simples, objetiva e amigável para gestores operacionais e analistas de infraestrutura predial.

## Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** – Interface interativa e responsiva
- **Pandas** – Manipulação e análise de dados
- **Plotly** – Gráficos dinâmicos e interativos
- **GitHub Pages** – Hospedagem do código-fonte

## Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/M-4vlis/Estudo_Consudo_de_Agua.git
cd Estudo_Consudo_de_Agua
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
streamlit run app.py
```

## Deploy com Streamlit Cloud

1. Suba seu projeto completo no GitHub.
2. Acesse: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecte sua conta do GitHub e selecione o repositório.
4. Configure o arquivo principal como `app.py`.
5. Clique em "Deploy" e aguarde o carregamento da aplicação.

> O link gerado poderá ser compartilhado com qualquer pessoa para visualização do dashboard em tempo real.

## Prints da Aplicação (opcional)

Adicione capturas de tela do dashboard aqui para demonstrar a interface visual.

## Contribuição

Sinta-se à vontade para abrir *issues*, sugerir melhorias ou criar *pull requests*. Toda colaboração é bem-vinda!

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
