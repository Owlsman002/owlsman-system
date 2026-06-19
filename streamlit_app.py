# ============================================================
# PHASE 4
# POISSON DISTRIBUTION ENGINE
# ============================================================


def phase_four_poisson(home_strength, away_strength):


    MAX_SCORE_CAP = 6


    home_matrix = []

    away_matrix = []


    for k in range(MAX_SCORE_CAP + 1):

        home_matrix.append(
            poisson.pmf(
                k,
                home_strength
            )
        )


        away_matrix.append(
            poisson.pmf(
                k,
                away_strength
            )
        )



    score_grid = np.outer(
        home_matrix,
        away_matrix
    )



    home_probability = 0
    draw_probability = 0
    away_probability = 0



    for h in range(MAX_SCORE_CAP + 1):

        for a in range(MAX_SCORE_CAP + 1):


            if h > a:

                home_probability += score_grid[h][a]


            elif h == a:

                draw_probability += score_grid[h][a]


            elif a > h:

                away_probability += score_grid[h][a]



    total = (
        home_probability
        +
        draw_probability
        +
        away_probability
    )


    home_probability /= total
    draw_probability /= total
    away_probability /= total



    baseline_odds = {


        "home":

        1 / home_probability,


        "draw":

        1 / draw_probability,


        "away":

        1 / away_probability

    }



    return {


        "grid":score_grid,


        "probabilities":{


            "home":home_probability,

            "draw":draw_probability,

            "away":away_probability


        },


        "baseline_odds":baseline_odds


    }




# ============================================================
# PHASE 5
# 5 ODDS STRESS MATRIX
# ============================================================


def phase_five_stress(probabilities):


    home = probabilities["home"]
    draw = probabilities["draw"]
    away = probabilities["away"]



    sigma = 0.036


    drag = (
        100 * sigma
    )



    states = {}



    # Odd 0

    states["Odd 0"] = {


        "home":home,

        "draw":draw,

        "away":away

    }



    # Odd 1 Home stress


    h = (
        home * 100
        +
        50
        -
        drag
    )

    d = draw * 100

    a = away * 100


    total = h+d+a



    states["Odd 1"]={


        "home":h/total,

        "draw":d/total,

        "away":a/total

    }



    # Odd 2 Away stress


    h = home*100

    d = draw*100


    a = (

        away*100
        +
        50
        -
        drag

    )


    total=h+d+a



    states["Odd 2"]={


        "home":h/total,

        "draw":d/total,

        "away":a/total

    }




    # Odd 3 Draw stress


    h=home*100


    d=(

        draw*100

        +

        50

        -

        drag

    )


    a=away*100


    total=h+d+a



    states["Odd 3"]={


        "home":h/total,

        "draw":d/total,

        "away":a/total

    }




    # Odd 4 Chaos


    h=(home*100)+50-drag

    d=(draw*100)+50-drag

    a=(away*100)+50-drag


    total=h+d+a



    states["Odd 4"]={


        "home":h/total,

        "draw":d/total,

        "away":a/total

    }



    return states





# ============================================================
# DOMINANCE ENGINE
# ============================================================


def dominance_engine(states):


    baseline = states["Odd 0"]


    home_dom = 0
    away_dom = 0



    for state in states:


        home_dom += (

            states[state]["home"]

            -

            baseline["home"]

        )



        away_dom += (

            states[state]["away"]

            -

            baseline["away"]

        )



    return {


        "home":

        home_dom,


        "away":

        away_dom

    }




# ============================================================
# MASTER BLENDED ODDS
# ============================================================


def master_odds(states):


    home = np.mean(

        [

        states[x]["home"]

        for x in states

        ]

    )


    draw = np.mean(

        [

        states[x]["draw"]

        for x in states

        ]

    )


    away = np.mean(

        [

        states[x]["away"]

        for x in states

        ]

    )



    return {


        "probabilities":{


            "home":home,

            "draw":draw,

            "away":away


        },


        "odds":{


            "home":1/home,

            "draw":1/draw,

            "away":1/away


        }

    }




# ============================================================
# PHASE 6
# BOOKMAKER COMPARISON
# ============================================================


def market_engine(master, baseline, bookmaker):


    model_home = master["probabilities"]["home"]

    model_draw = master["probabilities"]["draw"]

    model_away = master["probabilities"]["away"]



    book_home = 1/bookmaker["home"]

    book_draw = 1/bookmaker["draw"]

    book_away = 1/bookmaker["away"]



    value = {


        "home":

        model_home-book_home,


        "draw":

        model_draw-book_draw,


        "away":

        model_away-book_away

    }



    best = max(

        value,

        key=value.get

    )



    return {


        "value_margin":value,


        "best_edge":best


    }





# ============================================================
# CORRECT SCORE ENGINE
# ============================================================


def correct_scores(grid):


    flat = grid.flatten()


    top_two = np.argsort(flat)[::-1][:2]


    results=[]



    for index in top_two:


        h,a=np.unravel_index(

            index,

            grid.shape

        )


        results.append(

            f"{h}-{a}"

        )


    return results





# ============================================================
# RUN FULL ENGINE
# ============================================================


poisson_result = phase_four_poisson(

    strength["home_strength"],

    strength["away_strength"]

)



stress = phase_five_stress(

    poisson_result["probabilities"]

)



dominance = dominance_engine(

    stress

)



master = master_odds(

    stress

)



# Example bookmaker odds

bookmaker = {


"home":1.80,

"draw":3.50,

"away":4.50

}



market = market_engine(

    master,

    poisson_result["baseline_odds"],

    bookmaker

)



scores = correct_scores(

    poisson_result["grid"]

)



print("BASELINE ODDS")

print(
    poisson_result["baseline_odds"]
)



print("MASTER ODDS")

print(
    master["odds"]
)



print("DOMINANCE")

print(
    dominance
)



print("VALUE")

print(
    market
)



print("CORRECT SCORES")

print(
    scores
)
