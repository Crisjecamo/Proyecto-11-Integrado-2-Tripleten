#!/usr/bin/env python
# coding: utf-8

# # Contenido
# 
# * [Diccionario de los Datos](#diccionario)
# * [Introduccion](#introduccion)
# * [Preparamos los datos para el análisis](#dataframe)
#     * [Observacion](#observacion)
# * [Estudiar y comprobar los datos](#ecd)
#   * [¿Cuántos eventos hay en los registros?](#cehr)
#   * [¿Cuántos usuarios y usuarias hay en los registros?](#cuuhr)
#   * [¿Cuál es el promedio de eventos por usuario?](#cpeu)
#     * [Observacion](#observacion1)
#   * [¿Qué periodo de tiempo cubren los datos?](#qptcd)
#     * [Observacion](#observacion2)
#   * [¿Perdimos muchos eventos y usuarios al excluir los datos más antiguos?](#pmeueda)
#     * [Observacion](#observacion3)
#   * [Nos Asegúramos de tener usuarios y usuarias de los tres grupos experimentales](#natuutge)
#     * [Observacion](#observacion4)
# * [Estudiar el embudo de eventos](#eee)
#   * [Observamos qué eventos hay en los registros y su frecuencia de suceso](#oehrfs)
#     * [Observacion](#observacion5)
#   * [Encontramos la cantidad de usuarios y usuarias que realizaron cada una de estas acciones. Ordenamos los eventos por el número de usuarios y usuarias. Calculamos la proporción de usuarios y usuarias que realizaron la acción al menos una vez.](#ecuurcea)
#     * [Observacion](#observacion6)
#   * [¿En qué orden ocurrieron las acciones? ¿Todas son parte de una sola secuencia?](#ooa)
#     * [Observacion](#observacion7)
#   * [Utilizamos el embudo de eventos para encontrar la proporción de usuarios y usuarias que pasan de una etapa a la siguiente](#ueepepuupes)
#     * [Secuencia que empieza por Tutorial](#set)
#     * [Secuencia que empieza por MainScreenAppear](#sem)
#   * [¿En qué etapa pierdes más usuarios y usuarias?](#epuu)
#     * [Observacion](#observacion8)
#   * [¿Qué porcentaje de usuarios y usuarias hace todo el viaje desde su primer evento hasta el pago?](#puuhtvdpehp)
#     * [¿Cuántos usuarios y usuarias hay en cada grupo?](#cuucg)
#       * [Observacion](#observacion9)
# * [Estudiamos los resultados del experimento](#ere)
#   * [Observamos si hay una diferencia estadísticamente significativa entre las muestras 246 y 247](#tgctdcnmc)
#     * [Observacion](#observacion10)
#   * [Seleccionamos el evento más popular. En cada uno de los grupos de control, encontramos la cantidad de usuarios y usuarias que realizaron esta acción. Encontramos su proporción. Comprobamos si la diferencia entre los grupos es estadísticamente significativa](#sep)
#     * [Observacion](#observacion11)
#   * [Comprobamos si la diferencia entre las proporciones de un evento en dos grupos es estadísticamente significativa.](#cdepeges)
#     * [Observacion](#observacion12)
#   * [Realizamos lo mismo para el grupo con fuentes alteradas (248). Comparamos los resultados con los de cada uno de los grupos de control (246 y 247) para cada evento de forma aislada. Comparamos los resultados con los resultados combinados de los grupos de control](#rmpgfa)
#     * [Observacion](#observacion13)
#   * [Observamos si hay una diferencia estadísticamente significativa entre las muestras 246 y 248.](#odesem)
#   * [Observamos si hay una diferencia estadísticamente significativa entre las muestras 247 y 248.](#odesem78)
#   * [Comparamos los eventos del grupo 246 con el grupo 248](#cegg)
#     * [Observacion](#observacion14)
#   * [Comparamos los eventos del grupo 247 con el grupo 248](#cegg78)
#     * [Observacion](#observacion15)
#   [Comparamos los resultados con los resultados combinados de los grupos de control](#crrcgc)
#     * [Observacion](#observacion16)
#   * [Observamos si hay una diferencia estadísticamente significativa entre las muestras control y 248](#odesemc)
#     * [Observacion](#observacion17)
#   * [Comparamos los eventos para los grupos control con el grupo 248](#cepgcg)
#     * [Observacion](#observacion18)
# * [Conclusion General](#conclusion)
# * [Recomendaciones](#recomendaciones)

# # Diccionario de los datos <a id='diccionario'></a>
# Cada entrada de registro es una acción de usuario o un evento.
# 
# logs_exp_us.csv
# 
# * EventName: nombre del evento.
# 
# * DeviceIDHash: identificador de usuario unívoco.
# 
# * EventTimestamp: hora del evento.
# 
# * ExpId: número de experimento: 246 y 247 son los grupos de control, 248 es el grupo de prueba.

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# El diccionario de datos está claro y bien presentado. Has descrito adecuadamente cada columna, lo que facilita la comprensión del conjunto de datos.</div>
# 

