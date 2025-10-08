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

def insert_project(project,opdracht,level,n_hours,hour_loon):
    
  data = {"project":project,"opdracht":opdracht,"level":level,"n_hours":n_hours,"hour_loon":hour_loon}

  response = (
          supabase.table("ekotijd_projects")
          .insert(data)
          .execute()
      )

@st.dialog(" ")
def delete_item(id):
  if st.button("Let op! Klik hier als je dit wilt verwijderen",icon="🚨",type="primary",use_container_width=True):
      response = (
          supabase.table("ekotijd_projects")
          .delete()
          .eq("id", id)
          .execute()
          )
      st.rerun()




# --- APP ---
IMAGE = "Images/logo.png"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

waarnemer = controller.get('name')

selected = option_menu(None,["Formulier", 'Projecten'], icons=['bi-pen', 'bi-card-checklist'],orientation="horizontal",)

if selected == "Formulier":
  with st.form("my_form", clear_on_submit=True,border=True): 
    project  = st.text_input('Project', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    opdracht = st.text_input('Opdracht', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    level = st.selectbox("Niveau", ['Starter','Medior','Senior'], index=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")  
    n_hours = st.number_input('Totaal vaste uren', min_value=0, max_value=None, value='min', step=1, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")    
    hour_loon = st.number_input('Uur loon', min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    
    if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):    
        insert_project(project,opdracht,level,n_hours,hour_loon)

elif selected == 'Data':
  # try:
  df = supabase.table("ekotijd_projects").select("*").execute()
  df = pd.DataFrame(df.data)      
  df
  st.write('puparuolo')
  
  # except:
  #   st.image('https://t4.ftcdn.net/jpg/04/72/65/73/360_F_472657366_6kV9ztFQ3OkIuBCkjjL8qPmqnuagktXU.jpg',width=450)    
