import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast

from supabase import create_client, Client

from credentials import *

from streamlit_cookies_controller import CookieController
import time

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    page_title="⌛ ECO Tijd",
    
)

def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()
rows_users = supabase.table("df_users_ecotijd").select("*").execute()
df_references = pd.DataFrame(rows_users.data)


controller = CookieController()


# --FUNCTIONS---
def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft",type="password")
    try:
        if name == None:
            st.stop()
        
        index = df_references[df_references['username']==name].index[0]
        true_password = df_references.loc[index,"password"]
        type = df_references.loc[index,"type"]

    except:
        st.warning("De gebruikersnaam is niet correct.")
        st.stop()
                             
    if st.button("logIn"):
        if password == true_password:
            controller.set("name", name)
            controller.set("password", password)
            controller.set("type", type)
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")



#---APP---
page_1 = st.Page("page/hours_filling.py", title="Uren invullen formulier",icon=":material/timer:" )
page_2 = st.Page("page/dashboard.py", title="Dashboard",icon=":material/bar_chart:" )
page_3 = st.Page("page/dashboard_editor.py", title="Dashboard",icon=":material/bar_chart:" )
page_4 = st.Page("page/insert.py", title="Project uploaden",icon=":material/upload:" )



#---APP---
IMAGE = "image/logo.png"
st.logo(IMAGE,  link=None, size="large",icon_image=IMAGE)

user_id = controller.get("name")


time.sleep(1)
if not user_id:
    logIn()
    st.stop()



if controller.get("type") == 'user':

    pg = st.navigation([page_1,page_2],position="top")

elif controller.get("type") == 'editor':

    pg = st.navigation([page_1,page_2,page_3,page_4],position="top")
    
else:
    pg = st.navigation([page_1,page_2,page_3],position="top")


pg.run()
