import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide")

st.markdown("""
<style>
    button[data-testid="baseButton-secondary"]:has(div:contains("↑")) {
        background-color: #2e7d32 !important;
        color: white !important;
        padding: 0px !important;
        min-height: 28px !important;
    }
    
    button[data-testid="baseButton-secondary"]:has(div:contains("↓")) {
        background-color: #d32f2f !important;
        color: white !important;
        padding: 0px !important;
        min-height: 28px !important;
    }

    hr {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }

    h1 {
        margin-top: 2.5rem !important;
    }
    
    div.stButton > button {
        padding: 0.1rem 0.5rem !important;
        font-size: 0.8rem !important;
    }
    
    .stTextInput > div > div > input {
        padding: 0.1rem 0.5rem !important;
        line-height: 1.2 !important;
    }
    
    div.row-widget {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    section {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    section > div {
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

STATE_FILE = "dashboard_state.json"

COLORS = [
    '#a7e9af', '#ffd166', '#ef767a', '#7dace4',
    '#d4a0fa', '#ff9e79', '#9de3d0', '#b1b1b1'
]

def save_state_to_json():
    with open(STATE_FILE, 'w') as f:
        json.dump(st.session_state.areas, f, indent=4)

def load_state_from_json():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'Product': {
            'Visual Aesthetics': 1,
            'User Experience (ML Engineers)': 3,
            'Authentication': 2,
            'Notebooks': 4
        },
        'Distribution': {
            'Education Content': 6,
            'Presence of Socials': 1,
            'Open Source Contributions': 2
        },
        'Revenue': {'TBD': 0},
        'Partners': {'TBD': 0}
    }

if 'areas' not in st.session_state:
    st.session_state.areas = load_state_from_json()

def add_section():
    new_section = st.session_state.new_section_name
    if new_section and new_section not in st.session_state.areas:
        st.session_state.areas[new_section] = {'New Area': 0}
        st.session_state.new_section_name = ""
        save_state_to_json()

def add_area(section):
    new_area = st.session_state[f"new_area_{section}"]
    if new_area and new_area not in st.session_state.areas[section]:
        st.session_state.areas[section][new_area] = 0
        st.session_state[f"new_area_{section}"] = ""
        save_state_to_json()

def update_blocks(section, area, action):
    current = st.session_state.areas[section][area]
    if action == "add":
        st.session_state.areas[section][area] += 1
        save_state_to_json()
    elif action == "remove" and current > 0:
        st.session_state.areas[section][area] -= 1
        save_state_to_json()

st.markdown("# 🚀 Enverge Overview")
st.markdown("#### Main Areas of Focus")

for i, (section, areas) in enumerate(st.session_state.areas.items()):
    st.markdown(f"### {section}")
    
    color_index = i % len(COLORS)
    section_color = COLORS[color_index]
    
    for area, blocks in areas.items():
        col1, col2 = st.columns([3, 9])
        
        with col1:
            st.markdown(f"**{area}**")

        with col2:
            button_cols = st.columns([1, 8, 1])
            with button_cols[0]:
                st.button("↑", key=f"add_{section}_{area}", 
                         on_click=update_blocks, args=(section, area, "add"))
            
            with button_cols[1]:
                block_html = ""
                for i in range(blocks):
                    block_html += f'<span style="display: inline-block; width: 30px; height: 35px; background-color: {section_color}; margin-right: 5px; border-radius: 3px;"></span>'
                
                if blocks > 0:
                    st.markdown(block_html, unsafe_allow_html=True)
            
            with button_cols[2]:
                if blocks > 0:
                    st.button("↓", key=f"remove_{section}_{area}", 
                             on_click=update_blocks, args=(section, area, "remove"))
        
        st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([9, 2, 1])
    with col2:
        st.text_input(f"Add to {section}", key=f"new_area_{section}", 
                    label_visibility="collapsed", placeholder=f"Add to {section}")
    with col3:
        st.button("Add", key=f"add_area_btn_{section}", on_click=add_area, args=(section,))
    
    st.markdown("<hr style='margin-top: 0.3rem; margin-bottom: 0.3rem'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([8, 2, 2])
with col2:
    st.text_input("Add New Section", key="new_section_name", 
                label_visibility="collapsed", placeholder="Add New Section")
with col3:
    st.button("Add Section", key="add_section_btn", on_click=add_section)
