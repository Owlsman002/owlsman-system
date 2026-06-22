import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


def r3(x: float) -> float:
    """Round to 3 decimal places."""
    return round(x * 1000) / 1000


# ---------------------------------------------------------------------------
# Phase 1: Efficiency % & Conversion Rates
# ---------------------------------------------------------------------------

@dataclass
class Phase1Result:
    pct_scored: float
    calc_scored: float
    pct_concede: float
    calc_concede: float


def phase1(goals_scored: float, goals_conceded: float,
           shots_on_target_for: float, shots_on_target_against: float) -> Phase1Result:
    pct_scored = r3((goals_scored / shots_on_target_for) * 100)
    calc_scored = r3((1 / pct_scored) * 100)
    pct_concede = r3((goals_conceded / shots_on_target_against) * 100)
    calc_concede = r3((1 / pct_concede) * 100)
    return Phase1Result(pct_scored, calc_scored, pct_concede, calc_concede)


# ---------------------------------------------------------------------------
# Phase 2 & 3: Net Score, Score Power, Final Strength
# ---------------------------------------------------------------------------

@dataclass
class Phase23Result:
    net: float
    ratio: float
    power: float
    avg_xg_bc: float
    strength: float


def phase23(g_self: float, c_opp: float, sot_self: float,
            xg_self: float, bc_self: float,
            calc_scored_self: float, calc_concede_opp: float) -> Phase23Result:
    net = r3(calc_scored_self / calc_concede_opp)
    ratio = r3(g_self / c_opp)
    power = r3((ratio / net) * sot_self)
    avg_xg_bc = r3((xg_self + bc_self) / 2)
    strength = r3(avg_xg_bc * power)
    return Phase23Result(net, ratio, power, avg_xg_bc, strength)


# ---------------------------------------------------------------------------
# Phase 4: Discrete Poisson Distribution Grid -> Baseline Odds
# ---------------------------------------------------------------------------

MAX_SCORE_CAP = 6  # Fixed at 6, exactly as the original formula specifies.


def pmf(k: int, lam: float) -> float:
    return (lam ** k * math.exp(-lam)) / math.factorial(k)


def poisson_grid(lambda_home: float, lambda_away: float, cap: int = MAX_SCORE_CAP) -> List[List[float]]:
    """7x7 (or cap+1 x cap+1) grid: grid[h][a] = P(h; lambda_home) * P(a; lambda_away)."""
    grid = []
    for h in range(cap + 1):
        row = [pmf(h, lambda_home) * pmf(a, lambda_away) for a in range(cap + 1)]
        grid.append(row)
    return grid


def normalize_grid(grid: List[List[float]]) -> List[List[float]]:
    total = sum(sum(row) for row in grid)
    return [[v / total for v in row] for row in grid]


def outcome_sums(grid: List[List[float]]) -> Tuple[float, float, float]:
    home = draw = away = 0.0
    for h, row in enumerate(grid):
        for a, p in enumerate(row):
            if h > a:
                home += p
            elif h == a:
                draw += p
            else:
                away += p
    return home, draw, away


def to_pct(home: float, draw: float, away: float) -> Dict[str, float]:
    total = home + draw + away
    return {"h": r3(home / total * 100), "d": r3(draw / total * 100), "a": r3(away / total * 100)}


EPS = 0.001  # Floors a 0.000% probability so 100/x never literally divides by zero.


def odds_from_pct(pct: Dict[str, float]) -> Dict[str, float]:
    return {
        "oh": r3(100 / max(pct["h"], EPS)),
        "od": r3(100 / max(pct["d"], EPS)),
        "oa": r3(100 / max(pct["a"], EPS)),
    }


# ---------------------------------------------------------------------------
# Phase 5: 5-Odds Stress Matrix -> Separate Dominance Index
# ---------------------------------------------------------------------------

W_TAC, W_HUM, W_ENV, W_MKT = 0.6, 0.5, 0.4, 0.3
SIGMA = r3(W_TAC * W_HUM * W_ENV * W_MKT)
DRAG = r3(100 * SIGMA)


