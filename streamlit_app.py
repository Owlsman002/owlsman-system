import streamlit as st
import numpy as np
from scipy.stats import poisson


# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="OWLSNATION ENGINE",
    layout="wide"
)


# ==========================================================
# PASSWORD
# ==========================================================

PASSWORD = "OWLSNATION123"

user_password = st.text_input(
    "Password",
    type="password"
)

if user_password != PASSWORD:
    st.stop()


st.title("🦉 OWLSNATION QUANT ENGINE")


# ==========================================================
# SAFE FUNCTIONS
# ==========================================================

def safe_div(a, b):
    if b == 0:
        return 0
    return a / b


def odds(prob):
    if prob <= 0:
        return 999
    return 1 / prob



# ==========================================================
# PHASE 1
# ==========================================================

def phase_one(goals, shots):

    percentage = (
        safe_div(goals, shots)
        * 100
    )

    calculated = (
        safe_div(1, percentage)
        * 100
    )

    return calculated



# ==========================================================
# PHASE 2
# ==========================================================

def phase_two(
    calc_scored_A,
    calc_conceded_A,
    calc_scored_B,
    calc_conceded_B,

    goals_A,
    goals_B,

    conceded_A,
    conceded_B,

    sot_A,
    sot_B
):

    # Team A

    net_A = safe_div(
        calc_scored_A,
        calc_conceded_B
    )


    ratio_A = safe_div(
        goals_A,
        conceded_B
    )


    power_A = (
        safe_div(
            ratio_A,
            net_A
        )
        *
        sot_A
    )


    # Team B

    net_B = safe_div(
        calc_scored_B,
        calc_conceded_A
    )


    ratio_B = safe_div(
        goals_B,
        conceded_A
    )


    power_B = (
        safe_div(
            ratio_B,
            net_B
        )
        *
        sot_B
    )


    return power_A, power_B



# ==========================================================
# PHASE 3
# ==========================================================

def calculate_strength(
    xg,
    bc,
    score_power
):

    return (
        ((xg + bc) / 2)
        *
        score_power
    )



# ==========================================================
# PHASE 4 POISSON
# ==========================================================

def poisson_engine(
    home_strength,
    away_strength
):

    cap = 6


    home_matrix = [
        poisson.pmf(
            x,
            home_strength
        )
        for x in range(cap+1)
    ]


    away_matrix = [
        poisson.pmf(
            x,
            away_strength
        )
        for x in range(cap+1)
    ]


    grid = np.outer(
        home_matrix,
        away_matrix
    )


    home_win = np.sum(
        np.tril(
            grid,
            -1
        )
    )


    draw = np.sum(
        np.diag(grid)
    )


    away_win = np.sum(
        np.triu(
            grid,
            1
        )
    )


    total = (
        home_win
        +
        draw
        +
        away_win
    )


    home_win /= total
    draw /= total
    away_win /= total


    return (
        grid,
        home_win,
        draw,
        away_win
    )



# ==========================================================
# PHASE 5 STRESS MATRIX
# ==========================================================

def stress_matrix(
    home,
    draw,
    away
):

    sigma = 0.036

    drag = (
        100 * sigma
    )


    states={}


    # Odd 0

    states["Odd 0"]={
        "H":home,
        "D":draw,
        "A":away
    }


    # Odd 1 HOME

    h = (
        (home*100)
        +
        50
        -
        drag
    )

    d = draw*100
    a = away*100


    total = h+d+a


    states["Odd 1"]={
        "H":h/total,
        "D":d/total,
        "A":a/total
    }



    # Odd 2 AWAY

    a = (
        (away*100)
        +
        50
        -
        drag
    )

    h = home*100
    d = draw*100


    total=h+d+a


    states["Odd 2"]={
        "H":h/total,
        "D":d/total,
        "A":a/total
    }



    # Odd 3 DRAW

    d = (
        (draw*100)
        +
        50
        -
        drag
    )

    h=home*100
    a=away*100


    total=h+d+a


    states["Odd 3"]={
        "H":h/total,
        "D":d/total,
        "A":a/total
    }



    # Odd 4 CHAOS


    h=(home*100)+50-drag
    d=(draw*100)+50-drag
    a=(away*100)+50-drag


    total=h+d+a


    states["Odd 4"]={
        "H":h/total,
        "D":d/total,
        "A":a/total
    }


    return states



