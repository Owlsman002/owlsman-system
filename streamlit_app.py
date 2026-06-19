import streamlit as st
import numpy as np
from scipy.stats import poisson

# ============================================================
# PASSWORD
# ============================================================

APP_PASSWORD = "OWLSNATION123"

st.set_page_config(
    page_title="OWLSNATION",
    layout="wide"
)

password = st.text_input(
    "Enter Password",
    type="password"
)

if password != APP_PASSWORD:
    st.stop()

st.title(" OWLSNATION ENGINE V1")

# ============================================================
# SAFE FUNCTIONS
# ============================================================

def safe_div(a, b):
    if b == 0:
        return 0
    return a / b

def prob_to_odds(p):
    if p <= 0:
        return 999
    return round(1 / p, 2)

# ============================================================
# INPUT SECTION
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("HOME TEAM")

    h_goals_scored = st.number_input(
        "Avg Goals Scored",
        value=2.0
    )

    h_goals_conceded = st.number_input(
        "Avg Goals Conceded",
        value=1.0
    )

    h_sot_for = st.number_input(
        "Avg Shots On Target For",
        value=5.0
    )

    h_sot_against = st.number_input(
        "Avg Shots On Target Against",
        value=3.0
    )

    h_xg = st.number_input(
        "Normalized xG",
        value=0.77
    )

    h_bc = st.number_input(
        "Normalized Big Chances",
        value=0.58
    )

with col2:
    st.subheader("AWAY TEAM")

    a_goals_scored = st.number_input(
        "Away Avg Goals Scored",
        value=3.0
    )

    a_goals_conceded = st.number_input(
        "Away Avg Goals Conceded",
        value=2.0
    )

    a_sot_for = st.number_input(
        "Away Avg Shots On Target For",
        value=2.0
    )

    a_sot_against = st.number_input(
        "Away Avg Shots On Target Against",
        value=8.0
    )

    a_xg = st.number_input(
        "Away Normalized xG",
        value=0.89
    )

    a_bc = st.number_input(
        "Away Normalized Big Chances",
        value=0.50
    )

st.divider()

# ============================================================
# BOOKMAKER ODDS
# ============================================================

st.subheader("Bookmaker Odds")

b1, b2, b3 = st.columns(3)

with b1:
    book_home = st.number_input(
        "Bookie Home",
        value=2.10
    )

with b2:
    book_draw = st.number_input(
        "Bookie Draw",
        value=3.30
    )

with b3:
    book_away = st.number_input(
        "Bookie Away",
        value=3.80
    )

# ============================================================
# RUN ENGINE
# ============================================================