def renormalize(h: float, d: float, a: float) -> Dict[str, float]:
    total = h + d + a
    return {"h": r3(h / total * 100), "d": r3(d / total * 100), "a": r3(a / total * 100)}


def stress_state(base: Dict[str, float], target: str) -> Dict[str, float]:
    h, d, a = base["h"], base["d"], base["a"]
    if target == "home":
        h = r3((h + 50) - DRAG)
    elif target == "away":
        a = r3((a + 50) - DRAG)
    elif target == "draw":
        d = r3((d + 50) - DRAG)
    elif target == "all":
        h = r3((h + 50) - DRAG)
        d = r3((d + 50) - DRAG)
        a = r3((a + 50) - DRAG)
    return renormalize(h, d, a)


def build_five_states(base_pct: Dict[str, float]) -> List[Dict[str, float]]:
    return [
        dict(base_pct),
        stress_state(base_pct, "home"),
        stress_state(base_pct, "away"),
        stress_state(base_pct, "draw"),
        stress_state(base_pct, "all"),
    ]


def implied_probs(states: List[Dict[str, float]]) -> List[Dict[str, float]]:
    out = []
    for s in states:
        o = odds_from_pct(s)
        out.append({"h": r3(1 / o["oh"]), "d": r3(1 / o["od"]), "a": r3(1 / o["oa"])})
    return out


def dominance_index(implied: List[Dict[str, float]], side: str) -> float:
    baseline = implied[0][side]
    total = 0.0
    for state in implied[1:]:
        total = r3(total + r3(state[side] - baseline))
    return total


# ---------------------------------------------------------------------------
# Phase 6: Ensemble Master Odds, Bookmaker comparison, Value Margin
# ---------------------------------------------------------------------------

def master_pct_from_states(states: List[Dict[str, float]]) -> Dict[str, float]:
    return {
        "h": r3(sum(s["h"] for s in states) / 5),
        "d": r3(sum(s["d"] for s in states) / 5),
        "a": r3(sum(s["a"] for s in states) / 5),
    }


def bookmaker_normalized_pct(bk_h: float, bk_d: float, bk_a: float) -> Dict[str, float]:
    implied = {"h": 1 / bk_h, "d": 1 / bk_d, "a": 1 / bk_a}
    total = implied["h"] + implied["d"] + implied["a"]
    return {"h": r3(implied["h"] / total * 100), "d": r3(implied["d"] / total * 100), "a": r3(implied["a"] / total * 100)}


def value_margin(master_pct: Dict[str, float], bk_pct: Dict[str, float]) -> Dict[str, float]:
    return {
        "h": r3(master_pct["h"] - bk_pct["h"]),
        "d": r3(master_pct["d"] - bk_pct["d"]),
        "a": r3(master_pct["a"] - bk_pct["a"]),
    }


# ---------------------------------------------------------------------------
# Final step: Dominance + Draw-Difference grid
# (drives correct scores & markets -- NOT Strength, Baseline, or Master H/A)
# ---------------------------------------------------------------------------

DOM_MAX_ADJ = 0.4
DOM_SCALE = 0.3
NEUTRAL_BASE_LAMBDA = 1.35  # Independent reference: average goals/team, not derived
                            # from Strength, Baseline, or Master.


def dom_adj_factor(dom: float) -> float:
    """Bounded, saturating adjustment (max +/-40%) so an extreme Dominance score
    nudges scoring expectancy without ever being able to erase it entirely."""
    return 1 + DOM_MAX_ADJ * math.tanh(dom / DOM_SCALE)


@dataclass
class DominanceDrawDiffResult:
    lambda_home: float
    lambda_away: float
    draw_diff_pct: float
    model_consensus_draw_pct: float
    grid: List[List[float]]
    outcome_pct: Dict[str, float]


