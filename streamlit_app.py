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
    "Home Average Shots On Target For",
    value=5.0
)


SOTA_A = st.number_input(
    "Home Average Shots On Target Against",
    value=3.0
)


xG_A = st.number_input(
    "Home Normalized xG",
    value=0.77
)


BC_A = st.number_input(
    "Home Normalized Big Chances",
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
    "Away Average Shots On Target For",
    value=2.0
)


SOTA_B = st.number_input(
    "Away Average Shots On Target Against",
    value=8.0
)


xG_B = st.number_input(
    "Away Normalized xG",
    value=0.89
)


BC_B = st.number_input(
    "Away Normalized Big Chances",
    value=0.50
)




st.header("BOOKMAKER ODDS")


BOOK_HOME = st.number_input(
    "Bookmaker Home Odd",
    value=3.00
)


BOOK_DRAW = st.number_input(
    "Bookmaker Draw Odd",
    value=3.20
)


BOOK_AWAY = st.number_input(
    "Bookmaker Away Odd",
    value=2.20
)




# ==========================
# RUN MODEL
# ==========================


if st.button("RUN MODEL"):



    # ======================
    # PHASE 1
    # EFFICIENCY
    # ======================


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





    # ======================
    # PHASE 2
    # NET + POWER
    # ======================



    Net_A = (

        Calc_Scored_A /

        Calc_Concede_B

    )



    Ratio_A = (

        G_A /

        C_B

    )



    Power_A = (

        Ratio_A /

        Net_A

    ) * SOT_A





    Net_B = (

        Calc_Scored_B /

        Calc_Concede_A

    )



    Ratio_B = (

        G_B /

        C_A

    )



    Power_B = (

        Ratio_B /

        Net_B

    ) * SOT_B




    # ======================
    # PHASE 3
    # FINAL STRENGTH
    # ======================



    alpha = (

        (xG_A + BC_A)

        /

        2

    ) * Power_A



    beta = (

        (xG_B + BC_B)

        /

        2

    ) * Power_B





    # ======================
    # PHASE 4
    # POISSON MATRIX
    # ======================


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



    base = {


        "Home":P_Home_Base/total,

        "Draw":P_Draw_Base/total,

        "Away":P_Away_Base/total


    }





    # ======================
    # PHASE 5
    # VARIANCE DRAG
    # ======================


    sigma = 0.036


    states={}



    states["0"]=base




    def stress_state(target):


        h = base["Home"]*100

        d = base["Draw"]*100

        a = base["Away"]*100



        if target=="Home":

            h=(h+50)-3.6



        if target=="Away":

            a=(a+50)-3.6



        if target=="Draw":

            d=(d+50)-3.6




        total=h+d+a



        return {


            "Home":h/total,

            "Draw":d/total,

            "Away":a/total


        }




    states["1"]=stress_state("Home")

    states["2"]=stress_state("Away")

    states["3"]=stress_state("Draw")




    h=(base["Home"]*100+50)-3.6

    d=(base["Draw"]*100+50)-3.6

    a=(base["Away"]*100+50)-3.6



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


        for state in states.values():


            score += (

                state[side]

                -

                base[side]

            )


        dominance[side]=score





    # ======================
    # MASTER BLEND
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
    # MARKET VALUE
    # ======================


    bookmaker_prob={


        "Home":1/BOOK_HOME,

        "Draw":1/BOOK_DRAW,

        "Away":1/BOOK_AWAY


    }




    value_margin={


        x:

        master_prob[x]-bookmaker_prob[x]


        for x in master_prob


    }




    best_side=max(

        value_margin,

        key=value_margin.get

    )





    # ======================
    # MARKET FILTERS
    # ======================



    expected_goals = alpha + beta



    btts_probability=(

        1-math.exp(-alpha)

    )*(

        1-math.exp(-beta)

    )





    # ======================
    # CORRECT SCORES
    # ======================


    top_scores=np.argsort(

        grid.flatten()

    )[::-1][:2]



    scores=[]



    for index in top_scores:


        h,a=np.unravel_index(

            index,

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

        "Home":odd_converter(base["Home"]),

        "Draw":odd_converter(base["Draw"]),

        "Away":odd_converter(base["Away"])

    })




    st.subheader("MASTER ODDS")


    st.write(master_odds)




    st.subheader("DOMINANCE INDEX")


    st.write(dominance)




    st.subheader("VALUE MARGIN")


    st.write(value_margin)



    st.write(
        "Best Value Side:",
        best_side
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




    st.subheader("TOP CORRECT SCORES")


    st.write(scores)
