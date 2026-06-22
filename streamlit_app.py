import streamlit as st
from owlsnation_engine import TeamStats, run_engine

st.set_page_config(
    page_title="OWLSNATION Engine",
    page_icon="🦉",
    layout="wide"
)

st.title("🦉 OWLSNATION Engine")

st.caption(
    "Strength → Poisson Baseline → 5-State Stress Matrix → "
    "Dominance Index → 3-Way Draw Comparison → Markets & Correct Scores"
)

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Home — Team A")

    name_a = st.text_input(
        "Team name",
        value="Team A",
        key="name_a"
    )

    ga = st.number_input(
        "Avg Goals Scored",
        min_value=0.0,
        value=2.0,
        step=0.01,
        key="ga"
    )

    ca = st.number_input(
        "Avg Goals Conceded",
        min_value=0.0,
        value=4.0,
        step=0.01,
        key="ca"
    )

    sota = st.number_input(
        "Shots on Target For",
        min_value=0.0,
        value=5.0,
        step=0.01,
        key="sota"
    )

    sotaga = st.number_input(
        "Shots on Target Against",
        min_value=0.0,
        value=3.0,
        step=0.01,
        key="sotaga"
    )

    bca = st.number_input(
        "Avg Big Chances",
        min_value=0.0,
        value=0.58,
        step=0.01,
        key="bca"
    )

    xga = st.number_input(
        "Avg Expected Goals (xG)",
        min_value=0.0,
        value=0.77,
        step=0.01,
        key="xga"
    )

with col_b:
    st.subheader("Away — Team B")

    name_b = st.text_input(
        "Team name",
        value="Team B",
        key="name_b"
    )

    gb = st.number_input(
        "Avg Goals Scored",
        min_value=0.0,
        value=3.0,
        step=0.01,
        key="gb"
    )

    cb = st.number_input(
        "Avg Goals Conceded",
        min_value=0.0,
        value=5.0,
        step=0.01,
        key="cb"
    )

    sotb = st.number_input(
        "Shots on Target For",
        min_value=0.0,
        value=2.0,
        step=0.01,
        key="sotb"
    )

    sotbga = st.number_input(
        "Shots on Target Against",
        min_value=0.0,
        value=8.0,
        step=0.01,
        key="sotbga"
    )

    bcb = st.number_input(
        "Avg Big Chances",
        min_value=0.0,
        value=0.50,
        step=0.01,
        key="bcb"
    )

    xgb = st.number_input(
        "Avg Expected Goals (xG)",
        min_value=0.0,
        value=0.89,
        step=0.01,
        key="xgb"
    )

st.divider()

st.subheader("Bookmaker Decimal Odds")

bk_col1, bk_col2, bk_col3 = st.columns(3)

with bk_col1:
    bk_home = st.number_input(
        f"{name_a} Win Odd",
        min_value=1.01,
        value=3.40,
        step=0.01,
        key="bk_home"
    )

with bk_col2:
    bk_draw = st.number_input(
        "Draw Odd",
        min_value=1.01,
        value=3.40,
        step=0.01,
        key="bk_draw"
    )

with bk_col3:
    bk_away = st.number_input(
        f"{name_b} Win Odd",
        min_value=1.01,
        value=2.10,
        step=0.01,
        key="bk_away"
    )

st.divider()

run_clicked = st.button(
    "RUN ENGINE",
    type="primary",
    use_container_width=True
)

