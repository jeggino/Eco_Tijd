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

@st.dialog(" ")
def update_item(id,project_id,opdracht_id,level_id,n_hours_id,hour_loon_id):

  project  = st.text_input('Project', value=project_id, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
  opdracht = st.text_input('Opdracht', value=opdracht_id, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
  level = st.selectbox("Niveau", ['Starter','Medior','Senior'], index=['Starter','Medior','Senior'].index(level_id), disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")  
  n_hours = st.number_input('Totaal vaste uren', min_value=0, max_value=None, value=n_hours_id, step=1, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")    
  hour_loon = st.number_input('Uur loon', min_value=None, max_value=None, value=hour_loon_id, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")

  if st.button("**Update**", type="primary",use_container_width=True):
      data = {"project":project,"opdracht":opdracht,"level":level,"n_hours":n_hours,'hour_loon':hour_loon}
      response = (
          supabase.table("ekotijd_projects")
          .update(data)
          .eq("id", id)
          .execute()
          )
      
      st.rerun()





# --- APP ---
IMAGE = "Images/logo.png"
st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)

waarnemer = controller.get('name')

selected = option_menu(None,["Formulier", 'Taken'], icons=['bi-pen', 'bi-card-checklist'],orientation="horizontal",)

if selected == "Formulier":
  with st.form("my_form", clear_on_submit=True,border=True): 
    project  = st.text_input('Project', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    opdracht = st.text_input('Opdracht', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    level = st.selectbox("Niveau", ['Starter','Medior','Senior'], index=None, disabled=False, label_visibility="visible", accept_new_options=False, width="stretch")  
    n_hours = st.number_input('Totaal vaste uren', min_value=0, max_value=None, value='min', step=1, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")    
    hour_loon = st.number_input('Uur loon', min_value=None, max_value=None, value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible", icon=None, width="stretch")
    
    if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):    
        insert_project(project,opdracht,level,n_hours,hour_loon)

elif selected == 'Taken':
  # try:
  df = supabase.table("ekotijd_projects").select("*").execute()
  df = pd.DataFrame(df.data)      




  event = st.dataframe(
      df,
      column_order = ['project','opdracht','level','n_hours','hour_loon'],
      column_config={
        "project": "Project",
        "opdracht": "Opdracht",
        "level": "Niveau",
        "n_hours": "Totaal vaste uren",
        "hour_loon": st.column_config.NumberColumn("Uur loon", format="€ %d"),

      },
      hide_index=True,
      key="data",
      on_select="rerun",
      selection_mode=["single-row"]
  )

  if len(event.selection['rows']) != 0:
    if st.button("Taak bijwerken",use_container_width=True):
      id = df.loc[event.selection['rows'][0],'id']
      project_id = df.loc[event.selection['rows'][0],'project']
      opdracht_id = df.loc[event.selection['rows'][0],'opdracht']
      level_id = df.loc[event.selection['rows'][0],'level']
      n_hours_id = df.loc[event.selection['rows'][0],'n_hours']
      hour_loon_id = df.loc[event.selection['rows'][0],'hour_loon']

      update_item(id,project_id,opdracht_id,level_id,n_hours_id,hour_loon_id)
      
      
    if st.button(":red[**Taak verwijder**]",use_container_width=True):
      delete_item(df.loc[event.selection['rows'][0],'id'])

