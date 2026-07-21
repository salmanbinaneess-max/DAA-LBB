import streamlit as st
import pandas as pd


def matrix_chain_order(dims):
    """
    Matrix Chain Multiplication using DP
    Time: O(n^3), Space: O(n^2)
    """
    n = len(dims) - 1

    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1

            m[i][j] = float('inf')

            for k in range(i, j):
                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


def print_optimal_parens(s, i, j):
    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="Matrix Chain Multiplication", layout="wide")

st.title("🔗 Matrix Chain Multiplication (Dynamic Programming)")

st.write(
    "Find the minimum number of scalar multiplications needed "
    "to multiply a chain of matrices."
)

st.subheader("Enter Matrix Dimensions")

default_dims = "10,30,5,60,10"

dims_input = st.text_input(
    "Dimensions (comma-separated)",
    default_dims
)

if st.button("Calculate"):

    try:
        dims = [int(x.strip()) for x in dims_input.split(",")]

        if len(dims) < 2:
            st.error("Enter at least two dimensions.")
            st.stop()

        n = len(dims) - 1

        st.subheader("Matrices")

        matrix_info = []

        for i in range(n):
            matrix_info.append(
                [f"A{i+1}", f"{dims[i]} × {dims[i+1]}"]
            )

        st.table(
            pd.DataFrame(
                matrix_info,
                columns=["Matrix", "Dimensions"]
            )
        )

        m, s = matrix_chain_order(dims)

        st.subheader("Results")

        st.metric(
            "Minimum Scalar Multiplications",
            f"{m[1][n]:,}"
        )

        st.success(
            f"Optimal Parenthesization: "
            f"{print_optimal_parens(s, 1, n)}"
        )

        # DP Table
        st.subheader("DP Cost Table")

        table = []

        for i in range(1, n + 1):
            row = []

            for j in range(1, n + 1):

                if j < i:
                    row.append("---")
                else:
                    row.append(m[i][j])

            table.append(row)

        df = pd.DataFrame(
            table,
            index=[f"A{i}" for i in range(1, n + 1)],
            columns=[f"A{i}" for i in range(1, n + 1)]
        )

        st.dataframe(df, use_container_width=True)

    except ValueError:
        st.error("Please enter valid integers separated by commas.")

st.markdown("---")
st.info("Time Complexity: O(n³) | Space Complexity: O(n²)")