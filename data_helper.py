import os
import json
import pandas as pd
from utils import get_alliance
from shapely.geometry import Polygon, Point, MultiPolygon

with open('./data/TN_AC.geojson') as f:
    ac_gj = json.load(f)

results_df = pd.read_csv('./DetailedResults21.csv')


def convert_shapely_polygon(name, geometry):
    try:
        if geometry['type'] == 'Polygon':
            return Polygon(geometry['coordinates'][0])

        elif geometry['type'] == 'MultiPolygon':
            return MultiPolygon([Polygon(pol) for pol in geometry['coordinates'][0]])
    except Exception as e:
        print(name, e)
        return None


def generate_columnlayer_data(add=0.005):
    shapely_dts = {ac['properties']['AC_NO']: convert_shapely_polygon(ac['properties']['AC_NO'], ac['geometry'])
                   for ac in ac_gj['features']}

    results_df['temp'] = results_df['Party Name'].apply(
        lambda x: get_alliance(x, "2021"))

    df_a = []
    df_b = []
    # add = 0.005
    for feat in ac_gj['features']:
        ac_no = feat['properties']['AC_NO']
        consti_df = results_df[(results_df['Constituency No.'] == ac_no)]
        dmk_votes = int(consti_df[consti_df['temp'].isin(
            ['DMK', 'DMK+'])]['Total Valid Votes'].iloc[0])
        admk_votes = int(consti_df[consti_df['temp'].isin(
            ['AIADMK', 'AIADMK+'])]['Total Valid Votes'].iloc[0])
        total_votes = consti_df['Total Votes'].iloc[0]
        margin = int(consti_df['margin'].iloc[0])

        df_a.append({
            "consti_no": feat['properties']['AC_NO'],
            "consti_name": feat['properties']['AC_NAME'],
            "votes": dmk_votes,
            "percentage": int((dmk_votes/total_votes)*100),
            'margin': margin,
            'margin_disp': margin if margin>0 else 0,
            "lat": shapely_dts[ac_no].representative_point().coords[0][1],
            "lng": shapely_dts[ac_no].representative_point().coords[0][0]
        })
        df_b.append({
            "consti_no": feat['properties']['AC_NO'],
            "consti_name": feat['properties']['AC_NAME'],
            "votes": admk_votes,
            "percentage": int((admk_votes/total_votes)*100),
            'margin': margin,
            "lat": shapely_dts[ac_no].representative_point().coords[0][1]+add,
            "lng": shapely_dts[ac_no].representative_point().coords[0][0]+add
        })

    pd.DataFrame(df_a).to_csv('./data/dmk_gj.csv', index=False)
    pd.DataFrame(df_b).to_csv('./data/admk_gj.csv', index=False)


def gj_results():
    for feat in ac_gj['features']:
        ac_no = feat['properties']['AC_NO']
        consti_df = results_df[(results_df['Constituency No.'] == ac_no)]
        result = 'Win' if consti_df['margin'].iloc[0] > 0 else 'Lose'
        feat['properties']['result'] = result

    with open('./ac_tn_results_gj.geojson', 'w') as f:
        json.dump(ac_gj, f)


generate_columnlayer_data(0.007)
