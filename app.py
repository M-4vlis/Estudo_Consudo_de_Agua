# === IMPORTAÇÕES ===
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale

# === CONFIGURAÇÕES ===
locale.setlocale(locale.LC_ALL, '')
st.set_page_config(page_title="Dashboard Consumo de Água", layout="wide")

# === CARREGAMENTO DE DADOS ===
@st.cache_data
def load_data():
    df = pd.read_excel("consolidado_agua.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    df['medição'] = pd.to_datetime(df['medição'], errors='coerce')
    df['ano'] = df['medição'].dt.year.astype(str)
    df['mês'] = df['medição'].dt.month
    df['volume medido (m³)'] = pd.to_numeric(df['volume medido (m³)'], errors='coerce')
    df['volume faturado (m³)'] = pd.to_numeric(df['volume faturado (m³)'], errors='coerce')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    return df

df = load_data()

# === ORDENAÇÃO DE MESES ===
nomes_meses = {
    '1': 'Jan', '2': 'Fev', '3': 'Mar', '4': 'Abr',
    '5': 'Mai', '6': 'Jun', '7': 'Jul', '8': 'Ago',
    '9': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
}
ordem_meses = list(nomes_meses.values())

df['nome_mês'] = df['mês'].map(lambda x: nomes_meses.get(str(x)))
df['nome_mês'] = pd.Categorical(df['nome_mês'], categories=ordem_meses, ordered=True)

# === ESTIMATIVAS 2025 ===
df_filtrado = df[df['ano'] < '2025']
estimativa_consumo = df_filtrado.groupby('ano')['volume medido (m³)'].sum().mean()
estimativa_valor = df_filtrado.groupby('ano')['valor'].sum().mean()

# === LAYOUT DE TELAS ===
col1, col2 = st.columns([1, 4])

# === COLUNA 1: LATERAL COM RESUMO ===
with col1:
    st.markdown("<h2 style='text-align: left; color: #ffffff;'> Consumo de Água</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: #ffffff;'> Estimativa 2025</h3>", unsafe_allow_html=True)
    
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=estimativa_consumo,
        title={'text': "Consumo Estimado 2025"},
        gauge={
            'axis': {'range': [0, 50000]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 20000], 'color': "lightgray"},
                {'range': [20000, 40000], 'color': "gray"},
                {'range': [40000, 50000], 'color': "darkblue"},
            ]
        }
    ))
    st.plotly_chart(gauge, use_container_width=True)
    st.metric("Valor Estimado 2025", f"R$ {locale.format_string('%.2f',estimativa_valor, grouping=True)}")

    # Tendência de consumo e valor por ano
    consumo_por_ano = df.groupby("ano")["volume medido (m³)"].sum().reset_index()
    valor_por_ano = df.groupby("ano")["valor"].sum().reset_index()

    fig_consumo = px.line(consumo_por_ano, x="ano", y="volume medido (m³)", title="Consumo por Ano", markers=True)
    fig_valor = px.line(valor_por_ano, x="ano", y="valor", title="Valor por Ano", markers=True)
    
    st.plotly_chart(fig_consumo, use_container_width=True)
    st.plotly_chart(fig_valor, use_container_width=True)

# === COLUNA 2: DASHBOARD PRINCIPAL ===
with col2:
    st.markdown("## 📊 Comparativo Anual")

    # SELETOR DE ANO
    anos = sorted(df['ano'].unique())
    ano_sel = st.selectbox("Selecione o Ano", anos)

    df_ano = df[df['ano'] == ano_sel]

    # === MÉTRICAS DO ANO SELECIONADO ===
    vol1 = df_ano['volume medido (m³)'].sum()
    vol2 = df_ano['volume faturado (m³)'].sum()
    val1 = df_ano['valor'].sum()

    col1m, col2m, col3m = st.columns(3)
    col1m.metric("🔵 Volume Medido ano selecionado", f"{locale.format_string('%.0f', vol1, grouping=True)} m³")
    col2m.metric(
    "🟢 Volume Faturado ano selecionado",
    f"{locale.format_string('%d', vol2, grouping=True)} m³",
    delta=f"{locale.format_string('%.2f', ((vol2 - vol1) / vol1) * 100)}%")

    col3m.metric("💰 Valor Total ano selecionado", f"R$ {locale.format_string('%.2f', val1, grouping=True)}")

    # === GRÁFICO: Valor Mensal ===
    mensal_valor = df_ano.groupby('nome_mês')['valor'].sum().reindex(ordem_meses)
    fig_valor_mensal = px.bar(
        x=mensal_valor.index, y=mensal_valor.values,
        labels={'x': 'Mês', 'y': 'Valor (R$)'},
        color=mensal_valor.values
    )
    st.subheader(f"Valor Mensal - {ano_sel}")
    st.plotly_chart(fig_valor_mensal, use_container_width=True)

    # === GRÁFICO: Medido vs Faturado ===
    comparativo = df_ano.groupby('nome_mês')[['volume medido (m³)', 'volume faturado (m³)']].sum().reset_index()
    comparativo = comparativo.sort_values('nome_mês')

    fig_comp = go.Figure()
    for tipo, cor in zip(['volume medido (m³)', 'volume faturado (m³)'], ['#55ff14', '#ff2400']):
        fig_comp.add_trace(go.Bar(
            x=comparativo['nome_mês'],
            y=comparativo[tipo],
            name=tipo,
            marker_color=cor,
            text=comparativo[tipo],
            textposition='outside'
        ))
    fig_comp.update_layout(
        barmode='group',
        title=f'Volume Medido vs Faturado - {ano_sel}',
        xaxis_title='Mês',
        yaxis_title='',
        showlegend=True,
        uniformtext_minsize=8,
        uniformtext_mode='show',
        margin=dict(t=80),  # aumenta o topo (t = top)
    )
    st.subheader("Volume Medido vs Faturado")
    st.plotly_chart(fig_comp, use_container_width=True)

    # === GRÁFICO: Comparativo Valor 2023 x 2024 ===
    df_agrupado = df[df['ano'].isin(['2020','2021','2022','2023','2024'])].groupby(['ano', 'nome_mês'])['valor'].sum().reset_index()
    df_agrupado['nome_mês'] = pd.Categorical(df_agrupado['nome_mês'], categories=ordem_meses, ordered=True)
    df_agrupado = df_agrupado.sort_values(['ano', 'nome_mês'])

    fig_valores_comparativo = go.Figure()
    for ano in df_agrupado['ano'].unique():
        dados = df_agrupado[df_agrupado['ano'] == ano]
        fig_valores_comparativo.add_trace(go.Bar(
            x=dados['nome_mês'],
            y=dados['valor'],
            name=ano,
            textposition='outside'
        ))

    fig_valores_comparativo.update_layout(
        barmode='group',
        title="Valor Total por Mês - 2020 à 2024",
        xaxis_title="Mês",
        yaxis_title="",
        showlegend=True
    )
    st.subheader("Comparativo de Valor Total")
    st.plotly_chart(fig_valores_comparativo, use_container_width=True)

    # === TABELA EXPANDÍVEL ===
    with st.expander("📋 Ver dados em tabela"):
        st.dataframe(df, use_container_width=True)