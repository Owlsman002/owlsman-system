import streamlit as st
import numpy as np
from scipy.stats import poisson


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



def calculate_metric(value):

    if value == 0:
        return 0

    if value > 100:
        return 100/value

    return (1/value)*100



def odd_converter(prob):

    if prob == 0:
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


home_goals = st.number_input(
    "Home Average Goals Scored",
    value=2.0
)


home_conceded = st.number_input(
    "Home Average Goals Conceded",
    value=4.0
)


home_sot_for = st.number_input(
    "Home Shots On Target For",
    value=5.0
)


home_sot_against = st.number_input(
    "Home Shots On Target Against",
    value=3.0
)


home_xg = st.number_input(
    "Home xG",
    value=0.77
)


home_bc = st.number_input(
    "Home Big Chances Scored",
    value=0.58
)




st.header("AWAY LAST 4 MATCHES")


away_goals = st.number_input(
    "Away Average Goals Scored",
    value=3.0
)


away_conceded = st.number_input(
    "Away Average Goals Conceded",
    value=5.0
)


away_sot_for = st.number_input(
    "Away Shots On Target For",
    value=2.0
)


away_sot_against = st.number_input(
    "Away Shots On Target Against",
    value=8.0
)


away_xg = st.number_input(
    "Away xG",
    value=0.89
)


away_bc = st.number_input(
    "Away Big Chances Scored",
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


    home_scored_percent = (
        home_goals/home_sot_for
    )*100


    home_conceded_percent = (
        home_conceded/home_sot_against
    )*100



    away_scored_percent = (
        away_goals/away_sot_for
    )*100


    away_conceded_percent = (
        away_conceded/away_sot_against
    )*100




    home_calc_scored = calculate_metric(
        home_scored_percent
    )


    home_calc_conceded = calculate_metric(
        home_conceded_percent
    )



    away_calc_scored = calculate_metric(
        away_scored_percent
    )


    away_calc_conceded = calculate_metric(
        away_conceded_percent
    )



    # ======================
    # PHASE 2
    # ======================


    home_net = safe_div(
        home_calc_scored,
        away_calc_conceded
    )


    away_net = safe_div(
        away_calc_scored,
        home_calc_conceded
    )



    home_ratio = safe_div(
        home_goals,
        away_conceded
    )


    away_ratio = safe_div(
        away_goals,
        home_conceded
    )



    home_power = (
        safe_div(
            home_ratio,
            home_net
        )
        *
        home_sot_for
    )



    away_power = (
        safe_div(
            away_ratio,
            away_net
        )
        *
        away_sot_for
    )




    # ======================
    # PHASE 3
    # ======================


    home_strength = (
        (home_xg + home_bc)/2
    ) * home_power



    away_strength = (
        (away_xg + away_bc)/2
    ) * away_power




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


    grid = grid/grid.sum()



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




    baseline = {

        "Home":home_prob,
        "Draw":draw_prob,
        "Away":away_prob

    }




    baseline_odds = {

        x:odd_converter(y)

        for x,y in baseline.items()

    }




    # ======================
    # PHASE 5 STRESS
    # ======================


    sigma = 0.036


    states={}


    states["Odd 0"]=baseline



    def create_state(target):


        h = baseline["Home"]
        d = baseline["Draw"]
        a = baseline["Away"]



        if target=="Home":

            h=(h+0.50)-sigma


        if target=="Draw":

            d=(d+0.50)-sigma


        if target=="Away":

            a=(a+0.50)-sigma



        total=h+d+a


        return {

            "Home":h/total,
            "Draw":d/total,
            "Away":a/total

        }



    states["Odd 1"]=create_state("Home")
    states["Odd 2"]=create_state("Away")
    states["Odd 3"]=create_state("Draw")



    h=(home_prob+0.50)-sigma
    d=(draw_prob+0.50)-sigma
    a=(away_prob+0.50)-sigma


    total=h+d+a


    states["Odd 4"]={

        "Home":h/total,
        "Draw":d/total,
        "Away":a/total

    }





    # ======================
    # DOMINANCE
    # ======================


    dominance={}


    for team in ["Home","Away"]:


        score=0


        for state in states.values():


            score += (
                state[team]
                -
                baseline[team]
            )


        dominance[team]=score




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




    # ======================
    # CORRECT SCORES
    # ======================


    best=np.argsort(

        grid.flatten()

    )[::-1][:2]


    scores=[]


    for x in best:


        h,a=np.unravel_index(

            x,

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


    st.write(
        "Home Strength",
        round(home_strength,2)
    )


    st.write(
        "Away Strength",
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



    st.subheader(
        "CORRECT SCORES"
    )

    st.write(scores)
