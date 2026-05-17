import streamlit as st
import pandas as pd
import clickhouse_connect
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

st.set_page_config(page_title="Northwind Sales Dashboard", layout="wide")

def get_client():
    return clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT")),
        username=os.getenv("CLICKHOUSE_USER"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
        database=os.getenv("CLICKHOUSE_DB")
    )

st.title("📊 Northwind Strategic Dashboard")
st.markdown("KPIs de Vendas baseados na arquitetura Medallion (Bronze -> Silver -> Gold)")

try:
    client = get_client()
    
    # Query Gold Layer
    df = client.query_df("SELECT * FROM fct_sales")

    # KPIs superiores
    total_sales = df['order_total_value'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"$ {total_sales:,.2f}")
    col2.metric("Total de Pedidos", f"{total_orders}")
    col3.metric("Ticket Médio", f"$ {avg_order_value:,.2f}")

    # Gráficos
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Vendas por País")
        fig_country = px.pie(df, values='order_total_value', names='ship_country', hole=.3)
        st.plotly_chart(fig_country, use_container_width=True)

    with c2:
        st.subheader("Evolução de Vendas (Mensal)")
        df['month'] = pd.to_datetime(df['order_date']).dt.to_period('M').astype(str)
        monthly_sales = df.groupby('month')['order_total_value'].sum().reset_index()
        fig_trend = px.line(monthly_sales, x='month', y='order_total_value', markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Detalhes dos Pedidos")
    st.dataframe(df.sort_values('order_date', ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao conectar ou buscar dados: {e}")
    st.info("Certifique-se de que o dbt run foi executado com sucesso.")
