import streamlit as st
import pandas as pd
from itertools import permutations

INF = float('inf')


def tsp_brute_force(cost, n):
    """
    Brute Force TSP
    Time Complexity: O(n!)
    """
    cities = list(range(1, n))

    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        current_cost = sum(
            cost[path[i]][path[i + 1]]
            for i in range(n)
        )

        if current_cost < best_cost:
            best_cost = current_cost
            best_path = path

    return best_path, best_cost


# ---------------------------
# Default 5-City Matrix
# ---------------------------

default_cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

cities = ["A", "B", "C", "D", "E"]

# ---------------------------
# Streamlit UI
# ---------------------------

st.set_page_config(
    page_title="TSP Solver",
    layout="wide"
)

st.title("🚗 Travelling Salesman Problem (TSP)")

st.write(
    "Find the minimum-cost tour that visits every city exactly once "
    "and returns to the starting city."
)

# Display Cost Matrix

st.subheader("Cost Matrix")

display_matrix = []

for row in default_cost:
    display_matrix.append(
        ["INF" if x == INF else x for x in row]
    )

df = pd.DataFrame(
    display_matrix,
    index=cities,
    columns=cities
)

st.dataframe(df, use_container_width=True)

if st.button("Find Optimal Tour"):

    n = len(default_cost)

    with st.spinner("Searching all possible tours..."):
        best_path, best_cost = tsp_brute_force(
            default_cost,
            n
        )

    st.success("Optimal Tour Found!")

    tour = " → ".join(
        cities[i] for i in best_path
    )

    col1, col2 = st.columns(2)

    col1.metric("Minimum Cost", best_cost)
    col2.metric(
        "Cities Visited",
        len(best_path) - 1
    )

    st.subheader("Optimal Tour")

    st.markdown(f"### {tour}")

    # Path Verification

    st.subheader("Path Cost Breakdown")

    breakdown = []

    for i in range(n):
        u = best_path[i]
        v = best_path[i + 1]

        breakdown.append([
            cities[u],
            cities[v],
            default_cost[u][v]
        ])

    breakdown_df = pd.DataFrame(
        breakdown,
        columns=[
            "From",
            "To",
            "Cost"
        ]
    )

    st.table(breakdown_df)

    st.success(
        f"Total Tour Cost = {best_cost}"
    )

st.markdown("---")
st.info(
    "Brute Force TSP checks every possible tour. "
    "Time Complexity: O(n!). Suitable only for small numbers of cities."
)