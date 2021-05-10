import os
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk


@st.cache
def load_data(path):
    df = pd.read_csv(path)
    try:
        df['margin_scaled'] = df['margin_disp'] - df['margin_disp'].min()
        df['margin_scaled'] /= df['margin_disp'].max()
        df['margin_scaled'] *= 100
    except:
        pass
    return df


df_dmk = load_data('./data/dmk_gj.csv')
df_admk = load_data('./data/admk_gj.csv')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Choose visualisation',
    ('DMK vs ADMK', 'Constituency-wise Margin')
)


view = pdk.data_utils.compute_view(df_dmk[["lng", "lat"]])
view.pitch = 75
view.bearing = 60

tooltip = {
    "html": "<b>Consituency:{consti_name}({consti_no})</b><br><b>Votes:</b>{votes}",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}
common_properties = {
    "radius": 500,
    "elevation_scale": 500,
}


column_layer = pdk.Layer(
    "ColumnLayer",
    data=df_dmk,
    get_position=["lng", "lat"],
    get_elevation="percentage",
    elevation_scale=common_properties['elevation_scale'],
    radius=common_properties['radius'],
    get_fill_color=["255,0,0"],
    pickable=True,
    auto_highlight=True,
)
column_layer_a = pdk.Layer(
    "ColumnLayer",
    data=df_admk,
    get_position=["lng", "lat"],
    get_elevation="percentage",
    elevation_scale=common_properties['elevation_scale'],
    radius=common_properties['radius'],
    get_fill_color=["0,255,0"],
    pickable=True,
    auto_highlight=True,
)

r = pdk.Deck(
    [column_layer, column_layer_a],
    initial_view_state=view,
    tooltip=tooltip,
    map_provider="mapbox",
    map_style="mapbox://styles/priyathamkatta/ckoi86td958ok17u6tfnqh2bl",
)
if add_selectbox == 'DMK vs ADMK':
    st.title(add_selectbox)

    st.pydeck_chart(r)
    st.markdown('''
    <div style='background-color:#FF0000; width:20px; height:20px; padding-left:20px;'>DMK</div>
    <div style='background-color:#008000; width:20px; height:20px;padding-left:20px;'>ADMK</div>
    ''', unsafe_allow_html=True)

elif add_selectbox == 'Constituency-wise Margin':
    st.title(add_selectbox)

    st.pydeck_chart(pdk.Deck(
        pdk.Layer(
            "ColumnLayer",
            data=df_dmk,
            get_position=["lng", "lat"],
            get_elevation="margin_scaled",
            elevation_scale=500,
            radius=1000,
            get_fill_color=["255, 237, 133"],
            pickable=True,
            auto_highlight=True,
        ),
        initial_view_state=view,
        tooltip={
            "html": "<b>Consituency:{consti_name}({consti_no})</b><br><b>Margin:</b>{margin}",
            "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
        },
        map_provider="mapbox",
        map_style="mapbox://styles/priyathamkatta/ckoi86td958ok17u6tfnqh2bl",
    ))

if __name__ == '__main__':
    pass
