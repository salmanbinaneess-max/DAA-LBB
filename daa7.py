import streamlit as st
import pandas as pd


def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Diagonal attack
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

        backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


def board_to_dataframe(solution, n):
    board = []

    for row in range(n):
        current_row = []

        for col in range(n):
            if solution[row] == col:
                current_row.append("♛")
            else:
                current_row.append("·")

        board.append(current_row)

    return pd.DataFrame(
        board,
        columns=[f"C{c+1}" for c in range(n)]
    )


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(
    page_title="N-Queens Solver",
    layout="wide"
)

st.title("♕ N-Queens Problem Using Backtracking")

st.write(
    "Place N queens on an N×N chessboard so that "
    "no two queens attack each other."
)

n = st.slider(
    "Select N",
    min_value=4,
    max_value=12,
    value=8
)

if st.button("Solve N-Queens"):

    with st.spinner("Finding solutions..."):
        solutions, backtracks = solve_n_queens(n)

    st.success("Computation Complete!")

    col1, col2 = st.columns(2)

    col1.metric("Number of Solutions", len(solutions))
    col2.metric("Backtracking Steps", backtracks)

    # Show all solutions for small N
    if n <= 6:

        st.subheader("Solutions")

        for idx, sol in enumerate(solutions, start=1):

            st.markdown(f"### Solution {idx}")
            st.write(sol)

            df = board_to_dataframe(sol, n)
            st.table(df)

    else:

        st.info(
            f"{len(solutions)} solutions found. "
            f"For N > 6, board display is hidden to keep the app fast."
        )

        if solutions:
            st.subheader("First Solution")

            st.write(solutions[0])

            df = board_to_dataframe(solutions[0], n)
            st.table(df)

st.markdown("---")
st.info(
    "Backtracking explores possible queen placements and "
    "rejects invalid positions early."
)