def build_dominance_drawdiff_grid(dom_home: float, dom_away: float,
                                   baseline_draw_pct: float, master_draw_pct: float,
                                   bookmaker_draw_pct: float) -> DominanceDrawDiffResult:
    """Correct scores and markets are generated from each team's Dominance Index plus
    a THREE-way Draw comparison: Baseline Draw%, Master Draw%, and Bookmaker Draw%.
    Baseline and Master are averaged into a single 'model consensus' Draw view, then
    compared against the Bookmaker's Draw% to produce the Draw-difference signal."""
    lambda_home = r3(NEUTRAL_BASE_LAMBDA * dom_adj_factor(dom_home))
    lambda_away = r3(NEUTRAL_BASE_LAMBDA * dom_adj_factor(dom_away))

    raw_grid = poisson_grid(max(lambda_home, 0.01), max(lambda_away, 0.01))
    grid = normalize_grid(raw_grid)
    n = len(grid)

    model_consensus_draw_pct = r3((baseline_draw_pct + master_draw_pct) / 2)
    draw_diff_pct = r3(bookmaker_draw_pct - model_consensus_draw_pct)

    diag_sum = sum(grid[i][i] for i in range(n))
    off_sum = sum(grid[h][a] for h in range(n) for a in range(n) if h != a)

    new_diag_frac = min(max(diag_sum * 100 + draw_diff_pct, 0.001), 99.999) / 100
    new_off_frac = 1 - new_diag_frac
    diag_scale = new_diag_frac / diag_sum if diag_sum > 0 else 0.0
    off_scale = new_off_frac / off_sum if off_sum > 0 else 0.0

    final_grid = [
        [grid[h][a] * (diag_scale if h == a else off_scale) for a in range(n)]
        for h in range(n)
    ]

    home_pct = sum(final_grid[h][a] for h in range(n) for a in range(n) if h > a) * 100
    draw_pct = sum(final_grid[i][i] for i in range(n)) * 100
    away_pct = sum(final_grid[h][a] for h in range(n) for a in range(n) if a > h) * 100

    return DominanceDrawDiffResult(
        lambda_home=lambda_home,
        lambda_away=lambda_away,
        draw_diff_pct=draw_diff_pct,
        model_consensus_draw_pct=model_consensus_draw_pct,
        grid=final_grid,
        outcome_pct={"h": home_pct, "d": draw_pct, "a": away_pct},
    )


@dataclass
class MarketCandidate:
    name: str
    prob: float


def market_candidates(grid: List[List[float]], outcome_pct: Dict[str, float],
                       dom_home: float, dom_away: float,
                       lambda_home: float, lambda_away: float,
                       name_a: str, name_b: str,
                       top_scores: List[Tuple[int, int, float]]) -> List[MarketCandidate]:
    """BTTS and Over/Under are derived directly from the SAME top-N predicted correct
    scores shown to the user, weighted by their relative probability among just those
    scores -- this guarantees the market verdict can never contradict the correct-score
    predictions (e.g. predicting 1-1 while recommending Over 2.5). DC12 and Handicap
    remain sourced from the full Dominance+DrawDiff grid, since match result / margin
    is a different dimension not directly implied by a single scoreline."""
    n = len(grid)

    top_total_p = sum(p for _, _, p in top_scores)
    under_weight = sum(p for h, a, p in top_scores if h + a <= 2)
    btts_yes_weight = sum(p for h, a, p in top_scores if h >= 1 and a >= 1)
    under_pct3 = r3((under_weight / top_total_p) * 100)
    over_pct3 = r3(100 - under_pct3)
    btts_yes_pct3 = r3((btts_yes_weight / top_total_p) * 100)
    btts_no_pct3 = r3(100 - btts_yes_pct3)

    dc12 = r3(outcome_pct["h"] + outcome_pct["a"])

    favorite_is_home = lambda_home >= lambda_away
    fav_dominance = dom_home if favorite_is_home else dom_away

    margin_win_prob = 0.0
    for h in range(n):
        for a in range(n):
            p = grid[h][a]
            if favorite_is_home and (h - a) >= 2:
                margin_win_prob += p
            if not favorite_is_home and (a - h) >= 2:
                margin_win_prob += p
    margin_win_prob = r3(margin_win_prob)

    if fav_dominance >= 0:
        handicap_name = f"{name_a if favorite_is_home else name_b} -1.5 Asian Handicap"
        handicap_prob = r3(margin_win_prob * 100)
    else:
        handicap_name = f"{name_b if favorite_is_home else name_a} +1.5 Asian Handicap"
        handicap_prob = r3((1 - margin_win_prob) * 100)

    btts_name = "BTTS — Yes" if btts_yes_pct3 >= btts_no_pct3 else "BTTS — No"
    btts_prob = max(btts_yes_pct3, btts_no_pct3)

    goals_name = "Under 2.5 / Low-Scoring Match" if under_pct3 >= over_pct3 else "Over 2.5 / High-Scoring Match"
    goals_prob = max(under_pct3, over_pct3)

    candidates = [
        MarketCandidate(btts_name, btts_prob),
        MarketCandidate("Double Chance (12) — No Draw", dc12),
        MarketCandidate(goals_name, goals_prob),
        MarketCandidate(handicap_name, handicap_prob),
    ]
    candidates.sort(key=lambda c: c.prob, reverse=True)
    return candidates