if st.button("RUN OWLSNATION"):

    # ========================================================
    # PHASE 1
    # ========================================================

    h_score_pct = safe_div(
        h_goals_scored,
        h_sot_for
    ) * 100

    h_concede_pct = safe_div(
        h_goals_conceded,
        h_sot_against
    ) * 100

    a_score_pct = safe_div(
        a_goals_scored,
        a_sot_for
    ) * 100

    a_concede_pct = safe_div(
        a_goals_conceded,
        a_sot_against
    ) * 100

    def calc_metric(x):
        if x > 100:
            return 100 / x
        return (1 / x) * 100

    h_calc_score = calc_metric(h_score_pct)
    h_calc_concede = calc_metric(h_concede_pct)

    a_calc_score = calc_metric(a_score_pct)
    a_calc_concede = calc_metric(a_concede_pct)

    # ========================================================
    # PHASE 2
    # ========================================================

    h_net = safe_div(
        h_calc_score,
        a_calc_concede
    )

    a_net = safe_div(
        a_calc_score,
        h_calc_concede
    )

    h_ratio = safe_div(
        h_goals_scored,
        a_goals_conceded
    )

    a_ratio = safe_div(
        a_goals_scored,
        h_goals_conceded
    )

    h_score_power = (
        safe_div(h_ratio, h_net)
        * h_sot_for
    )

    a_score_power = (
        safe_div(a_ratio, a_net)
        * a_sot_for
    )

    # ========================================================
    # PHASE 3
    # ========================================================

    home_strength = (
        ((h_xg + h_bc) / 2)
        * h_score_power
    )

    away_strength = (
        ((a_xg + a_bc) / 2)
        * a_score_power
    )

    # ========================================================
    # PHASE 4
    # ========================================================

    MAX_GOALS = 6

    home_probs = [
        poisson.pmf(
            k,
            home_strength
        )
        for k in range(MAX_GOALS + 1)
    ]

    away_probs = [
        poisson.pmf(
            k,
            away_strength
        )
        for k in range(MAX_GOALS + 1)
    ]

    grid = np.outer(
        home_probs,
        away_probs
    )

    p_home = np.sum(
        np.tril(grid, -1)
    )

    p_draw = np.sum(
        np.diag(grid)
    )

    p_away = np.sum(
        np.triu(grid, 1)
    )

    total = (
        p_home +
        p_draw +
        p_away
    )

    p_home /= total
    p_draw /= total
    p_away /= total

    baseline_home = prob_to_odds(p_home)
    baseline_draw = prob_to_odds(p_draw)
    baseline_away = prob_to_odds(p_away)

    # ========================================================
    # CORRECT SCORES
    # ========================================================

    flat = grid.flatten()

    best = np.argsort(flat)[::-1][:2]

    scores = []

    for idx in best:
        h, a = np.unravel_index(
            idx,
            grid.shape
        )
        scores.append(
            f"{h}-{a}"
        )

    # ========================================================
    # PHASE 5
    # ========================================================

    sigma = 0.036

    states = {}

    states["0"] = {
        "H": p_home,
        "D": p_draw,
        "A": p_away
    }

    def stress(
        target,
        other1,
        other2
    ):
        boost = (
            target +
            0.50 -
            sigma
        )

        total = (
            boost +
            other1 +
            other2
        )

        return (
            boost / total,
            other1 / total,
            other2 / total
        )

    h1, d1, a1 = stress(
        p_home,
        p_draw,
        p_away
    )

    states["1"] = {
        "H": h1,
        "D": d1,
        "A": a1
    }

    a2, h2, d2 = stress(
        p_away,
        p_home,
        p_draw
    )

    states["2"] = {
        "H": h2,
        "D": d2,
        "A": a2
    }

    d3, h3, a3 = stress(
        p_draw,
        p_home,
        p_away
    )

    states["3"] = {
        "H": h3,
        "D": d3,
        "A": a3
    }

    h4 = p_home + 0.50 - sigma
    d4 = p_draw + 0.50 - sigma
    a4 = p_away + 0.50 - sigma

    t4 = h4 + d4 + a4

    states["4"] = {
        "H": h4 / t4,
        "D": d4 / t4,
        "A": a4 / t4
    }

    # ========================================================
    # DOMINANCE
    # ========================================================

    home_dom = sum(
        states[s]["H"] -
        states["0"]["H"]
        for s in states
    )

    away_dom = sum(
        states[s]["A"] -
        states["0"]["A"]
        for s in states
    )

    # ========================================================
    # BLENDED
    # ========================================================

    blend_home = np.mean(
        [states[s]["H"] for s in states]
    )

    blend_draw = np.mean(
        [states[s]["D"] for s in states]
    )

    blend_away = np.mean(
        [states[s]["A"] for s in states]
    )

    blended_home_odd = prob_to_odds(
        blend_home
    )

    blended_draw_odd = prob_to_odds(
        blend_draw
    )

    blended_away_odd = prob_to_odds(
        blend_away
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    st.subheader("PHASE 3")

    st.write(
        "Home Strength:",
        round(home_strength, 3)
    )

    st.write(
        "Away Strength:",
        round(away_strength, 3)
    )

    st.subheader("BASELINE ODDS")

    st.write(
        "Home:",
        baseline_home
    )

    st.write(
        "Draw:",
        baseline_draw
    )

    st.write(
        "Away:",
        baseline_away
    )

    st.subheader("BLENDED ODDS")

    st.write(
        "Home:",
        blended_home_odd
    )

    st.write(
        "Draw:",
        blended_draw_odd
    )

    st.write(
        "Away:",
        blended_away_odd
    )

    st.subheader("DOMINANCE")

    st.write(
        "Home Dominance:",
        round(home_dom, 4)
    )

    st.write(
        "Away Dominance:",
        round(away_dom, 4)
    )

    st.subheader("CORRECT SCORES")

    st.write(scores[0])
    st.write(scores[1])

    # ========================================================
    # PHASE 6 - MARKET DECISION ENGINE
    # ========================================================

    st.subheader("PHASE 6 - MARKET ANALYSIS")


    # ----------------------------
    # BOOKMAKER IMPLIED PROBABILITY
    # ----------------------------

    book_home_prob = 1 / book_home
    book_draw_prob = 1 / book_draw
    book_away_prob = 1 / book_away


    # ----------------------------
    # MODEL VALUE MARGINS
    # ----------------------------

    home_value = (
        blend_home -
        book_home_prob
    )

    draw_value = (
        blend_draw -
        book_draw_prob
    )

    away_value = (
        blend_away -
        book_away_prob
    )


    value_table = {
        "HOME": home_value,
        "DRAW": draw_value,
        "AWAY": away_value
    }


    best_side = max(
        value_table,
        key=value_table.get
    )


    best_value = value_table[best_side]


    st.write(
        "Best Value Side:",
        best_side
    )

    st.write(
        "Value Margin:",
        round(best_value * 100, 2),
        "%"
    )


    # ----------------------------
    # BTTS ENGINE
    # ----------------------------

    expected_goals = (
        home_strength +
        away_strength
    )


    btts_probability = (
        1 -
        np.exp(-home_strength)
        -
        np.exp(-away_strength)
        +
        np.exp(
            -(home_strength + away_strength)
        )
    )


    st.subheader("BTTS")

    st.write(
        "BTTS Probability:",
        round(
            btts_probability * 100,
            2
        ),
        "%"
    )


    if btts_probability > 0.55:
        st.success(
            "BTTS YES SUPPORT"
        )
    else:
        st.warning(
            "BTTS NOT STRONG"
        )


    # ----------------------------
    # TOTAL GOALS ENGINE
    # ----------------------------

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


    # ----------------------------
    # DOUBLE CHANCE ENGINE
    # ----------------------------

    st.subheader("DOUBLE CHANCE")


    if blend_home + blend_draw > 0.70:
        st.success(
            "1X DOUBLE CHANCE"
        )


    if blend_away + blend_draw > 0.70:
        st.success(
            "X2 DOUBLE CHANCE"
        )


    if blend_home + blend_away > 0.75:
        st.success(
            "12 DOUBLE CHANCE"
        )


    # ----------------------------
    # HANDICAP ENGINE
    # ----------------------------

    st.subheader("HANDICAP")


    if best_side == "HOME":
        if home_dom >= 0:
            st.success(
                "HOME HANDICAP SUPPORT"
            )
        else:
            st.warning(
                "FADE HOME HANDICAP - FRAGILE"
            )

    elif best_side == "AWAY":
        if away_dom >= 0:
            st.success(
                "AWAY HANDICAP SUPPORT"
            )
        else:
            st.warning(
                "FADE AWAY HANDICAP - FRAGILE"
            )

    else:
        st.info(
            "DRAW EDGE - Consider safer markets"
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    st.subheader(
        "OWLSNATION FINAL VERDICT"
    )


    st.write(
        "Baseline Odds:",
        {
            "Home": baseline_home,
            "Draw": baseline_draw,
            "Away": baseline_away
        }
    )


    st.write(
        "Master Odds:",
        {
            "Home": blended_home_odd,
            "Draw": blended_draw_odd,
            "Away": blended_away_odd
        }
    )


    st.write(
        "Bookmaker Odds:",
        {
            "Home": book_home,
            "Draw": book_draw,
            "Away": book_away
        }
    )


    st.write(
        "Predicted Correct Scores:"
    )

    st.write(scores[0])
    st.write(scores[1])
    
