import streamlit as st
import numpy as np
from scipy.stats import poisson
import math


# =====================================================
# APP SETTINGS
# =====================================================

st.set_page_config(
    page_title="OWLSNATION ENGINE V1",
    layout="wide"
)


st.title("🦉 OWLSNATION BETTING ENGINE V1")



# =====================================================
# SAFE FUNCTIONS
# =====================================================

def safe_div(a,b):

    if b == 0:
        return 0

    return a / b



def odd_converter(prob):

    if prob <= 0:
        return 999

    return round(1/prob,2)



# =====================================================
# MANUAL INPUT
# =====================================================


home_team = st.text_input(
    "Home Team",
    "Team A"
)


away_team = st.text_input(
    "Away Team",
    "Team B"
)



st.header("HOME DATA")


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




st.header("AWAY DATA")


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


BOOK_HOME = st.number_input(
    "Book Home Odd",
    value=3.00
)


BOOK_DRAW = st.number_input(
    "Book Draw Odd",
    value=3.20
)


BOOK_AWAY = st.number_input(
    "Book Away Odd",
    value=2.20
)




# =====================================================
# RUN ENGINE
# =====================================================


if st.button("RUN MODEL"):



    # =================================================
    # PHASE 1
    # EFFICIENCY CONVERSION
    # =================================================


    Pct_Scored_A = (
        G_A / SOT_A
    ) * 100


    Calc_Scored_A = (
        1 / Pct_Scored_A
    ) * 100



    Pct_Concede_A = (
        C_A / SOTA_A
    ) * 100


    Calc_Concede_A = (
        1 / Pct_Concede_A
    ) * 100




    Pct_Scored_B = (
        G_B / SOT_B
    ) * 100


    Calc_Scored_B = (
        1 / Pct_Scored_B
    ) * 100



    Pct_Concede_B = (
        C_B / SOTA_B
    ) * 100


    Calc_Concede_B = (
        1 / Pct_Concede_B
    ) * 100





    # =================================================
    # PHASE 2
    # NET + POWER
    # =================================================


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




    # =================================================
    # PHASE 3
    # FINAL STRENGTH
    # =================================================


    alpha = (

        safe_div(
            xG_A + BC_A,
            2
        )

        *

        Power_A

    )



    beta = (

        safe_div(
            xG_B + BC_B,
            2
        )

        *

        Power_B

    )





    # =================================================
    # PHASE 4
    # POISSON MATRIX
    # =================================================


    MAX_SCORE_CAP = 6



    home_distribution = [

        poisson.pmf(
            i,
            alpha
        )

        for i in range(MAX_SCORE_CAP+1)

    ]



    away_distribution = [

        poisson.pmf(
            i,
            beta
        )

        for i in range(MAX_SCORE_CAP+1)

    ]



    grid = np.outer(

        home_distribution,

        away_distribution

    )




    P_Home_Base = 0
    P_Draw_Base = 0
    P_Away_Base = 0



    for h in range(MAX_SCORE_CAP+1):

        for a in range(MAX_SCORE_CAP+1):


            if h > a:

                P_Home_Base += grid[h][a]


            elif h == a:

                P_Draw_Base += grid[h][a]


            else:

                P_Away_Base += grid[h][a]





    total = (

        P_Home_Base +

        P_Draw_Base +

        P_Away_Base

    )



    P_Home_Base /= total
    P_Draw_Base /= total
    P_Away_Base /= total



    baseline = {

        "Home":P_Home_Base,

        "Draw":P_Draw_Base,

        "Away":P_Away_Base

    }




    # =================================================
    # PHASE 5
    # VARIANCE DRAG
    # =================================================


    sigma = 0.036


    drag = 100 * sigma



    states = {}



    states["0"] = baseline




    def create_state(target):


        h = P_Home_Base * 100
        d = P_Draw_Base * 100
        a = P_Away_Base * 100



        if target == "Home":

            h = (h + 50) - drag


        if target == "Draw":

            d = (d + 50) - drag


        if target == "Away":

            a = (a + 50) - drag



        total = h+d+a



        return {

            "Home":h/total,

            "Draw":d/total,

            "Away":a/total

        }





    states["1"] = create_state("Home")

    states["2"] = create_state("Away")

    states["3"] = create_state("Draw")





    h = (P_Home_Base*100)+50-drag

    d = (P_Draw_Base*100)+50-drag

    a = (P_Away_Base*100)+50-drag



    total = h+d+a



    states["4"] = {

        "Home":h/total,

        "Draw":d/total,

        "Away":a/total

    }






    # =================================================
    # DOMINANCE
    # =================================================


    dominance = {}



    for side in ["Home","Away"]:


        score = 0



        for state in states.values():


            score += (

                state[side]

                -

                baseline[side]

            )


        dominance[side] = score





    # =================================================
    # MASTER BLENDED ODDS
    # =================================================


    master_probability = {}



    for outcome in [
        "Home",
        "Draw",
        "Away"
    ]:


        master_probability[outcome] = np.mean(

            [

                states[x][outcome]

                for x in states

            ]

        )




    master_odds = {


        x:

        odd_converter(
            y
        )

        for x,y in master_probability.items()

    }





    # =================================================
    # MARKET TREE
    # =================================================



    bookmaker_probability = {


        "Home":1/BOOK_HOME,

        "Draw":1/BOOK_DRAW,

        "Away":1/BOOK_AWAY

    }




    value_margin = {


        x:

        master_probability[x]

        -

        bookmaker_probability[x]


        for x in master_probability

    }




    best_value = max(

        value_margin,

        key=value_margin.get

    )




    expected_goals = alpha + beta



    btts_probability = (

        1 - math.exp(-alpha)

    ) * (

        1 - math.exp(-beta)

    )





    # =================================================
    # CORRECT SCORES
    # =================================================


    highest = np.argsort(

        grid.flatten()

    )[::-1][:2]



    scores = []



    for i in highest:


        h,a = np.unravel_index(

            i,

            grid.shape

        )


        scores.append(

            f"{h}-{a}"

        )





    # =================================================
    # OUTPUT
    # =================================================


    st.header(

        f"{home_team} vs {away_team}"

    )



    st.subheader("FINAL STRENGTH")


    st.write(
        "Home Alpha:",
        round(alpha,2)
    )


    st.write(
        "Away Beta:",
        round(beta,2)
    )




    st.subheader("BASELINE ODDS")


    st.write({

        "Home":

        odd_converter(P_Home_Base),

        "Draw":

        odd_converter(P_Draw_Base),

        "Away":

        odd_converter(P_Away_Base)

    })





    st.subheader("MASTER BLENDED ODDS")


    st.write(master_odds)




    st.subheader("DOMINANCE INDEX")


    st.write(dominance)



    st.subheader("VALUE MARGIN")


    st.write(value_margin)


    st.write(
        "Best Value Edge:",
        best_value
    )




    st.subheader("MARKET CHECK")



    st.write(

        "BTTS Probability:",

        round(
            btts_probability*100,
            2
        ),

        "%"

    )



    st.write(

        "Expected Goals:",

        round(
            expected_goals,
            2
        )

    )



    if btts_probability > 0.55:

        st.success(
            "BTTS YES SUPPORT"
        )

    else:

        st.warning(
            "BTTS NOT STRONG"
        )




    if expected_goals >= 2.8:

        st.success(
            "HIGH SCORING MATCH SIGNAL"
        )


    elif expected_goals <= 2.0:

        st.success(
            "LOW SCORING MATCH SIGNAL"
        )


    else:

        st.info(
            "NORMAL GOAL ENVIRONMENT"
        )




    st.subheader("CORRECT SCORES")


    st.write(scores)