if run_clicked:

    inputs = {
        "Team A Goals Scored": ga,
        "Team A Goals Conceded": ca,
        "Team A Shots on Target For": sota,
        "Team A Shots on Target Against": sotaga,
        "Team A Big Chances": bca,
        "Team A xG": xga,
        "Team B Goals Scored": gb,
        "Team B Goals Conceded": cb,
        "Team B Shots on Target For": sotb,
        "Team B Shots on Target Against": sotbga,
        "Team B Big Chances": bcb,
        "Team B xG": xgb,
    }

    zero_fields = [
        k for k, v in inputs.items()
        if v <= 0
    ]

    if zero_fields:

        st.error(
            "Every stat field must be greater than 0. Check: "
            + ", ".join(zero_fields)
        )

    else:

        team_a = TeamStats(
            name=name_a or "Team A",
            goals_scored=ga,
            goals_conceded=ca,
            shots_on_target_for=sota,
            shots_on_target_against=sotaga,
            big_chances=bca,
            expected_goals=xga
        )

        team_b = TeamStats(
            name=name_b or "Team B",
            goals_scored=gb,
            goals_conceded=cb,
            shots_on_target_for=sotb,
            shots_on_target_against=sotbga,
            big_chances=bcb,
            expected_goals=xgb
        )

        result = run_engine(
            team_a,
            team_b,
            bk_home,
            bk_draw,
            bk_away
        )

        st.success("Engine run complete.")

        st.subheader("Final Team Strength")

        s1, s2 = st.columns(2)

        s1.metric(team_a.name, result.strength_home)
        s2.metric(team_b.name, result.strength_away)

        st.subheader("Baseline vs Master vs Bookmaker Odds")

        st.table({
            "Outcome": [
                f"{team_a.name} Win",
                "Draw",
                f"{team_b.name} Win"
            ],
            "Baseline Odds": [
                result.baseline_odds["oh"],
                result.baseline_odds["od"],
                result.baseline_odds["oa"]
            ],
            "Master Odds": [
                result.master_odds["oh"],
                result.master_odds["od"],
                result.master_odds["oa"]
            ],
            "Bookmaker Odds": [
                bk_home,
                bk_draw,
                bk_away
            ],
        })

        st.subheader("Separate Dominance Index")

        d1, d2 = st.columns(2)

        d1.metric(
            team_a.name,
            result.dominance_home,
            delta="Resilient"
            if result.dominance_home >= 0
            else "Fragile"
        )

        d2.metric(
            team_b.name,
            result.dominance_away,
            delta="Resilient"
            if result.dominance_away >= 0
            else "Fragile"
        )

        st.subheader("3-Way Draw Comparison")

        st.write(
            f"Baseline Draw% = **{result.baseline_pct['d']}** "
            f"| Master Draw% = **{result.master_pct['d']}** "
            f"| Consensus (avg) = **{result.model_consensus_draw_pct}** "
            f"| Bookmaker Draw% = **{result.bookmaker_pct['d']}**"
        )

        st.write(
            f"Draw difference (Bookmaker − Consensus) = "
            f"**{result.draw_diff_pct} pts**"
        )

        st.subheader("Value Margin vs Bookmaker")

        st.table({
            "Outcome": [
                f"{team_a.name}",
                "Draw",
                f"{team_b.name}"
            ],
            "Value Margin %": [
                result.value_margin["h"],
                result.value_margin["d"],
                result.value_margin["a"]
            ],
        })

        st.subheader("Top 2 Markets")

        for i, m in enumerate(result.top_markets, 1):
            st.write(f"**{i}. {m.name}** — {m.prob}%")

        st.subheader("Top 3 Correct Scores")

        sc1, sc2, sc3 = st.columns(3)

        for col, (h, a, p) in zip(
            (sc1, sc2, sc3),
            result.top_scores
        ):
            col.metric(
                f"{h} - {a}",
                f"{round(p * 100, 2)}%"
            )

        with st.expander("Show raw EngineResult (debug)"):

            st.json({
                "strength_home": result.strength_home,
                "strength_away": result.strength_away,
                "baseline_pct": result.baseline_pct,
                "baseline_odds": result.baseline_odds,
                "dominance_home": result.dominance_home,
                "dominance_away": result.dominance_away,
                "master_pct": result.master_pct,
                "master_odds": result.master_odds,
                "bookmaker_pct": result.bookmaker_pct,
                "value_margin": result.value_margin,
                "model_consensus_draw_pct":
                    result.model_consensus_draw_pct,
                "draw_diff_pct":
                    result.draw_diff_pct,
            })

else:
    st.info(
        "Fill in both teams' stats and the bookmaker odds above, "
        "then click **RUN ENGINE**."
           )
