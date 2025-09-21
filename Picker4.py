import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="NFL Elo Probabilities", layout="wide")
st.title("NFL Elo-Based Probabilities")

@st.cache_data
def fetch_projections():
    url = 'https://projects.fivethirtyeight.com/nfl-api/nfl_elo.csv'
    try:
        df = pd.read_csv(url)
        latest = df.groupby('team1').tail(1)
        projections = latest[['team1','team2','elo1_pre','elo2_pre']].copy()
        projections.rename(columns={
            'team1':'home',
            'team2':'away',
            'elo1_pre':'model_prob_home',
            'elo2_pre':'model_prob_away'
        }, inplace=True)
        # Ensure probabilities sum to 1
        projections['model_prob_away'] = 1 - projections['model_prob_home']
        return projections
    except Exception as e:
        st.error(f"Error fetching live data: {e}")
        return pd.DataFrame()

# Fetch live data
projections = fetch_projections()

if not projections.empty:
    st.subheader("Elo-Based Probabilities")
    st.dataframe(projections)

    st.subheader("Visual Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    ax.bar(projections['home'], projections['model_prob_home'], width, label='Home Win Prob')
    ax.bar(projections['away'], projections['model_prob_away'], width, bottom=projections['model_prob_home'], label='Away Win Prob')
    ax.set_ylabel('Probability')
    ax.set_xlabel('Teams')
    ax.set_title('Elo-Based Win Probabilities')
    ax.legend()
    plt.xticks(rotation=90)
    st.pyplot(fig)
else:
    st.warning("No live data available right now.")
