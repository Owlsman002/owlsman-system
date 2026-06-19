import streamlit as st
import numpy as np
from scipy.stats import poisson
import math


# ==========================
# APP SETTINGS
# ==========================

st.set_page_config(
    page_title="OWLSNATION ENGINE",
    layout="wide"
)


st.title("🦉 OWLSNATION BETTING ENGINE")


# ==========================
# SAFE FUNCTIONS
# ==========================

def safe_div(a,b):

    if b == 0:
        return 0

    return a/b



def odd_converter(prob):

    if prob <= 0:
        return 999

    return round(1/prob,2)



# ==========================
# MANUAL INPUT
# ==========================


home_team = st.text_input(
    "Home Team",
    "Team A"
)


away_team = st.text_input(
    "Away Team",
    "Team B"
)



st.header("HOME LAST 4 MATCHES")


G_A = st.number_input(
    "Home Average Goals Scored",
    value=2.0
)


C_A = st.number_input(
    "Home Average Goals Conceded",
    value=4.0
)


SOT_A = st.number_input(
    "Home Shots On Target For",
    value=5.0
)


SOTA_A = st.number_input(
    "Home Shots On Target Against",
    value=3.0
)


xG_A = st.number_input(
    "Home xG",
    value=0.77
)


BC_A = st.number_input(
    "Home Big Chances",
    value=0.58
)




st.header("AWAY LAST 4 MATCHES")


G_B = st.number_input(
    "Away Average Goals Scored",
    value=3.0
)


C_B = st.number_input(
    "Away Average Goals Conceded",
    value=5.0
)


SOT_B = st.number_input(
    "Away Shots On Target For",
    value=2.0
)


SOTA_B = st.number_input(
    "Away Shots On Target Against",
    value=8.0
)


xG_B = st.number_input(
    "Away xG",
    value=0.89
)


BC_B = st.number_input(
    "Away Big Chances",
    value=0.50
)



st.header("BOOKMAKER ODDS")


book_home = st.number_input(
    "Book Home Odd",
    value=3.00
)


book_draw = st.number_input(
    "Book Draw Odd",
    value=3.20
)


book_away = st.number_input(
    "Book Away Odd",
    value=2.20
)




# ==========================
# RUN ENGINE
# ==========================