def top_correct_scores(grid: List[List[float]], top_n: int = 3) -> List[Tuple[int, int, float]]:
    n = len(grid)
    flat = [(h, a, grid[h][a]) for h in range(n) for a in range(n)]
    flat.sort(key=lambda x: x[2], reverse=True)
    return flat[:top_n]


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------

@dataclass
class TeamStats:
    name: str
    goals_scored: float
    goals_conceded: float
    shots_on_target_for: float
    shots_on_target_against: float
    big_chances: float
    expected_goals: float


@dataclass
class EngineResult:
    strength_home: float
    strength_away: float
    baseline_pct: Dict[str, float]
    baseline_odds: Dict[str, float]
    dominance_home: float
    dominance_away: float
    master_pct: Dict[str, float]
    master_odds: Dict[str, float]
    bookmaker_pct: Dict[str, float]
    value_margin: Dict[str, float]
    model_consensus_draw_pct: float
    draw_diff_pct: float
    top_markets: List[MarketCandidate]
    top_scores: List[Tuple[int, int, float]]


def run_engine(team_a: TeamStats, team_b: TeamStats,
               bookmaker_home_odd: float, bookmaker_draw_odd: float, bookmaker_away_odd: float) -> EngineResult:

    # Phase 1
    p1a = phase1(team_a.goals_scored, team_a.goals_conceded,
                 team_a.shots_on_target_for, team_a.shots_on_target_against)
    p1b = phase1(team_b.goals_scored, team_b.goals_conceded,
                 team_b.shots_on_target_for, team_b.shots_on_target_against)

    # Phase 2 & 3
    p23a = phase23(team_a.goals_scored, team_b.goals_conceded, team_a.shots_on_target_for,
                    team_a.expected_goals, team_a.big_chances, p1a.calc_scored, p1b.calc_concede)
    p23b = phase23(team_b.goals_scored, team_a.goals_conceded, team_b.shots_on_target_for,
                    team_b.expected_goals, team_b.big_chances, p1b.calc_scored, p1a.calc_concede)

    strength_home = p23a.strength
    strength_away = p23b.strength

    # Phase 4
    grid = poisson_grid(strength_home, strength_away)
    home_sum, draw_sum, away_sum = outcome_sums(grid)
    base_pct = to_pct(home_sum, draw_sum, away_sum)
    base_odds = odds_from_pct(base_pct)

    # Phase 5
    states = build_five_states(base_pct)
    implied = implied_probs(states)
    dom_home = dominance_index(implied, "h")
    dom_away = dominance_index(implied, "a")

    # Phase 6
    master_pct = master_pct_from_states(states)
    master_odds = odds_from_pct(master_pct)
    bk_pct = bookmaker_normalized_pct(bookmaker_home_odd, bookmaker_draw_odd, bookmaker_away_odd)
    margin = value_margin(master_pct, bk_pct)

    # Final step: Dominance + Draw-Difference grid (drives scores & markets)
    dd = build_dominance_drawdiff_grid(dom_home, dom_away, base_pct["d"], master_pct["d"], bk_pct["d"])
    scores = top_correct_scores(dd.grid)
    candidates = market_candidates(dd.grid, dd.outcome_pct, dom_home, dom_away,
                                    dd.lambda_home, dd.lambda_away, team_a.name, team_b.name, scores)

    return EngineResult(
        strength_home=strength_home,
        strength_away=strength_away,
        baseline_pct=base_pct,
        baseline_odds=base_odds,
        dominance_home=dom_home,
        dominance_away=dom_away,
        master_pct=master_pct,
        master_odds=master_odds,
        bookmaker_pct=bk_pct,
        value_margin=margin,
        model_consensus_draw_pct=dd.model_consensus_draw_pct,
        draw_diff_pct=dd.draw_diff_pct,
        top_markets=candidates[:2],
        top_scores=scores,
    )


