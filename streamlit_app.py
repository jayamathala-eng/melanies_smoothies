# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(  """Choose the Fruits you want in your Smoothie!.""")
name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be',name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
ingredients_list=st.multiselect('Choose upto 5 Ingredients:',my_dataframe)
if ingredients_list and len(ingredients_list) > 5:
    st.error('You can choose a maximum of 5 ingredients!')
elif ingredients_list:
    ingredients_string= ''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(name_on_order+' '+'Your Smoothie is ordered!', icon="✅")
