
# ============================================================
# IMPORTS
# ============================================================

import psycopg2
import streamlit as st

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return psycopg2.connect(
        dbname=st.secrets["database"]["database"],
        user=st.secrets["database"]["username"],
        password=st.secrets["database"]["password"],
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        sslmode=st.secrets["database"]["sslmode"],
    )