# ==========================================================
# INPUT
# ==========================================================

c1,c2=st.columns(2)


with c1:

    st.subheader("TEAM A")


    A_goals=st.number_input(
        "Average Goals Scored",
        value=2.0
    )


    A_conceded=st.number_input(
        "Average Goals Conceded",
        value=4.0
    )


    A_sot=st.number_input(
        "Average SOT For",
        value=5.0
    )


    A_sot_against=st.number_input(
        "Average SOT Against",
        value=3.0
    )


    A_xg=st.number_input(
        "Average xG",
        value=0.77
    )


    A_bc=st.number_input(
        "Average Big Chances",
        value=0.58
    )



with c2:

    st.subheader("TEAM B")


    B_goals=st.number_input(
        "Away Goals Scored",
        value=3.0
    )


    B_conceded=st.number_input(
        "Away Goals Conceded",
        value=5.0
    )


    B_sot=st.number_input(
        "Away SOT For",
        value=2.0
    )


    B_sot_against=st.number_input(
        "Away SOT Against",
        value=8.0
    )


    B_xg=st.number_input(
        "Away xG",
        value=0.89
    )


    B_bc=st.number_input(
        "Away Big Chances",
        value=0.50
    )



st.divider()


if st.button("RUN MODEL"):


    # Phase 1


    A_calc_score = phase_one(
        A_goals,
        A_sot
    )


    A_calc_concede = phase_one(
        A_conceded,
        A_sot_against
    )


    B_calc_score = phase_one(
        B_goals,
        B_sot
    )


    B_calc_concede = phase_one(
        B_conceded,
        B_sot_against
    )



    # Phase 2


    A_power,B_power = phase_two(

        A_calc_score,
        A_calc_concede,

        B_calc_score,
        B_calc_concede,

        A_goals,
        B_goals,

        A_conceded,
        B_conceded,

        A_sot,
        B_sot

    )



    # Phase 3


    A_strength = calculate_strength(
        A_xg,
        A_bc,
        A_power
    )


    B_strength = calculate_strength(
        B_xg,
        B_bc,
        B_power
    )



    # Phase 4


    grid,H,D,A = poisson_engine(
        A_strength,
        B_strength
    )


    st.subheader("BASELINE ODD 0")


    st.write(
        "Team A:",
        round(odds(H),2)
    )

    st.write(
        "Draw:",
        round(odds(D),2)
    )

    st.write(
        "Team B:",
        round(odds(A),2)
    )



    # Phase 5


    states=stress_matrix(
        H,
        D,
        A
    )


    st.subheader("MASTER BLENDED ODDS")


    blend_H=np.mean(
        [
            states[x]["H"]
            for x in states
        ]
    )


    blend_D=np.mean(
        [
            states[x]["D"]
            for x in states
        ]
    )


    blend_A=np.mean(
        [
            states[x]["A"]
            for x in states
        ]
    )


    st.write(
        "Team A:",
        round(odds(blend_H),2)
    )


    st.write(
        "Draw:",
        round(odds(blend_D),2)
    )


    st.write(
        "Team B:",
        round(odds(blend_A),2)
    )



    # Dominance


    dom_H=sum(
        states[x]["H"]-H
        for x in states
    )


    dom_A=sum(
        states[x]["A"]-A
        for x in states
    )


    st.subheader("DOMINANCE")


    st.write(
        "Team A:",
        round(dom_H,4)
    )


    st.write(
        "Team B:",
        round(dom_A,4)
    )



    # Correct Scores


    flat=grid.flatten()


    indexes=np.argsort(flat)[::-1][:2]


    st.subheader("CORRECT SCORES")


    for i in indexes:

        h,a=np.unravel_index(
            i,
            grid.shape
        )

        st.write(
            f"{h}-{a}"
        )