def print_report(team_a: TeamStats, team_b: TeamStats, result: EngineResult) -> None:
    print("=" * 60)
    print("OWLSNATION ENGINE REPORT")
    print("=" * 60)
    print(f"{team_a.name} Strength: {result.strength_home}")
    print(f"{team_b.name} Strength: {result.strength_away}")
    print()
    print("Baseline Odds (Odd 0):")
    print(f"  {team_a.name}: {result.baseline_odds['oh']}   Draw: {result.baseline_odds['od']}   {team_b.name}: {result.baseline_odds['oa']}")
    print()
    print("Separate Dominance Index:")
    print(f"  {team_a.name}: {result.dominance_home}")
    print(f"  {team_b.name}: {result.dominance_away}")
    print()
    print("Master (Ensemble) Odds:")
    print(f"  {team_a.name}: {result.master_odds['oh']}   Draw: {result.master_odds['od']}   {team_b.name}: {result.master_odds['oa']}")
    print()
    print("Value Margin vs Bookmaker:")
    print(f"  Home: {result.value_margin['h']}%   Draw: {result.value_margin['d']}%   Away: {result.value_margin['a']}%")
    print()
    print("3-Way Draw Comparison (drives the Draw-Difference adjustment):")
    print(f"  Baseline Draw% = {result.baseline_pct['d']}   Master Draw% = {result.master_pct['d']}   "
          f"Consensus (avg) = {result.model_consensus_draw_pct}   Bookmaker Draw% = {result.bookmaker_pct['d']}")
    print(f"  Draw diff (Bookmaker - Consensus) = {result.draw_diff_pct} pts")
    print()
    print("Top 2 Markets (Dominance + Draw-Difference grid):")
    for i, m in enumerate(result.top_markets, 1):
        print(f"  {i}. {m.name} — {m.prob}%")
    print()
    print("Top 3 Correct Scores (Dominance + Draw-Difference grid):")
    for i, (h, a, p) in enumerate(result.top_scores, 1):
        print(f"  {i}. {h}-{a} ({round(p * 100, 2)}%)")


if __name__ == "__main__":
    # Example: the worked sample used throughout this project's verification.
    team_a = TeamStats(
        name="Team A",
        goals_scored=2, goals_conceded=4,
        shots_on_target_for=5, shots_on_target_against=3,
        big_chances=0.58, expected_goals=0.77,
    )
    team_b = TeamStats(
        name="Team B",
        goals_scored=3, goals_conceded=5,
        shots_on_target_for=2, shots_on_target_against=8,
        big_chances=0.50, expected_goals=0.89,
    )

    result = run_engine(team_a, team_b, bookmaker_home_odd=3.40, bookmaker_draw_odd=3.40, bookmaker_away_odd=2.10)
    print_report(team_a, team_b, result)
