  import streamlit as st
import numpy as np
from scipy.stats import poisson

st.title("⚽ Football Prediction Engine")

# --- PHASE 1 & 2: INPUTS ---
st.header("1. Team Statistics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Team A (Home)")
    a_goal = st.number_input("Avg Goals Scored", 0.0, 10.0, 2.0)
    a_conc = st.number_input("Avg Goals Conceded", 0.0, 10.0, 4.0)
    a_sot = st.number_input("Avg Shots on Target", 0.0, 20.0, 5.0)
    a_sot_against = st.number_input("Avg SoT Against", 0.0, 20.0, 3.0)
    a_xg = st.number_input("Avg xG", 0.0, 5.0, 0.77)
    a_big = st.number_input("Avg Big Chances", 0.0, 5.0, 0.58)

with col2:
    st.subheader("Team B (Away)")
    b_goal = st.number_input("Avg Goals Scored ", 0.0, 10.0, 3.0)
    b_conc = st.number_input("Avg Goals Conceded ", 0.0, 10.0, 5.0)
    b_sot = st.number_input("Avg Shots on Target ", 0.0, 20.0, 2.0)
    b_sot_against = st.number_input("Avg SoT Against ", 0.0, 20.0, 8.0)
    b_xg = st.number_input("Avg xG ", 0.0, 5.0, 0.89)
    b_big = st.number_input("Avg Big Chances ", 0.0, 5.0, 0.50)

if st.button("Calculate Prediction"):
    # Phase 1 Logic
    a_calc_s = (1 / (a_goal / a_sot * 100)) * 100
    a_calc_c = (1 / (a_conc / a_sot_against * 100)) * 100
    b_calc_s = (1 / (b_goal / b_sot * 100)) * 100
    b_calc_c = (1 / (b_conc / b_sot_against * 100)) * 100
    
    # Phase 2 Logic
    a_net = a_calc_s / b_calc_c
    a_power = (a_goal / b_conc) / a_net * a_sot
    
    b_net = b_calc_s / a_calc_c
    b_power = (b_goal / a_conc) / b_net * b_sot
    
    # Phase 3 Logic
    home_strength = ((a_xg + a_big) / 2) * a_power
    away_strength = ((b_xg + b_big) / 2) * b_power
    
    # Poisson Matrix
    matrix = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            matrix[i, j] = poisson.pmf(i, home_strength) * poisson.pmf(j, away_strength)
            
    home_win = np.sum(np.tril(matrix, -1))
    draw = np.sum(np.diag(matrix))
    away_win = np.sum(np.triu(matrix, 1))
    
    st.success(f"Team A Strength: {home_strength:.2f} | Team B Strength: {away_strength:.2f}")
    
    st.table({
        "Outcome": ["Home Win", "Draw", "Away Win"],
        "Probability (%)": [home_win*100, draw*100, away_win*100],
        "Fair Odds": [1/home_win, 1/draw, 1/away_win]
    })
