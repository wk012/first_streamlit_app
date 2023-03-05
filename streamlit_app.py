import streamlit
import pandas as pd
import requests as rs
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')


streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Bluebaerry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free -Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:" , list(my_fruit_list.index),['Avocado','Strawberries'])

fruit_to_show = my_fruit_list.loc[fruit_selected]

# Display the table on the page.
streamlit.dataframe(fruit_to_show)


def get_fruit_data (this_fruit_choice):
    fruityvice_response = rs.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_norm = pd.json_normalize(fruityvice_response.json())
    return fruityvice_norm

streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please Select fruit to get info')
  else:
    back_from_function = get_fruit_data(fruit_choice)
    #streamlit.write('The user entered',fruit_choice)
    streamlit.dataframe(back_from_function)
  
except URLError as e:
    streamlit.error()
    
# streamlit.text(fruityvice_response.json()) Just writes to the screen

#Snowflake functions
def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_list()
    streamlit.dataframe(my_data_row)


def inset_sf_row(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("Insert into fruit_load_list values ('from streamlit')")
         return "Thanks for adding" +new_fruit

add_my_fruit = streamlit.text_input('What fruit to add?','')
 
if streamlit.button('Add Fruit to list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = inset_sf_row(add_my_fruit)
    streamlit.text(back_from_function)
    
    
    
streamlit.stop() #stops code from running below this line 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit to add?','')
streamlit.write('Thanks for adding',add_my_fruit)

my_cur.execute("Insert into fruit_load_list values ('from streamlit')")


