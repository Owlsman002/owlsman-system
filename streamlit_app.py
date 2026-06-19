import streamlit as st
import numpy as np
from scipy.stats import poisson
import math


# =====================================================
# APP SETTINGS
# =====================================================

st.set_page_config(
    page_title="OWLSNATION ENGINE V2",
    layout="wide"
)


st.title("🦉 OWLSNATION ENGINE V2")


# =====================================================
# SAFE FUNCTIONS
# =====================================================

def safe_div(a,b):
    if b == 0:
        return 0
    return a/b


def odds(prob):
    if prob <= 0:
        return 999
    return round(1/prob,2)



# =====================================================
# INPUTS
# =====================================================

st.sidebar.header("MATCH INPUT")


home = st.sidebar.text_input(
    "Home Team",
    "Team A"
)


away = st.sidebar.text_input(
    "Away Team",
    "Team B"
)



st.sidebar.subheader("HOME DATA")


G_A = st.sidebar.number_input(
    "Goals Scored",
    value=2.0
)

C_A = st.sidebar.number_input(
    "Goals Conceded",
    value=4.0
)

SOT_A = st.sidebar.number_input(
    "Shots On Target For",
    value=5.0
)

SOTA_A = st.sidebar.number_input(
    "Shots On Target Against",
    value=3.0
)

xG_A = st.sidebar.number_input(
    "xG",
    value=0.77
)

BC_A = st.sidebar.number_input(
    "Big Chances",
    value=0.58
)




st.sidebar.subheader("AWAY DATA")


G_B = st.sidebar.number_input(
    "Away Goals Scored",
    value=3.0
)

C_B = st.sidebar.number_input(
    "Away Goals Conceded",
    value=5.0
)

SOT_B = st.sidebar.number_input(
    "Away Shots On Target For",
    value=2.0
)

SOTA_B = st.sidebar.number_input(
    "Away Shots On Target Against",
    value=8.0
)

xG_B = st.sidebar.number_input(
    "Away xG",
    value=0.89
)

BC_B = st.sidebar.number_input(
    "Away Big Chances",
    value=0.50
)



st.sidebar.subheader("BOOKMAKER")


BOOK_HOME = st.sidebar.number_input(
    "Home Odd",
    value=3.00
)

BOOK_DRAW = st.sidebar.number_input(
    "Draw Odd",
    value=3.20
)

BOOK_AWAY = st.sidebar.number_input(
    "Away Odd",
    value=2.20
)




if st.button("RUN ENGINE"):



# =====================================================
# PHASE 1
# =====================================================


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



# =====================================================
# PHASE 2
# =====================================================


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



# =====================================================
# PHASE 3
# =====================================================


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



# =====================================================
# PHASE 4 POISSON
# =====================================================


    cap = 6


    home_matrix = [

        poisson.pmf(i,alpha)

        for i in range(cap+1)

    ]


    away_matrix = [

        poisson.pmf(i,beta)

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


            if h>a:

                home_prob += grid[h][a]


            elif h==a:

                draw_prob += grid[h][a]


            else:

                away_prob += grid[h][a]



    total = (
        home_prob+
        draw_prob+
        away_prob
    )


    base = {

        "Home":home_prob/total,

        "Draw":draw_prob/total,

        "Away":away_prob/total

    }



# =====================================================
# PHASE 5 VARIANCE STATES
# =====================================================


    sigma = 0.036

    drag = 100*sigma


    states={}


    states["0"]=base



    def stress(target):

        h = base["Home"]*100
        d = base["Draw"]*100
        a = base["Away"]*100


        if target=="Home":
            h = h+50-drag

        if target=="Draw":
            d = d+50-drag

        if target=="Away":
            a = a+50-drag



        total=h+d+a


        return {

            "Home":h/total,

            "Draw":d/total,

            "Away":a/total

        }



    states["1"]=stress("Home")

    states["2"]=stress("Away")

    states["3"]=stress("Draw")



    h=base["Home"]*100+50-drag
    d=base["Draw"]*100+50-drag
    a=base["Away"]*100+50-drag


    total=h+d+a


    states["4"]={

        "Home":h/total,

        "Draw":d/total,

        "Away":a/total

    }



# =====================================================
# DOMINANCE
# =====================================================


    dominance={}


    for side in ["Home","Away"]:

        score=0


        for s in states:

            score += (
                states[s][side]
                -
                base[side]
            )


        dominance[side]=score




# =====================================================
# MASTER ODDS
# =====================================================


    master_prob={}


    for x in ["Home","Draw","Away"]:

        master_prob[x]=np.mean(

            [

                states[s][x]

                for s in states

            ]

        )


    master_odds={

        x:odds(master_prob[x])

        for x in master_prob

    }




# =====================================================
# MARKET TREE
# =====================================================


    book_prob={

        "Home":1/BOOK_HOME,

        "Draw":1/BOOK_DRAW,

        "Away":1/BOOK_AWAY

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



    expected_goals = alpha+beta


    btts=(

        1-math.exp(-alpha)

    )*(

        1-math.exp(-beta)

    )




# =====================================================
# CORRECT SCORES
# =====================================================


    indexes=np.argsort(
        grid.flatten()
    )[::-1][:2]


    scores=[]


    for i in indexes:

        h,a=np.unravel_index(
            i,
            grid.shape
        )

        scores.append(
            f"{h}-{a}"
        )




# =====================================================
# OUTPUT
# =====================================================


    st.header(
        f"{home} vs {away}"
    )


    st.subheader("STRENGTH")

    st.write(
        "Home Strength:",
        round(alpha,2)
    )


    st.write(
        "Away Strength:",
        round(beta,2)
    )



    st.subheader("BASELINE ODD 0")

    st.write({

        "Home":odds(base["Home"]),

        "Draw":odds(base["Draw"]),

        "Away":odds(base["Away"])

    })



    st.subheader("MASTER ODDS")

    st.write(master_odds)



    st.subheader("DOMINANCE")

    st.write(dominance)



    st.subheader("VALUE EDGE")

    st.write(value)

    st.write(
        "Best Value:",
        best
    )



    st.subheader("MARKET CHECK")

    st.write(
        "BTTS Probability:",
        round(btts*100,2),
        "%"
    )


    st.write(
        "Expected Goals:",
        round(expected_goals,2)
    )



    if expected_goals >= 2.8:

        st.success(
            "HIGH SCORING SIGNAL"
        )

    elif expected_goals <=2:

        st.success(
            "LOW SCORING SIGNAL"
        )

    else:

        st.info(
            "NORMAL GOAL ENVIRONMENT"
        )



    st.subheader("CORRECT SCORES")

    st.write(scores)