if st.button("RUN MODEL"):



    # ======================
    # PHASE 1
    # ======================


    Calc_Scored_A = safe_div(
        100,
        safe_div(G_A,SOT_A)*100
    )


    Calc_Concede_A = safe_div(
        100,
        safe_div(C_A,SOTA_A)*100
    )


    Calc_Scored_B = safe_div(
        100,
        safe_div(G_B,SOT_B)*100
    )


    Calc_Concede_B = safe_div(
        100,
        safe_div(C_B,SOTA_B)*100
    )



    # ======================
    # PHASE 2
    # ======================


    Net_A = safe_div(
        Calc_Scored_A,
        Calc_Concede_B
    )


    Ratio_A = safe_div(
        G_A,
        C_B
    )


    Power_A = (
        safe_div(
            Ratio_A,
            Net_A
        )
        *
        SOT_A
    )



    Net_B = safe_div(
        Calc_Scored_B,
        Calc_Concede_A
    )


    Ratio_B = safe_div(
        G_B,
        C_A
    )


    Power_B = (
        safe_div(
            Ratio_B,
            Net_B
        )
        *
        SOT_B
    )



    # ======================
    # PHASE 3
    # ======================


    home_strength = (

        (xG_A + BC_A)/2

    ) * Power_A



    away_strength = (

        (xG_B + BC_B)/2

    ) * Power_B




    # ======================
    # PHASE 4 POISSON
    # ======================


    cap = 6


    home_matrix = [

        poisson.pmf(
            i,
            home_strength
        )

        for i in range(cap+1)

    ]



    away_matrix = [

        poisson.pmf(
            i,
            away_strength
        )

        for i in range(cap+1)

    ]



    grid = np.outer(
        home_matrix,
        away_matrix
    )



    home_prob = 0
    draw_prob = 0
    away_prob = 0



    for h in range(cap+1):

        for a in range(cap+1):

            if h > a:

                home_prob += grid[h][a]


            elif h == a:

                draw_prob += grid[h][a]


            else:

                away_prob += grid[h][a]



    total = (
        home_prob +
        draw_prob +
        away_prob
    )



    baseline = {

        "Home":home_prob/total,

        "Draw":draw_prob/total,

        "Away":away_prob/total

    }



    baseline_odds = {

        x:odd_converter(y)

        for x,y in baseline.items()

    }




    # ======================
    # PHASE 5 STRESS MATRIX
    # ======================


    sigma = 0.036


    states={}


    states["0"] = baseline



    def create_state(target):


        h = baseline["Home"]*100
        d = baseline["Draw"]*100
        a = baseline["Away"]*100


        if target=="Home":

            h += 50 - (100*sigma)


        if target=="Draw":

            d += 50 - (100*sigma)


        if target=="Away":

            a += 50 - (100*sigma)



        total=h+d+a


        return {

            "Home":h/total,
            "Draw":d/total,
            "Away":a/total

        }



    states["1"]=create_state("Home")

    states["2"]=create_state("Away")

    states["3"]=create_state("Draw")




    h = baseline["Home"]*100 + 50 -(100*sigma)

    d = baseline["Draw"]*100 + 50 -(100*sigma)

    a = baseline["Away"]*100 + 50 -(100*sigma)



    total=h+d+a


    states["4"]={

        "Home":h/total,

        "Draw":d/total,

        "Away":a/total

    }




    # ======================
    # DOMINANCE
    # ======================


    dominance={}



    for side in ["Home","Away"]:


        score=0


        for s in states:


            score += (

                states[s][side]

                -

                baseline[side]

            )


        dominance[side]=score




    # ======================
    # MASTER ODDS
    # ======================


    master_prob={}



    for outcome in [

        "Home",
        "Draw",
        "Away"

    ]:


        master_prob[outcome]=np.mean(

            [

                states[x][outcome]

                for x in states

            ]

        )



    master_odds={

        x:odd_converter(y)

        for x,y in master_prob.items()

    }




    # ======================
    # BOOK VALUE
    # ======================


    book_prob={

        "Home":1/book_home,

        "Draw":1/book_draw,

        "Away":1/book_away

    }



    value={


        x:

        master_prob[x]-book_prob[x]


        for x in master_prob

    }



    best=max(

        value,

        key=value.get

    )




    # ======================
    # MARKET CHECK
    # ======================


    expected_goals = (

        home_strength +

        away_strength

    )


    btts=(

        1-math.exp(-home_strength)

    )*(

        1-math.exp(-away_strength)

    )




    # ======================
    # CORRECT SCORES
    # ======================


    top=np.argsort(

        grid.flatten()

    )[::-1][:2]



    scores=[]


    for i in top:


        h,a=np.unravel_index(

            i,

            grid.shape

        )


        scores.append(

            f"{h}-{a}"

        )




    # ======================
    # OUTPUT
    # ======================


    st.header(

        f"{home_team} vs {away_team}"

    )



    st.subheader(
        "TEAM STRENGTH"
    )


    st.write(
        "Home Strength:",
        round(home_strength,2)
    )


    st.write(
        "Away Strength:",
        round(away_strength,2)
    )



    st.subheader(
        "BASELINE ODDS"
    )


    st.write(
        baseline_odds
    )



    st.subheader(
        "MASTER ODDS"
    )


    st.write(
        master_odds
    )



    st.subheader(
        "DOMINANCE"
    )


    st.write(
        dominance
    )



    st.subheader(
        "BOOKMAKER VALUE"
    )


    st.write(
        value
    )


    st.write(
        "Best Value:",
        best
    )



    st.subheader(
        "MARKET CHECK"
    )


    st.write(
        "BTTS Probability:",
        round(btts*100,2),
        "%"
    )


    st.write(
        "Expected Goals:",
        round(expected_goals,2)
    )



    st.subheader(
        "CORRECT SCORES"
    )


    st.write(scores)