# # Introduccion <a id='introduccion'></a>
# 
# Este proyecto tiene como objetivo analizar un conjunto de datos de registros de eventos de usuarios para una aplicación móvil. El análisis se centra en comprender el comportamiento del usuario, identificar patrones en la secuencia de eventos y evaluar el impacto de un experimento A/B testing.
# 
# El conjunto de datos contiene información sobre diferentes eventos, como la visualización de la pantalla principal, la visualización de ofertas, la interacción con el carrito de compras y la finalización exitosa del pago. Se estudiará el embudo de eventos para determinar las etapas en las que se pierden más usuarios y la proporción de usuarios que completan el recorrido completo hasta el pago.
# 
# Además, se evaluará el experimento A/B testing para determinar si las modificaciones introducidas en un grupo de prueba tuvieron un impacto significativo en el comportamiento del usuario en comparación con los grupos de control. Se utilizarán pruebas estadísticas para determinar si las diferencias observadas son estadísticamente significativas.
# 
# El análisis proporcionará información valiosa sobre el comportamiento del usuario, las áreas de mejora en la aplicación y la efectividad de las modificaciones introducidas en el experimento. Los resultados ayudarán a optimizar la aplicación para mejorar la experiencia del usuario y aumentar las conversiones.

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# La introducción está bien planteada, explicando claramente el propósito del análisis y el enfoque en el comportamiento de usuario y pruebas A/B. Ofreces una descripción clara de las etapas del embudo y del objetivo del experimento A/B.</div>
# 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly import graph_objects as go
import seaborn as sns
from scipy import stats as st
import math as mth
import numpy as np


# # Preparamos los datos para el análisis <a id='dataframe'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> La preparación de los datos está bien ejecutada. Renombraste las columnas para mayor claridad, verificaste la presencia de datos nulos y duplicados, y eliminaste correctamente los duplicados con `drop_duplicates()`. Además, el uso de `pd.to_datetime()` para trabajar con fechas es apropiado. </div>

# In[2]:


#Leemos el dataset
df = pd.read_csv('/datasets/logs_exp_us.csv', sep='\t')
df.head()


# In[3]:


#Cambiamos el nombre de las columnas
new_columns ={
    'EventName': 'event_name',
    'DeviceIDHash': 'user_id',
    'EventTimestamp': 'event_timestamp',
    'ExpId': 'exp_id',
}
df.rename(columns = new_columns, inplace = True)
print(df.columns)


# In[4]:


# Utilice unit='s' para convertir desde marcas de tiempo de Unix
#Creamos la columna con las fechas y horas
df['event_datetime'] = pd.to_datetime(df['event_timestamp'], unit='s')

#Creamos una columna que contenga solo las fechas
df['event_date'] = pd.to_datetime(df['event_datetime'].dt.date)
df.head()


# In[5]:


#Utilizamos el metodo info para tener una vision general
df.info()


# In[6]:


#Verificamos si tenemos datos ausentes
df.isna().sum()


# In[7]:


#Verificamos si tenemos datos Duplicados
df.duplicated().sum()


# In[8]:


#Verificamos cuales son los datos duplicados podemos ver que los datos con indice 452 y 453 son identicos
df[df['user_id']== 5613408041324010552].head()


# ### Observacion: <a id='observacion'></a>
# 
# Si visualizamos los indice 452 y 453 podremos notar que son registros totalmente identicos que se pudieron haber geenerado por algun error al momento del registro, por ende procederemos a eliminar los datos duplicados.

# In[9]:


#Eliminamos los datos duplicados y verificamos si fueron eliminados
df= df.drop_duplicates()
df.duplicated().sum()


# # Estudiar y comprobar los datos <a id='ecd'></a>

# ## ¿Cuántos eventos hay en los registros? <a id='cehr'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> Utilizaste correctamente `value_counts()` para contar los eventos, mostrando que "MainScreenAppear" es el evento más frecuente con 119,101 ocurrencias. Los eventos están bien ordenados por frecuencia. </div>

# In[10]:


#Verificamos el total de eventos registrados en nuestros datos
events= df['event_name'].value_counts().reset_index()
events


# ## ¿Cuántos usuarios y usuarias hay en los registros? <a id='cuuhr'></a>

# In[11]:


#Verificamos cuantos usuarios unicos tenemos en nuestros registros
unique_users= df['user_id'].nunique()
print(f'Cantidad de usuarios unicos registrados: {unique_users}')


# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> El cálculo del número de usuarios únicos es adecuado utilizando `nunique()`. Los resultados son claros y bien explicados, mostrando que tienes 7551 usuarios únicos. </div>

# ## ¿Cuál es el promedio de eventos por usuario? <a id='cpeu'></a>

# In[12]:


#Calculamos la media y mediana de eventos por usuario
print(f'Promedio de eventos por usuario: {round(df.groupby("user_id")["event_name"].count().mean())}')
print(f'Mediana de eventos por usuario: {round(df.groupby("user_id")["event_name"].count().median())}')


# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> El cálculo de la media y la mediana de eventos por usuario está bien hecho. Es útil que incluyas ambos valores (32 y 20) para mostrar la distribución de los eventos por usuario. </div>

# ### Observacion: <a id='cbservacion1'></a>
# 
# El promedio de eventos por usuarios es de 32 y la mediana es 20 eventos.

# ## ¿Qué periodo de tiempo cubren los datos? Encuentraremos la fecha máxima y mínima. Trazaremos un histograma por fecha y hora. ¿Podemos tener seguridad de que tenemos datos igualmente completos para todo el periodo? Los eventos más antiguos podrían terminar en los registros de algunos usuarios o usuarias por razones técnicas, esto podría sesgar el panorama general. Encontramos el momento en el que los datos comienzan a estar completos e ignoramos la sección anterior. ¿Qué periodo representan realmente los datos? <a id='qptcd'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> Identificaste correctamente las fechas mínima y máxima de los datos. La creación del histograma es una excelente elección visual para analizar la distribución de eventos a lo largo del tiempo. </div>

# In[13]:


#Trazamos un histograma por fecha y hora.
print(f"Fecha mínima: {df['event_datetime'].min()}")
print(f"Fecha máxima: {df['event_datetime'].max()}")

# Trazar un histograma por fecha y hora
plt.figure(figsize=(14, 10))

sns.histplot(data= df, x='event_datetime')

# Configurar las propiedades del eje x
plt.xticks(rotation=45, ha='right')  # se ajusta la inclinación y alineación de las etiquetas
plt.xlabel('Fecha y Hora')  # se etablece el título del eje x

