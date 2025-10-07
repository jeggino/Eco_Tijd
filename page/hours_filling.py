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


controller = CookieController()


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
def insert_hours(waarnemer,datum,project,opdracht,opmerking):
    
  data = {"waarnemer":waarnemer,"datum":datum,"project":project,"opdracht":opdracht,"opmerking":opmerking}

  response = (
          supabase.table("ekotijd_df_hours")
          .insert(data)
          .execute()
      )

@st.dialog(" ")
def delete_item(key):
  if st.button("Let op! Klik hier als je dit wilt verwijderen",icon="🚨",type="primary",use_container_width=True):
      response = (
          supabase.table("ekotijd_df_hours")
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
    
  if st.form_submit_button("**Gegevens opslaan**",use_container_width=True):

    datum  = st.date_input(label, value="today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible", width="stretch")
    project = None
    opdracht = None
    opmerking = None

    

        insert_hours(waarnemer,datum,project,opdracht,opmerking)
