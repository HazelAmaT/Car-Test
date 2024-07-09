import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats

# Cargar datos

vehicle_df = pd.read_csv('vehicles_us.csv',sep=',',keep_default_na=True)
data_obj = ['model_year','cylinders','is_4wd','date_posted','odometer']
column_missed = ['model_year','cylinders','odometer','paint_color','is_4wd']

def data_to_int(columns):
    for col in columns:
        if col == 'date_posted':
            vehicle_df[col] = pd.to_datetime(vehicle_df[col], format='%d/%m/%Y', errors='coerce')
        else:
            # Llenar NaN con 0 antes de convertir a int para evitar errores
            vehicle_df[col] = vehicle_df[col].fillna(0).astype(int)
    return vehicle_df

# Imprime el DataFrame modificado si deseas ver los cambios
data_to_int(data_obj)

def rename_data (column):
    for col in column:
        vehicle_df[col] = vehicle_df[col].fillna('not specificed')
    return vehicle_df
# Imprime el DataFrame modificado si deseas ver los cambios
rename_data(column_missed)

# Título de la aplicación Streamlit
st.title('Análisis de Precios de Automóviles')

# Función para crear un histograma interactivo
def plot_barchart(df, column,max_cost):
    filtered_df = df[df['price'] <= max_cost]  # Filtra los datos según el valor máximo de precio seleccionado
    fig = px.scatter(filtered_df, x='odometer', y='price', title='Gráfico de Dispersión de Precios de Automóviles')
    fig.update_layout(xaxis_title='Kilometraje', yaxis_title='Precio')
    st.plotly_chart(fig)

# Mostrar una selección de las columnas disponibles
column_to_analyze = st.selectbox("Selecciona una columna", vehicle_df.columns)

# Selección del número de bins para el histograma
max_cost = st.slider('Selecciona el rango de precios', vehicle_df['price'].min(), vehicle_df['price'].max(), value=vehicle_df['price'].max(),step=1)

plot_barchart(vehicle_df, column_to_analyze,max_cost) 


def results_data(df):
    mean_odometer = df['odometer'].mean()
    var_odometer = df['odometer'].var()
    std_odometer = np.sqrt(var_odometer)
    percentage_below_100k = stats.norm.cdf(100000, mean_odometer, std_odometer) * 100
    return percentage_below_100k, mean_odometer, var_odometer   

percentage_below_100k, mean_odometer, var_odometer = results_data(vehicle_df)

start_button =  st.button('Mostrar')
if start_button == True:
        st.write(f'"El {percentage_below_100k}% de los autos tienen kilometraje menor a los 100,000 km"')


def histogram_price(df,condition_labels):
    for condition in condition_labels:
        filtered_df = df[df['condition'] == condition]
        fig = px.histogram(filtered_df, x='price', title=f'Histogram for {condition} condition')
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)
    

unique_types = set(vehicle_df['condition'].unique())
condition_labels = list(unique_types)

histogram_price(vehicle_df, condition_labels)