plt.show()


# ### Observacion: <a id='observacion2'></a>
# 
# La fecha minima es 25 de julio de 2019 y la fecha maxima es 7 de agosto de 2019.
# 
# Nuestros datos indican que a partir del 31 de julio de 2019 se observa un aumento significativo en la cantidad de registros realizados.

# ## ¿Perdimos muchos eventos y usuarios al excluir los datos más antiguos? <a id='pmeueda'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> Excluiste correctamente los eventos anteriores al 31 de julio de 2019 y verificaste que solo el 0.33% de los datos fueron descartados. El razonamiento detrás de esta exclusión es sólido. </div>

# In[14]:


#Verificamos que cantidad de datos representan los que vamos a excluir y su porcentaje
#Filtramos los datos para excluir los registros menores a '2019-07-31'

filtered_old_data = df[df['event_datetime'] < '2019-07-31'].shape[0]
print(f"Número de eventos excluidos que vamos a excluir: {filtered_old_data}\n\n",
      f"Porcentaje de los datos a excluir: {round((796/243713)*100, 2)}%")
print()
df= df[df['event_datetime'] >= '2019-07-31']
df.info()


# ### Observacion: <a id='observacion3'></a>
# 
# excluimos 796 registros lo que representan un 0,33% de los datos y solo los quedamos con los datos mayores o iguales a la fecha de 31 de julio de 2019.

# ## Nos Asegúramos de tener usuarios y usuarias de los tres grupos experimentales. <a id='natuutge'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> Verificaste correctamente la distribución de usuarios entre los grupos experimentales utilizando `groupby()` y `nunique()`. Las proporciones similares entre los grupos son un buen indicador de equilibrio. </div>

# In[15]:


#Verificamos la cantidad de usuarios en los 3 grupos
df.groupby('exp_id')['user_id'].nunique().reset_index()


# ### Observacion: <a id='observacion4'></a>
# 
# * En el Grupo 246 tenemos 2485 usuarios unicos registrados
# 
# * En el grupo 247 tenemos 2517 usuarios unicos registrados
# 
# * En el grupo 248 tenemos 2540 usuarios unicos registrados
# 
# A simple vista podemos ver que tenemos una proporcion de usuarios muy parecida entre los 3 grupos.

# # Estudiar el embudo de eventos <a id='eee'></a>

# ## Observamos qué eventos hay en los registros y su frecuencia de suceso. <a id='oehrfs'></a>

# <div class="alert alert-block alert-success"> <b>Éxito</b> <a class="tocSkip"></a> Has mostrado que "MainScreenAppear" es el evento más frecuente, seguido de "OffersScreenAppear", "CartScreenAppear", "PaymentScreenSuccessful" y "Tutorial". La presentación de estos resultados es clara y precisa. </div>

# In[16]:


events_count= df['event_name'].value_counts().reset_index()
print(events_count)
fig = px.bar(events_count, x="index", y='event_name', labels={'index':'Evento', 'event_name':'Frecuencia'})
fig.show()


# ## Observacion: <a id='observacion5'></a>
# 
# El evento más frecuente en nuestro gráfico es 'MainScreenAppear' con 118,578 registros, seguido de 'OffersScreenAppear' (46,707), 'CartScreenAppear' (42,560), 'PaymentScreenSuccessful' (34,058) y finalmente 'tutorial' (1,014).

# ## Encontramos la cantidad de usuarios y usuarias que realizaron cada una de estas acciones. Ordenamos los eventos por el número de usuarios y usuarias. Calculamos la proporción de usuarios y usuarias que realizaron la acción al menos una vez. <a id='ecuurcea'></a>

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# El análisis de cuántos usuarios realizaron cada acción es preciso. Has utilizado correctamente `groupby()` para agrupar los datos y calcular la cantidad de usuarios por evento.</div>
# 

# In[17]:


#Agrupamos los datos para obtener los usuarios unicos que realizaron cada uno de los eventos
users_unic= df.groupby('event_name')['user_id'].nunique().reset_index().sort_values(by='user_id', ascending=False)
users_unic


# In[18]:


