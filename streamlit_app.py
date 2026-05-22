# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests  # Cleaned up import location

# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write("""Choose the Fruits you want in your Smoothie!.""")

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)

# Connect to Snowflake using secrets
session = Session.builder.configs(st.secrets["snowflake"]).create()

# Convert Snowpark table column explicitly to a pandas dataframe for st.multiselect
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME').to_pandas()

ingredients_list = st.multiselect('Choose up to 5 Ingredients:', my_dataframe['FRUIT_NAME'])

if ingredients_list and len(ingredients_list) > 5:
    st.error('You can choose a maximum of 5 ingredients!')
elif ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name_on_order + ' ' + 'Your Smoothie is ordered!', icon="✅")

# Fixed indentation, removed markdown link syntax, and printed the JSON payload
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
if smoothiefroot_response.status_code == 200:
    st.json(smoothiefroot_response.json())
else:
    st.error("Could not fetch fruit details from API.")
