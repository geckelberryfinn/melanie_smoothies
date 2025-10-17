# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits for your custom Smoothie 
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
name_on_smoothie = st.text_input("Name on Smoothie:")

dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
ingridients = st.multiselect("Choose up to 5 fruits", 
                             dataframe,
                            max_selections=5)
if ingridients:
    ingridients_string = ''

    for fruit in ingridients:
        ingridients_string += fruit + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order ,ingredients)
            values ('""" + name_on_smoothie + "','" + ingridients_string + """')"""
    time_to_insert = st.button("Sumbit")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
            
# st.dataframe(data=dataframe, use_container_width=True)