fig = go.Figure(go.Funnel(
    y = users_unic['event_name'],
    x = users_unic['user_id'],
    textposition = "inside",
    textinfo = "value+percent initial",
    opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )

fig.update_layout(title_text='Cantidad de usuarios y usuarias que realizaron cada una de estas acciones') # Set the title for the figure
fig.show()


# In[19]:


# Calcula la proporción de usuarios que realizaron cada acción al menos una vez
total_users = df['user_id'].nunique()
users_per_event = df.groupby('event_name')['user_id'].nunique()
proportion_users_per_event = (users_per_event / total_users) * 100

# Ordena los eventos por la proporción de usuarios que los realizaron
proportion_users_per_event = proportion_users_per_event.sort_values(ascending=False)

print(f"Proporción de usuarios que realizaron cada acción al menos una vez:\n\n {proportion_users_per_event}")


# ### Observacion: <a id='observacion6'></a>
# 
# Podemos observar en nuestro grafico que la cantidad de usuarios unicos en cada etapa del embudo va disminuyendo. De los 7429 usuarios que han visitado la pagina solo 3542 Realizaron una compra lo que equivale a un 48% del total inicial.
# 
# Con estos datos de proporciones podemos confirmar lo que nos muestra nuestro embudo

# ## ¿En qué orden ocurrieron las acciones? ¿Todas son parte de una sola secuencia? <a id='ooa'></a>

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# El uso de tablas pivote para analizar el orden de las acciones es una buena elección. Has identificado secuencias claras de eventos, lo cual es clave para entender el flujo de comportamiento de los usuarios.</div>
# 

# In[20]:


# buscamos la hora del primer suceso de cada evento. Usaremos el método pivot_table()

users = df.pivot_table(
    index='user_id',
    columns='event_name',
    values='event_datetime',
    aggfunc='min')

users.head()


# ### Observacion: <a id='observacion7'></a>
# 
# Con el estudio de nuestra tabla pivot notamos 2 secuencias una  que viene de clientes que entran directamente a la pagina principal, ven la oferta, agregan productos a sus carritos y realizan la compra.
# 
# otra de clientes que primero ven el tutorial, luego entran a la pagina principal, ven la oferta, agregan productos a sus carritos y compran

# ## Utilizamos el embudo de eventos para encontrar la proporción de usuarios y usuarias que pasan de una etapa a la siguiente. (Por ejemplo, para la secuencia de eventos A → B → C, calculamos la proporción de usuarios en la etapa B a la cantidad de usuarios en la etapa A y la proporción de usuarios en la etapa C a la cantidad en la etapa B) <a id='ueepepuupes'></a>

# ## Secuencia que empieza por Tutorial <a id='set'></a>

# In[21]:


#Enbudo de usuarios que primero vieron el tutorial
step_1 = ~users['Tutorial'].isna()
step_2 = step_1 & (users['MainScreenAppear'] > users['Tutorial'])
step_3 = step_2 & (users['OffersScreenAppear'] > users['MainScreenAppear'])
step_4 = step_3 & (users['CartScreenAppear'] > users['OffersScreenAppear'])
step_5 = step_4 & (users['PaymentScreenSuccessful'] > users['CartScreenAppear'])

c_tutorial = users[step_1].shape[0]
c_mainscreen = users[step_2].shape[0]
c_offers = users[step_3].shape[0]
c_cart = users[step_4].shape[0]
c_payment = users[step_5].shape[0]

print('Vieron el Tutorial:', c_tutorial, 'Proporcion: ', round((c_tutorial/c_tutorial) * 100, 2), '%')
print('Visitaron la Pagina:', c_mainscreen, 'Proporcion: ', round((c_mainscreen/c_tutorial) * 100, 2), '%')
print('Vieron la Oferta:', c_offers, 'Proporcion: ', round((c_offers/c_mainscreen) * 100, 2), '%')
print('Agregaron Productos a su Carrito:', c_cart, 'Proporcion: ', round((c_cart/c_offers) * 100, 2), '%')
print('Pagaron:', c_payment, 'Proporcion: ', round((c_payment/c_cart) * 100, 2), '%')



# In[22]:


fig = go.Figure(go.Funnel(
    y = [ "Vieron el Tutorial", "Visitaron la Pagina", "Vieron la Oferta", "Agregaron Productos a su Carrito",
         "Pagaron"],
    x = [845, 793, 628, 352, 217],
    textposition = "inside",
    textinfo = "value+percent initial",
    opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )

fig.update_layout(title_text='La proporción de usuarios y usuarias que pasan de una etapa a la siguiente empezando por Tutorial') # Set the title for the figure
fig.show()


# ## Secuencia que empieza por MainScreenAppear <a id='sem'></a>

# In[23]:


#Embudo de usuarios que entraron directo a la pagina web

step_1 = ~users['MainScreenAppear'].isna()
step_2 = step_1 & (users['OffersScreenAppear'] > users['MainScreenAppear'])
step_3 = step_2 & (users['CartScreenAppear'] > users['OffersScreenAppear'])
step_4 = step_3 & (users['PaymentScreenSuccessful'] > users['CartScreenAppear'])
step_5 = step_4 & (users['Tutorial'] > users['PaymentScreenSuccessful'])

n_mainscreen = users[step_1].shape[0]
n_offers = users[step_2].shape[0]
n_cart = users[step_3].shape[0]
n_payment = users[step_4].shape[0]
n_tutorial = users[step_5].shape[0]

print('Visitaron la Pagina:', n_mainscreen, 'Proporcion: ', round((n_mainscreen/n_mainscreen) * 100, 2), '%')
print('Vieron la Oferta:', n_offers, 'Proporcion: ', round((n_offers/n_mainscreen) * 100, 2),'%')
print('Agregaron Productos a su Carrito:', n_cart, 'Proporcion: ', round((n_cart/n_offers) * 100, 2), '%')
print('Pagaron:', n_payment, 'Proporcion: ', round((n_payment/n_cart) * 100, 2), '%')
print('Vieron el Tutorial:', n_tutorial, 'Proporcion: ', round((n_tutorial/n_payment) * 100, 2), '%')


# In[24]:


fig = go.Figure(go.Funnel(
    y = ["Visitaron la Pagina", "Vieron la Oferta", "Agregaron Productos a su Carrito",
         "Pagaron", "Vieron el Tutorial",],
    x = [7429 , 4116, 1672 , 453, 1],
    textposition = "inside",
    textinfo = "value+percent initial",
    opacity = 0.65, marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )

fig.update_layout(title_text='La proporción de usuarios y usuarias que pasan de una etapa a la siguiente empezando por MainScreenAppear') # Set the title for the figure
fig.show()


# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# Buen trabajo en calcular las proporciones de usuarios que completan cada etapa del embudo, tanto para la secuencia que comienza con Tutorial como con MainScreenAppear. Las visualizaciones en forma de embudo son excelentes para comunicar los hallazgos.</div>
# 

# ## ¿En qué etapa pierdes más usuarios y usuarias? <a id='epuu'></a>

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# Identificaste correctamente las etapas donde se pierden más usuarios. Este análisis es crucial para tomar decisiones en cuanto a mejoras en la aplicación.</div>
# 

# ### Observacion: <a id='observacion8'></a>
# 
# Etapa con mayor pérdida de usuarios en el embudo que empieza por MainScreenAppear:
# Entre 'Vieron la Oferta' y 'Pagaron'
# 
# Etapa con mayor pérdida de usuarios en el embudo que empieza por Tutorial:
# Entre 'Vieron la Oferta' y 'Pagaron'
# 
# En ambos embudos se observa una significativa pérdida de clientes al momento de agregar productos al carrito, sin concretar la compra. Este fenómeno es particularmente evidente en el embudo de los usuarios que ingresan inicialmente a MainScreenAppear. Por el contrario, los usuarios que completan el tutorial antes de ingresar a la pagina presentan una mayor tasa de conversión.

# ## ¿Qué porcentaje de usuarios y usuarias hace todo el viaje desde su primer evento hasta el pago? <a id='puuhtvdpehp'></a>

# In[25]:


# Calcular el porcentaje de usuarios que completaron todo el viaje hasta el pago
total_users = users.shape[0]
users_completed_journey = users[~users['PaymentScreenSuccessful'].isna()].shape[0]
percentage_completed_mainscreenappear = (n_payment / n_mainscreen) * 100
percentage_completed_tutorial = (c_payment / c_mainscreen) * 100

print(f"Porcentaje de usuarios que completaron el viaje hasta el pago con la secuencia MainScreenAppear: {percentage_completed_mainscreenappear:.2f}%")
print(f"Porcentaje de usuarios que completaron el viaje hasta el pago con la secuencia Tutorial: {percentage_completed_tutorial:.2f}%")


# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# Has calculado correctamente el porcentaje de usuarios que completan el viaje desde el primer evento hasta el pago. Este es un hallazgo clave para el equipo de diseño y producto.</div>
# 

# ## ¿Cuántos usuarios y usuarias hay en cada grupo? <a id='cuucd'></a>

# In[26]:


#Agrupamos los datos para encontrar el numero de usuarios unicos por grupos
df.groupby('exp_id')['user_id'].nunique().reset_index()


# ### Observacion: <a id='observacion9'></a>
# 
# * El Grupo 246 tiene (2458) usuarios unicos.
# 
# * El Grupo 247 tiene (2517) usuarios unicos
# 
# * El Grupo 248 tiene (2540) usuarios unicos.
# 
# En general pudieramos decir que los grupos tienen registros de clientes unicos muy parecidos.

# # Estudiamos los resultados del experimento <a id='ere'></a>

# ## Tenemos dos grupos de control en el test A/A, donde comprobamos nuestros mecanismos y cálculos. Observamos si hay una diferencia estadísticamente significativa entre las muestras 246 y 247. <a id='tgctdcnmc'></a>
# 

# In[27]:


# Filtrar los datos para los grupos de control 246 y 247
group_246 = df[df['exp_id'] == 246]
group_247 = df[df['exp_id'] == 247]

# se contabilizan la cantidad de eventos por usuario/a en el grupo 246
# se hace con groupby() y se cuentan los eventos de la columna 'event_name' con count()
# se reinician los índices
counts_events_246 = group_246.groupby('user_id')['event_name'].count().reset_index()

# se cambian los nombres de las columnas
counts_events_246.columns = ['user_id', 'count_events']

# se imprime las 5 primeras filas
counts_events_246.head()


# In[28]:


# se contabilizan la cantidad de eventos por usuario/a en el grupo 247
# se hace con groupby() y se cuentan los eventos de la columna 'event_name' con count()
# se reinician los índices
counts_events_247 = group_247.groupby('user_id')['event_name'].count().reset_index()

# se cambian los nombres de las columnas
counts_events_247.columns = ['user_id', 'count_events']

# se imprime las 5 primeras filas
counts_events_247.head()


# In[29]:


# se establece el valor de alpha en 0.05
alpha = 0.05/24

# Realizar la prueba de Mann-Whitney de las dos muestras de A con la  función 'st.mannwhitneyu()'
results_A_A = st.mannwhitneyu(counts_events_246['count_events'], counts_events_247['count_events'])

print('El valor p es:', results_A_A.pvalue)

if results_A_A.pvalue < alpha:
    print('Se rechaza la hipótesis nula, hay diferencia entre los dos grupos')
else:
    print('No se rechaza la hipótesis nula, no hay diferencia entre los dos grupos')


# ### Observacion: <a id='observacion10'></a>
# 
# Podemos concluir que no hay una diferencia estadísticamente significativa entre las muestras 246 y 247.

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# ¡Gran trabajo! Has tomado una decisión acertada al utilizar la prueba <code>Mann-Whitney U</code> para comparar las distribuciones entre los grupos 246 y 247. Esta prueba no solo te permite analizar las diferencias en la mediana, sino también detectar cualquier variación en la forma o dispersión de los datos, lo cual es fundamental en un análisis como este. Dado que no siempre podemos asumir que los datos siguen una distribución normal, tu elección de una prueba no paramétrica garantiza un análisis más robusto y preciso. ¡Sigue así, estás demostrando una comprensión profunda de los métodos estadísticos!
# </div>
# 

# ## Seleccionamos el evento más popular. En cada uno de los grupos de control, encontramos la cantidad de usuarios y usuarias que realizaron esta acción. Encontramos su proporción. Comprobamos si la diferencia entre los grupos es estadísticamente significativa. Repetimos el procedimiento para todos los demás eventos. <a id='sep'></a>

# In[30]:


counts_users_events_246 = group_246.groupby('event_name')['user_id'].nunique().reset_index().sort_values(by='user_id', ascending=False)
counts_users_events_246


# In[31]:


counts_users_events_247 = group_247.groupby('event_name')['user_id'].nunique().reset_index().sort_values(by='user_id', ascending=False)
counts_users_events_247


# In[32]:


def proportion(df, event):
  total_users = df['user_id'].nunique()
  proportion = round(df[df['event_name']== event]['user_id'].nunique() / total_users, 3)
  return proportion

# con un bucle for se calcula la proporción para cada evento en el grupo 246
# se crea una lista con los nombres de los eventos de interés ordenados en de mayor a menor de acuerdo a su popularidad

events = ['MainScreenAppear', 'OffersScreenAppear', 'CartScreenAppear', 'PaymentScreenSuccessful', 'Tutorial']

for event in events:
    result_proportion = proportion(group_246, event) # se emplea la función proportion()
    print(f'La proporción del evento {event} es: {result_proportion}')


# In[33]:


# con un bucle for se calcula la proporción para cada evento en el grupo 247
for event in events:
    result_proportion = proportion(group_247, event) # se emplea la función proportion()
    print(f'La proporción del evento {event} es: {result_proportion}')


# ### Observacion: <a id='observacion11'></a>
# 
# A simple vista podemos ver que ambas proporcionas de los 2 grupos se parecen mucho ahora veamos como se compran uniendolas

# ## Comprobamos si la diferencia entre las proporciones de un evento en dos grupos es estadísticamente significativa. <a id='cdepege'></a>

# In[34]:


def test_proportions(group1, group2, event):
  """
  Comprueba si la diferencia entre las proporciones de un evento en dos grupos es estadísticamente
  significativa.

  Args:
    group1: DataFrame del primer grupo.
    group2: DataFrame del segundo grupo.
    event: Nombre del evento a comparar.

  Returns:
    Un diccionario con el valor p y si se rechaza la hipótesis nula.
  """
  #Calcula el número de usuarios únicos en el primer grupo.
  n1 = group1['user_id'].nunique()
  #Calcula el número de usuarios únicos en el segundo grupo.
  n2 = group2['user_id'].nunique()

  #Calcula el número de usuarios únicos que realizaron cada evento en el primer grupo.
  x1 = group1[group1['event_name'] == event]['user_id'].nunique()
  #Calcula el número de usuarios únicos que realizaron cada evento en el segundo grupo.
  x2 = group2[group2['event_name'] == event]['user_id'].nunique()

  purchases = np.array([x1, x2])
  leads = np.array([n1, n2])

  #Calcula la proporción de usuarios únicos que realizaron cada evento en el primer grupo
  p1 = purchases[0]/leads[0]
  #Calcula la proporción de usuarios únicos que realizaron cada evento en el segundo grupo
  p2 = purchases[1]/leads[1]

  #Calcula la proporción agrupada de usuarios que realizaron cada evento en ambos grupos.
  p_combined = (purchases[0] + purchases[1]) / (leads[0] + leads[1])

  #Calcula la puntuación z.
  z_value = (p1 - p2) / mth.sqrt(p_combined * (1 - p_combined) * (1/leads[0] + 1/leads[1]))

  # establece la distribución normal estándar (media 0, desviación estándar 1)
  distr = st.norm(0, 1)

  #Calculamos el p-value
  p_value = (1 - distr.cdf(abs(z_value))) * 2

  #Devuelve un diccionario con el valor p y si se debe rechazar la hipótesis nula.
  return {'p_value': p_value, 'reject_null': p_value < 0.05/24}


# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# ¡Excelente decisión al utilizar el estadístico <code>z</code> para comparar las proporciones de conversión entre los grupos! Este enfoque es ideal cuando se trata de proporciones, ya que permite evaluar si las diferencias observadas entre las tasas de conversión en los distintos grupos son estadísticamente significativas. Al aplicar esta técnica, has asegurado un análisis sólido de las conversiones, garantizando que cualquier diferencia detectada se deba a una verdadera variación entre los grupos y no a fluctuaciones aleatorias. ¡Gran trabajo, sigue aprovechando herramientas estadísticas tan poderosas!
# </div>
# 

# In[35]:


#Creamos un bucle for para iterar en cada evento y ambos grupos con funcion test_proportions
for event in events:
  results = test_proportions(group_246, group_247, event)
  print(f"Evento: {event}")
  print(f"Valor p: {results['p_value']}")
  print(f"Rechazar hipótesis nula: {results['reject_null']}")
  print("-" * 20)


# ### Observacion: <a id='observacion12'></a>
# 
# No se pudo rechazar la hipótesis nula: no hay razón para pensar que las proporciones son diferentes.
# 
# Por lo tanto, podemos afirmar nuestra hipotesis anterior, confirmamos que los grupos se dividieron correctamente.

# ## Realizamos lo mismo para el grupo con fuentes alteradas (248). Comparamos los resultados con los de cada uno de los grupos de control (246 y 247) para cada evento de forma aislada. Comparamos los resultados con los resultados combinados de los grupos de control. <a id='rmpgfa'></a>

# In[36]:


group_248= df[df['exp_id']== 248]

# se contabilizan la cantidad de eventos por usuario/a en el grupo 248
# se hace con groupby() y se cuentan los eventos de la columna 'event_name' con count()
# se reinician los índices
counts_events_248 = group_248.groupby('user_id')['event_name'].count().reset_index()

# se cambian los nombres de las columnas
counts_events_248.columns = ['user_id', 'count_events']

# se imprime las 5 primeras filas
counts_events_248.head()


# In[37]:


# con un bucle for se calcula la proporción para cada evento en el grupo 248
for event in events:
   result_proportion = proportion(group_248, event) # se emplea la función proportion()
   print(f'La proporción del evento {event} es: {result_proportion}')


# ### Observacion: <a id='observacion13'></a>
# 
# Desde ya podemos evidenciar al igual que con los grupos anteriores las proporciones son muy parecidas.

# ## Observamos si hay una diferencia estadísticamente significativa entre las muestras 246 y 248. <a id='odesem'></a>

# In[38]:


# se compara el grupo control 246 con el grupo con fuentes alteradas 248
# se establece el valor de alpha en 0.05
alpha = 0.05/24

# Realizar la prueba de Mann-Whitney de las muestras de del grupo 246 y el grupo 248 con la  función 'st.mannwhitneyu()'
results_246_248 = st.mannwhitneyu(counts_events_246['count_events'], counts_events_248['count_events'])

print('El valor p es:', results_246_248.pvalue)

if (results_246_248.pvalue < alpha):
    print("Hipótesis nula rechazada: existen diferencias significativas entre las distribuciones de los dos grupos comparados")
else:
    print("No se pudo rechazar la hipótesis nula: no hay diferencias entre los dos grupos")


# ## Observamos si hay una diferencia estadísticamente significativa entre las muestras 247 y 248. <a id='odesem78'></a>

# In[39]:


# se compara el grupo control 247 con el grupo con fuentes alteradas 248
# se establece el valor de alpha 0.05
alpha = 0.05/24

# Realizar la prueba de Mann-Whitney de las muestras de del grupo 247 y el grupo 248 con la  función 'st.mannwhitneyu()'
results_247_248 = st.mannwhitneyu(counts_events_247['count_events'], counts_events_248['count_events'])

print('El valor p es:', results_247_248.pvalue)

if (results_247_248.pvalue < alpha):
    print("Hipótesis nula rechazada: existen diferencias significativas entre las distribuciones de los dos grupos comparados")
else:
    print("No se pudo rechazar la hipótesis nula: no hay diferencias entre los dos grupos")


# In[40]:


#Buscamos el evento mas popular para el grupo 248

counts_users_events_248 = group_248.groupby('event_name')['user_id'].nunique().reset_index().sort_values(by='user_id', ascending=False)
counts_users_events_248


# ## Comparamos los eventos del grupo 246 con el grupo 248 <a id='cegg'></a>

# In[41]:


for event in events:
  results = test_proportions(group_246, group_248, event)
  print(f"Evento: {event}")
  print(f"Valor p: {results['p_value']}")
  print(f"Rechazar hipótesis nula: {results['reject_null']}")
  print("-" * 20)


# ## Observacion: <a id='observacion14'></a>
# 
# No hay razón para pensar que las proporciones son diferentes

# ## Comparamos los eventos del grupo 247 con el grupo 248 <a id='cegg78'></a>

# In[42]:


for event in events:
  results = test_proportions(group_247, group_248, event)
  print(f"Evento: {event}")
  print(f"Valor p: {results['p_value']}")
  print(f"Rechazar hipótesis nula: {results['reject_null']}")
  print("-" * 20)


# ### Observacion: <a id='observacion15'></a>
# 
# Los resultados de las pruebas estadísticas nos confirman nuevamente nuestra hipotesis, no evidencian diferencias significativas en las proporciones de eventos entre los grupos 246, 247 y 248. Por lo tanto, no se puede concluir que el grupo con fuentes alteradas 248 difiera de los grupos control en términos de las proporciones evaluadas.

# ## Comparamos los resultados con los resultados combinados de los grupos de control <a id='crrcgc'></a>

# In[43]:


#Unimos ya nuestra datos filtrados de cada grupo control con el metodo concat
control_groups= pd.concat([group_246, group_247])
counts_events_control= control_groups.groupby('user_id')['event_name'].count().reset_index()
counts_events_control.columns= ['user_id', 'count_events']
counts_events_control.head()


# In[44]:


# con un bucle for se calcula la proporción para cada evento en los grupos de control
for event in events:
    result_proportion = proportion(control_groups, event) # se emplea la función proportion()
    print(f'La proporción del evento {event} es: {result_proportion}')


# ### Observacion: <a id='observacion16'></a>
# 
# Nuevamente podemos dar la hipotesis de que las proporciones de los grupos de control unidos son muy parecidas a las proporciones anteriores.

# ## Observamos si hay una diferencia estadísticamente significativa entre las muestras control y 248. <a id='odesmc'></a>

# In[45]:


# se compara los grupos control con el grupo con fuentes alteradas 248
# se establece el valor de alpha en 0.05
alpha = 0.05/24

# Realizar la prueba de Mann-Whitney de las muestras de del grupo 247 y el grupo 248 con la  función 'st.mannwhitneyu()'
results_control_248 = st.mannwhitneyu(counts_events_control['count_events'], counts_events_248['count_events'])

print('El valor p es:', results_control_248.pvalue)

if (results_control_248.pvalue < alpha):
    print("Hipótesis nula rechazada: existen diferencias significativas entre las distribuciones de los dos grupos comparados")
else:
    print("No se pudo rechazar la hipótesis nula: no hay diferencias entre los dos grupos")


# In[46]:


#Buscamos el evento mas popular para los grupos control

counts_users_events_control = control_groups.groupby('event_name')['user_id'].nunique().reset_index().sort_values(by='user_id', ascending=False)
counts_users_events_control


# ### Observacion: <a id='observacion17'></a>
# 
# El evento popular en los 3 grupos evidentemente es MainScreenAppear

# ## Comparamos los eventos para los grupos control con el grupo 248 <a id='cepgcg'></a>

# In[47]:


for event in events:
  results = test_proportions(control_groups, group_248, event)
  print(f"Evento: {event}")
  print(f"Valor p: {results['p_value']}")
  print(f"Rechazar hipótesis nula: {results['reject_null']}")
  print("-" * 20)


# ### Observacion:  <a id='observacion18'></a>
# 
# Al no rechazar la hipótesis nula en cada uno de los eventos, afirmamos una vez mas nuestra hipotesis y se concluye que no existe evidencia estadística suficiente para afirmar que las proporciones de eventos sean distintas entre el grupo experimental (248) y los grupos control combinados.

# # Conclusion General: <a id='conclusion'></a>
# 
# No existe una diferencia estadísticamente significativa entre las proporciones de usuarios que realizaron cada evento entre los grupos de control (246 y 247) y el grupo de tratamiento (248).
# 
# El evento más popular fue MainScreenAppear.
# 
# **Hay dos secuencias principales de eventos:**
# 
# * Tutorial → MainScreenAppear → OffersScreenAppear → CartScreenAppear → PaymentScreenSuccessful
# ------------------------------------------------------
# * MainScreenAppear → OffersScreenAppear → CartScreenAppear → PaymentScreenSuccessful.
# 
# La mayoría de los usuarios se pierden entre los eventos OffersScreenAppear y PaymentScreenSuccessful.
# 
# La proporción de usuarios que completan todo el recorrido desde el primer evento hasta el pago es baja (alrededor del 6% para los usuarios que comienzan con MainScreenAppear y el 26% para los usuarios que comienzan con Tutorial).
# 
# Aplicando correcciones como Bonferroni. Realizamos 24 pruebas, el nivel de significancia para cada prueba individual en Bonferroni sería 0.0021 (0.05 / 24). Esto garantizaría que el nivel de error global sea de 0.05 y no se vea afectado por el número de comparaciones realizadas. ¡Este ajuste mejorará la precisión y la robustez del análisis! El nivel de significancia.
# 
# Para calcular el número de pruebas de hipótesis estadísticas realizadas, se debe contar el número de veces que se ha utilizado la función test_proportions() y las pruebas de Mann-Whitney. En este caso, se han realizado un total de 24 pruebas:
# 
# * 5 pruebas para comparar las proporciones de eventos entre los grupos 246 y 247.
# 
# * 5 pruebas para comparar las proporciones de eventos entre los grupos 246 y 248.
# 
# * 5 pruebas para comparar las proporciones de eventos entre los grupos 247 y 248.
# 
# * 5 pruebas para comparar las proporciones de eventos entre los grupos control y 248.
# 
# * 4 pruebas de Mann-Whitney para comparar las distribuciones de eventos entre los grupos.
# 
# Con un nivel de significancia de 0.1, existe una probabilidad del 10% de obtener un resultado falso positivo, es decir, rechazar la hipótesis nula cuando en realidad es verdadera.
# 
# En base a estos resultados, podemos concluir que el cambio de fuentes no parece intimidar a los usuarios y no afecta negativamente las tasas de conversión. Por lo tanto, el equipo de diseño puede proceder con la implementación de las nuevas fuentes en toda la aplicación con un bajo riesgo de afectar la experiencia del usuario o las métricas clave del negocio.

# # Recomendaciones <a id='recomendaciones'></a>
# 
# **Para el equipo de diseño:**
# 
# * **Implementar las nuevas fuentes:** Dado que el cambio de fuentes no tuvo un impacto negativo en el comportamiento del usuario, se recomienda implementar el nuevo diseño en toda la aplicación.
# 
# * **Monitorizar las métricas clave:** Después de la implementación, es fundamental monitorizar las métricas clave como la retención de usuarios, el engagement y las conversiones para asegurarse de que no haya efectos imprevistos a largo plazo.
# 
# * **Considerar la posibilidad de realizar pruebas A/B adicionales:** Si se introducen cambios de diseño adicionales en el futuro, se recomienda realizar pruebas A/B para evaluar su impacto y tomar decisiones basadas en datos.
# 
# **Para el equipo de producto:**
# 
# * **Optimizar el embudo de conversión:** Se observó una pérdida significativa de usuarios entre "Ver oferta" y "Pago". Se recomienda investigar las causas de esta pérdida y realizar mejoras en la experiencia del usuario para optimizar el embudo de conversión.
# 
# * **Personalizar la experiencia del tutorial:** Los usuarios que vieron el tutorial mostraron una mayor tasa de conversión. Se recomienda explorar formas de personalizar la experiencia del tutorial para que sea más atractiva y efectiva.
# 
# * **Segmentar usuarios:** Identificar los diferentes tipos de usuarios y sus necesidades para ofrecerles una experiencia más personalizada y relevante.
# 
# 
# **En general:**
# 
# * **Seguir utilizando un enfoque basado en datos:** Continuar utilizando pruebas A/B y análisis de datos para tomar decisiones informadas sobre el diseño y desarrollo de la aplicación.
# 
# * **Mantener una comunicación abierta entre equipos:** Fomentar la colaboración entre los equipos de diseño, producto y análisis para asegurar una experiencia de usuario coherente y optimizada.

# <div class="alert alert-block alert-success">
# <b>Éxito</b> <a class="tocSkip"></a>
# ¡Felicidades, Cristopher! Has realizado un excelente trabajo en este proyecto. Cada sección refleja un análisis cuidadoso y bien estructurado, desde la preparación de los datos hasta la interpretación de los resultados. Me impresiona cómo aplicaste correctamente la prueba <code>Mann-Whitney U</code> para comparar las distribuciones, y el uso del estadístico <code>z</code> para analizar las proporciones de conversión fue una decisión acertada. Además, tu razonamiento sobre la significancia estadística demuestra una sólida comprensión del análisis A/B.
# 
# Solo recuerda, dado que realizaste múltiples pruebas estadísticas, ajustar el nivel de significancia con una corrección como <code>Bonferroni</code> o <code>Sidak</code> es clave para mantener un control adecuado sobre los falsos positivos. Esto fortalecerá aún más tu análisis.
# 
# Es evidente que has dedicado mucho esfuerzo y detalle a este proyecto. ¡Sigue así! Estás construyendo una base sólida en análisis de datos y ciencia de la información. ¡Excelente trabajo!
# </div>
# 
