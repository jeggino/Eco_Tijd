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


def logOut():
    if st.button("logOut",use_container_width=True):
        controller.remove("name")
        st.rerun()



logOut()
