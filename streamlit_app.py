import streamlit as st
import numpy as np
from scipy.stats import poisson


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="OWLSNATION Betting Engine",
    layout="wide"
)


st.title("🦉 OWLSNATION Football Prediction Engine")


# ==========================================================
# MANUAL DATA INPUT
# ==========================================================


st.sidebar.header("TEAM INPUT")


home_team = st.sidebar.text_input(
    "Home Team",
    "Team A"
)

away_team = st.sidebar.text_input(
    "Away Team",
    "Team B"
)



st.sidebar.subheader("HOME LAST 4 MATCHES")


home_goals_scored = st.sidebar.number_input(
    "Home Avg Goals Scored",
    value=2.0
)

home_goals_conceded = st.sidebar.number_input(
    "Home Avg Goals Conceded",
    value=4.0
)


home_sot_for = st.sidebar.number_input(
    "Home Avg Shots On Target For",
    value=5.0
)


home_sot_against = st.sidebar.number_input(
    "Home Avg Shots On Target Against",
    value=3.0
)


home_xg = st.sidebar.number_input(
    "Home Avg xG",
    value=0.77
)


home_bc = st.sidebar.number_input(
    "Home Avg Big Chances Scored",
    value=0.58
)





st.sidebar.subheader("AWAY LAST 4 MATCHES")


away_goals_scored = st.sidebar.number_input(
    "Away Avg Goals Scored",
    value=3.0
)


away_goals_conceded = st.sidebar.number_input(
    "Away Avg Goals Conceded",
    value=5.0
)


away_sot_for = st.sidebar.number_input(
    "Away Avg Shots On Target For",
    value=2.0
)


away_sot_against = st.sidebar.number_input(
    "Away Avg Shots On Target Against",
    value=8.0
)


away_xg = st.sidebar.number_input(
    "Away Avg xG",
    value=0.89
)


away_bc = st.sidebar.number_input(
    "Away Avg Big Chances Scored",
    value=0.50
)





st.sidebar.subheader("BOOKMAKER ODDS")


book_home = st.sidebar.number_input(
    "Bookie Home Odd",
    value=1.80
)

book_draw = st.sidebar.number_input(
    "Bookie Draw Odd",
    value=3.50
)

book_away = st.sidebar.number_input(
    "Bookie Away Odd",
    value=4.50
)





# ==========================================================
# PHASE 1
# CALCULATED SCORED AND CONCEDED
# ==========================================================


def calculate_efficiency(goals, sot):


    result = (
        goals / sot
    ) * 100


    final = (
        1 / result
    ) * 100


    return final




home_calc_scored = calculate_efficiency(
    home_goals_scored,
    home_sot_for
)


home_calc_conceded = calculate_efficiency(
    home_goals_conceded,
    home_sot_against
)



away_calc_scored = calculate_efficiency(
    away_goals_scored,
    away_sot_for
)


away_calc_conceded = calculate_efficiency(
    away_goals_conceded,
    away_sot_against
)



# ==========================================================
# PHASE 2
# NET SCORE AND SCORE POWER
# ==========================================================



home_net_score = (

    home_calc_scored /

    away_calc_conceded

)



home_power = (

    (

    home_goals_scored /

    away_goals_conceded

    )

    /

    home_net_score

)

* home_sot_for





away_net_score = (

    away_calc_scored /

    home_calc_conceded

)



away_power = (

    (

    away_goals_scored /

    home_goals_conceded

    )

    /

    away_net_score

)

* away_sot_for





# ==========================================================
# PHASE 3
# TEAM STRENGTH
# ==========================================================



home_strength = (

    (

    home_xg +

    home_bc

    )

    /

    2

)

* home_power




away_strength = (

    (

    away_xg +

    away_bc

    )

    /

    2

)

* away_power





# ==========================================================
# PHASE 4
# POISSON MATRIX
# ==========================================================



def poisson_engine(home_strength, away_strength):


    cap = 6


    home_matrix = [

        poisson.pmf(x, home_strength)

        for x in range(cap+1)

    ]


    away_matrix = [

        poisson.pmf(x, away_strength)

        for x in range(cap+1)

    ]



    grid = np.outer(

        home_matrix,

        away_matrix

    )



    home_win = 0

    draw = 0

    away_win = 0



    for h in range(cap+1):

        for a in range(cap+1):


            if h > a:

                home_win += grid[h][a]


            elif h == a:

                draw += grid[h][a]


            else:

                away_win += grid[h][a]



    total = home_win + draw + away_win


    probs = {


        "home":home_win/total,

        "draw":draw/total,

        "away":away_win/total

    }



    odds = {


        "home":1/probs["home"],

        "draw":1/probs["draw"],

        "away":1/probs["away"]

    }



    return grid, probs, odds





grid, baseline_prob, baseline_odds = poisson_engine(

    home_strength,

    away_strength

)






# ==========================================================
# PHASE 5
# VARIANCE DRAG
# ==========================================================


def stress_matrix(prob):


    sigma = 0.036


    drag = sigma


    states = {}



    states["Odd 0"] = prob



    def stress(target):


        h = prob["home"]

        d = prob["draw"]

        a = prob["away"]


        if target=="home":

            h +=0.50

            h-=drag


        if target=="draw":

            d+=0.50

            d-=drag


        if target=="away":

            a+=0.50

            a-=drag



        total=h+d+a


        return {


        "home":h/total,

        "draw":d/total,

        "away":a/total

        }





    states["Odd 1"]=stress("home")

    states["Odd 2"]=stress("away")

    states["Odd 3"]=stress("draw")



    states["Odd 4"]={


        "home":(prob["home"]+0.50-drag)/

        (sum(prob.values())+1.50-(drag*3)),


        "draw":(prob["draw"]+0.50-drag)/

        (sum(prob.values())+1.50-(drag*3)),


        "away":(prob["away"]+0.50-drag)/

        (sum(prob.values())+1.50-(drag*3))


    }



    return states





states = stress_matrix(

    baseline_prob

)






# ==========================================================
# MASTER ODDS
# ==========================================================



master_prob = {


"home":

np.mean(

[states[x]["home"] for x in states]

),


"draw":

np.mean(

[states[x]["draw"] for x in states]

),


"away":

np.mean(

[states[x]["away"] for x in states]

)


}





master_odds={


x:

1/master_prob[x]

for x in master_prob

}






# ==========================================================
# PHASE 6
# VALUE AND DECISION
# ==========================================================


book_prob={


"home":1/book_home,

"draw":1/book_draw,

"away":1/book_away


}



value={


x:

master_prob[x]-book_prob[x]

for x in master_prob

}



best_market=max(

value,

key=value.get

)






# ==========================================================
# CORRECT SCORES
# ==========================================================


flat = grid.flatten()


top = np.argsort(flat)[::-1][:2]


scores=[]


for i in top:

    h,a=np.unravel_index(

        i,

        grid.shape

    )


    scores.append(

        f"{h}-{a}"

    )






# ==========================================================
# OUTPUT
# ==========================================================


st.subheader(
f"{home_team} vs {away_team}"
)


col1,col2,col3=st.columns(3)


with col1:

    st.write("TEAM STRENGTH")

    st.write(
        "Home:",
        round(home_strength,2)
    )

    st.write(
        "Away:",
        round(away_strength,2)
    )



with col2:

    st.write("BASELINE ODD 0")

    st.write(baseline_odds)



with col3:

    st.write("MASTER ODDS")

    st.write(master_odds)



st.subheader("VALUE EDGE")

st.write(value)


st.success(

f"Model prefers: {best_market}"

)



st.subheader("Correct Scores")

st.write(scores)
