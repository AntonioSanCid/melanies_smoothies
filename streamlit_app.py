# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
import requests
## importar función llamada col
from snowflake.snowpark.functions import col




# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

#
#import streamlit as lt

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your order Smoothie will be:',name_on_order)

# Se descarta el SelectBox debido a que ya tenemos la 
#tabla de opciones de frutas y es más extensa y más eficiente
# que colocar fruta por fruta manualmente

##option = st.selectbox(
##    "What´s your favorite fruit?",
##    ("Banana", "Strawberries", "Peaches"),
##)

##st.write("You selected:", option)


#Se agrega la sentancia .select(col('FRUIT_NAME')) 
# Para mostrar únicamente la columna con ese nombre

# Permite mostrar una tabla
#session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# para mostrar los datos de my_dataframe en formato de 
# multiselección y no de tabla usamos:
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
    # limitar la selección de frutas
    , max_selections=5
)

# para observar que datos contiene el 
# formato list al elegir opciones de frutas, usamos

##st.write(ingredients_list)

# o bien podemos usar

##st.text(ingredients_list)

#En este bloque if lo que estamos haciendo es 
# que creamos una lista vacía al principio y al
# momento de elegir una o más frutas de ingredients_list
# cada una de estas frutas se irá guardando en la lista
#ingredients_string
# para que al final de cada selección muestre los elementos 
# seleccionados usando st.write(ingredients_string)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    #lista vacía al principio
    ingredients_string =''

    # bucle for para agregar frutas dentro de ingredients_list
    #  la lista ingredients_string
    for fruit_chosen in ingredients_list:

        #+= significa " agregar esto a lo que  ya está en la variable "
        # se agrega + ' ' para agregar un espacio entre cada selección
        # de frutas y no se vea amontonado
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        # st.text(smoothiefroot_response.json())
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    # muestra la lista de frutas seleccionadas y alamacenadas en 
    # ingredients_string
    
    #st.write(ingredients_string)


    #aqui se crea un texto que empieza con insert...
    # y que contiene la lista de las frutas seleccionadas 
    # por el usuario 
    my_insert_stmt = """
    insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
    values ('""" + ingredients_string + """','""" + name_on_order + """')
    
    """

    #st.write(my_insert_stmt)
    #st.stop()
    # se muestra el texto creado en my_insert_stmt
    
    #st.write(my_insert_stmt)


    #Sobre este bloque de código indicamos que la 
    # lista de ingredientes que ha seleccionado el usuario
    # debemos ejecutar en una sesión de sql la sentencia
    # dentro de my_insert_stmt y envíar un mensaje de 
    # confirmación de pedido una vez que se ha dado
    # click en el botón

    #agregamos botón de envío para asegurar que el
    #cliente ha terminado de seleccionar
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(""" Your Smoothie is ordered, """ +name_on_order+ """!""" ,icon="✅")

    
#Agrega un cuadro con nombre para pedidos de batidos




