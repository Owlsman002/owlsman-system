import streamlit as st
import numpy as np
from scipy.stats import poisson


# =====================================================
# APP SETTINGS
# =====================================================

st.set_page_config(
    page_title="OWLSNATION ENGINE",
    layout="wide"
)


st.title("🦉 OWLSNATION BETTING ENGINE")


# =====================================================
# INPUT SECTION
# =====================================================


st.sidebar.header("MATCH INPUT")


home_team = st.sidebar.text_input(
    "Home Team",
    "Team A"
)

away_team = st.sidebar.text_input(
    "Away Team",
    "Team B"
)


st.sidebar.subheader("HOME LAST 4 MATCHES")


home_goals = st.sidebar.number_input(
    "Average Goals Scored",
    value=2.0
)

home_conceded = st.sidebar.number_input(
    "Average Goals Conceded",
    value=4.0
)

home_sot_for = st.sidebar.number_input(
    "Average Shots On Target For",
    value=5.0
)

home_sot_against = st.sidebar.number_input(
    "Average Shots On Target Against",
    value=3.0
)

home_xg = st.sidebar.number_input(
    "Average xG",
    value=0.77
)

home_bc = st.sidebar.number_input(
    "Average Big Chances Scored",
    value=0.58
)



st.sidebar.subheader("AWAY LAST 4 MATCHES")


away_goals = st.sidebar.number_input(
    "Average Goals Scored",
    value=3.0
)

away_conceded = st.sidebar.number_input(
    "Average Goals Conceded",
    value=5.0
)

away_sot_for = st.sidebar.number_input(
    "Average Shots On Target For",
    value=2.0
)

away_sot_against = st.sidebar.number_input(
    "Average Shots On Target Against",
    value=8.0
)

away_xg = st.sidebar.number_input(
    "Average xG",
    value=0.89
)

away_bc = st.sidebar.number_input(
    "Average Big Chances Scored",
    value=0.50
)



st.sidebar.subheader("BOOKMAKER ODDS")


book_home = st.sidebar.number_input(
    "Home Odd",
    value=3.00
)

book_draw = st.sidebar.number_input(
    "Draw Odd",
    value=3.20
)

book_away = st.sidebar.number_input(
    "Away Odd",
    value=2.20
)




# =====================================================
# PHASE 1
# CALCULATED SCORED / CONCEDED
# =====================================================


def calculate_attack(goals, sot):

    if sot == 0:
        return 0

    percentage = (
        goals / sot
    ) * 100


    return (
        1 / percentage
    ) * 100




home_calc_scored = calculate_attack(
    home_goals,
    home_sot_for
)


home_calc_conceded = calculate_attack(
    home_conceded,
    home_sot_against
)



away_calc_scored = calculate_attack(
    away_goals,
    away_sot_for
)


away_calc_conceded = calculate_attack(
    away_conceded,
    away_sot_against
)




# =====================================================
# PHASE 2
# NET SCORE + SCORE POWER
# =====================================================


home_net_score = (

    home_calc_scored /

    away_calc_conceded

)



home_score_power = (

    (

        home_goals /

        away_conceded

    )

    /

    home_net_score

)

* home_sot_for




away_net_score = (

    away_calc_scored /

    home_calc_conceded

)



away_score_power = (

    (

        away_goals /

        home_conceded

    )

    /

    away_net_score

)

* away_sot_for





# =====================================================
# PHASE 3
# TEAM STRENGTH
# =====================================================


home_strength = (

    (

        home_xg +

        home_bc

    )

    /

    2

)

* home_score_power



away_strength = (

    (

        away_xg +

        away_bc

    )

    /

    2

)

* away_score_power





# =====================================================
# PHASE 4
# POISSON ODD 0
# =====================================================


def poisson_engine(home_lambda, away_lambda):


    cap = 6


    home_matrix = [

        poisson.pmf(i, home_lambda)

        for i in range(cap+1)

    ]


    away_matrix = [

        poisson.pmf(i, away_lambda)

        for i in range(cap+1)

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


    probabilities = {

        "Home": home_win/total,

        "Draw": draw/total,

        "Away": away_win/total

    }


    odds = {

        k:

        1/v

        for k,v in probabilities.items()

    }



    return grid, probabilities, odds





grid, baseline_prob, baseline_odds = poisson_engine(

    home_strength,

    away_strength

)





# =====================================================
# PHASE 5
# VARIANCE STRESS MATRIX
# =====================================================


def stress_matrix(base):


    drag = 100 * 0.036


    states={}



    states["Odd 0"] = base



    def create(target):


        h = base["Home"]*100

        d = base["Draw"]*100

        a = base["Away"]*100



        if target=="Home":

            h=(h+50)-drag


        if target=="Draw":

            d=(d+50)-drag


        if target=="Away":

            a=(a+50)-drag



        total=h+d+a



        return {


        "Home":h/total,

        "Draw":d/total,

        "Away":a/total

        }



    states["Odd 1"] = create("Home")

    states["Odd 2"] = create("Away")

    states["Odd 3"] = create("Draw")




    h=(base["Home"]*100+50)-drag

    d=(base["Draw"]*100+50)-drag

    a=(base["Away"]*100+50)-drag



    total=h+d+a


    states["Odd 4"]={


        "Home":h/total,

        "Draw":d/total,

        "Away":a/total

    }



    return states




states = stress_matrix(
    baseline_prob
)






# =====================================================
# DOMINANCE INDEX
# =====================================================


dominance={}


for team in ["Home","Away"]:


    score=0


    baseline = baseline_prob[team]


    for state in states.values():

        score += (

            state[team]

            -

            baseline

        )


    dominance[team]=score






# =====================================================
# MASTER ODDS
# =====================================================


master_prob={}



for outcome in ["Home","Draw","Away"]:


    master_prob[outcome]=np.mean(

        [

            states[x][outcome]

            for x in states

        ]

    )



master_odds={


x:

1/y

for x,y in master_prob.items()

}







# =====================================================
# BOOKMAKER VALUE
# =====================================================


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





# =====================================================
# CORRECT SCORES
# =====================================================


top = np.argsort(

    grid.flatten()

)[::-1][:2]



correct=[]


for i in top:


    h,a=np.unravel_index(

        i,

        grid.shape

    )


    correct.append(

        f"{h}-{a}"

    )






# =====================================================
# OUTPUT
# =====================================================


st.header(

f"{home_team} vs {away_team}"

)


st.write(
"Home Strength:",
round(home_strength,2)
)


st.write(
"Away Strength:",
round(away_strength,2)
)



st.subheader("BASELINE ODD 0")

st.write(baseline_odds)



st.subheader("MASTER ODDS")

st.write(master_odds)



st.subheader("DOMINANCE INDEX")

st.write(dominance)



st.subheader("BOOKMAKER VALUE GAP")

st.write(value)



st.subheader("TOP CORRECT SCORES")

st.write(correct)
