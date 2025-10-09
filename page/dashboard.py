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
supabase = init_connection()
waarnemer = controller.get('name')

IMAGE = "Images/logo.png"


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


# def get_data():
#     df = supabase.table("ekotijd_hours").select("*").execute()
#     df = pd.DataFrame(df.data)                
#     df = df[(df['waarnemer']==waarnemer)]
#     return df

# --- APP ---

st.logo(IMAGE,  link=None, size="large", icon_image=IMAGE)



options = ["North", "East", "South", "West"]
selection = st.segmented_control(
    "Directions", options, selection_mode="single"
)


# get_data()
