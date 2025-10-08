import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date
from natsort import natsorted
import altair as alt

from supabase import create_client, Client
from streamlit_option_menu import option_menu

import random

from streamlit_cookies_controller import CookieController
import time



def init_connection():
  url = st.secrets["SUPABASE_URL"]
  key = st.secrets["SUPABASE_KEY"]
  return create_client(url, key)




controller = CookieController()
supabase = init_connection()


df = supabase.table("ekotijd_projects").select("*").execute()
df = pd.DataFrame(df.data)                

#options




st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] svg {
        height: 0rem;
        width: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

def init_connection():
  url = st.secrets["SUPABASE_URL"]
  key = st.secrets["SUPABASE_KEY"]
  return create_client(url, key)

supabase = init_connection()


# --- FUNCTIONS ---
def insert_hours(waarnemer,datum,project,opdracht,level,opmerking):
    
  data = {"waarnemer":waarnemer,"datum":datum,"project":project,"opdracht":opdracht,"level":level,"opmerking":opmerking}

  response = (
          supabase.table("ekotijd_hours")
          .insert(data)
          .execute()
      )

@st.dialog(" ")
def delete_item(key):
  if st.button("Let op! Klik hier als je dit wilt verwijderen",icon="🚨",type="primary",use_container_width=True):
      response = (
          supabase.table("ekotijd_hours")
          .delete()
          .eq("key", key)
          .execute()
          )
      st.rerun()




# --- APP ---
IMAGE = "Images/logo.png"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

waarnemer = controller.get('name')

with st.form("my_form", clear_on_submit=True,border=True): 
  datum  = st.date_input("Datum", value="today", format="YYYY/MM/DD", disabled=False, label_visibility="visible", width="stretch")

  project_options = df['project'].unique()
  project = st.selectbox("Project", project_options, index=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")

  opdracht_options = df[df['project']==project]['opdracht'].unique()
  opdracht = st.selectbox("Opdracht", opdracht_options, index=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")

  level_options = df[(df['project']==project)&(df['opdracht']==opdracht)]['level'].unique()
  level = st.selectbox("Niveau", ['Starter','Medior','Senior'], index=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")
  
  opmerking = st.text_area("Opmerking", value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", width="stretch")
  
  if st.form_submit_button("**Gegevens opslaan**",use_container_width=True): 
    if project or opdracht or level == None:
      st.write('fiil the input, please')
      st.stop()
    else:
      insert_hours(waarnemer,str(datum),project,opdracht,level,opmerking)
