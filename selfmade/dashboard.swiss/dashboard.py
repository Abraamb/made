import streamlit as st
import pandas as pd
import plotly.express as px

# Data voorbeeld
data = {
    'Datum': pd.date_range(start='2022-01-01', periods=100, freq='D'),
    'Klacht': ['Product beschadigd', 'Late levering', 'Verkeerd artikel', 'Product defect'] * 25,
    'Aantal': [1, 3, 2, 5] * 25
}
df = pd.DataFrame(data)

# CSS voor het dashboard
css = """
<style>
    .filter-section {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .data-section {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Sidebar voor filters
st.sidebar.header('Filter Opties')
start_date = st.sidebar.date_input('Start datum', df['Datum'].min())
end_date = st.sidebar.date_input('Eind datum', df['Datum'].max())

filtered_data = df[(df['Datum'] >= pd.Timestamp(start_date)) & (df['Datum'] <= pd.Timestamp(end_date))]

# Hoofdsectie
st.title('Dashboard voor Klachtenanalyse')

# Grafieken aan de linkerkant
st.markdown('<div class="data-section">', unsafe_allow_html=True)
grafiek_type = st.selectbox('Kies het type grafiek', ['Lijngrafiek', 'Staafgrafiek'], index=0)
if grafiek_type == 'Lijngrafiek':
    fig = px.line(filtered_data, x='Datum', y='Aantal', color='Klacht', title='Aantal Klachten over Tijd')
elif grafiek_type == 'Staafgrafiek':
    fig = px.bar(filtered_data, x='Datum', y='Aantal', color='Klacht', title='Aantal Klachten per Datum')
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Recente klachten aan de rechterkant
st.markdown('<div class="data-section">', unsafe_allow_html=True)
st.write('Recente Klachten')
recent_days = st.slider('Aantal dagen terug', 1, 30, 7)
recent_data = df[df['Datum'] >= pd.Timestamp(end_date) - pd.Timedelta(days=recent_days)]
st.dataframe(recent_data)
st.markdown('</div>', unsafe_allow_html=True)
