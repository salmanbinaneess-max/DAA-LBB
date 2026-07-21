import streamlit as st
import random
import pandas as pd

# Global counter
comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Conquer
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="Min-Max Analysis", layout="wide")

st.title("📊 Divide & Conquer Min-Max Algorithm")

st.write(
    "Compare Divide & Conquer Min-Max with the Naive approach "
    "based on the number of comparisons."
)

# User Input
size = st.slider(
    "Select Array Size",
    min_value=10,
    max_value=10000,
    value=100,
    step=10
)

if st.button("Generate Array & Analyze"):

    arr = [random.randint(1, 10000) for _ in range(size)]

    # Divide & Conquer
    comparison_count = 0
    mn, mx = min_max_dc(arr, 0, len(arr) - 1)
    dc_comps = comparison_count

    # Naive
    _, _, naive_comps = min_max_naive(arr)

    # Results
    st.subheader("Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Minimum", mn)
    col2.metric("Maximum", mx)
    col3.metric("D&C Comparisons", dc_comps)
    col4.metric("Naive Comparisons", naive_comps)

    st.subheader("Sample Array")

    st.write(arr[:50])
    if len(arr) > 50:
        st.info("Showing first 50 elements only.")

    st.subheader("Comparison Summary")

    formula = 3 * size // 2 - 2

    df = pd.DataFrame({
        "Array Size": [size],
        "D&C Comparisons": [dc_comps],
        "Naive Comparisons": [naive_comps],
        "Formula (3n/2 - 2)": [formula]
    })

    st.dataframe(df, use_container_width=True)

# --------------------------
# Performance Analysis Table
# --------------------------

st.subheader("Performance Analysis")

sizes = [10, 100, 1000, 10000]

records = []

for s in sizes:
    arr = [random.randint(1, 10000) for _ in range(s)]

    comparison_count = 0
    min_max_dc(arr, 0, len(arr) - 1)
    dc = comparison_count

    _, _, naive = min_max_naive(arr)

    records.append([
        s,
        dc,
        naive,
        3 * s // 2 - 2
    ])

perf_df = pd.DataFrame(
    records,
    columns=[
        "Size",
        "D&C Comparisons",
        "Naive Comparisons",
        "Formula (3n/2 - 2)"
    ]
)

st.dataframe(perf_df, use_container_width=True)

st.markdown("---")
st.success("Divide & Conquer reduces comparisons compared to the naive method.")
