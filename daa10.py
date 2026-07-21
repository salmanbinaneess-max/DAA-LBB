import streamlit as st
import random
import time
import sys
import pandas as pd

sys.setrecursionlimit(20000)

comparisons = 0


# -----------------------------
# Partition Function
# -----------------------------
def partition(arr, low, high):
    global comparisons

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        comparisons += 1

        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# -----------------------------
# Deterministic Quick Sort
# -----------------------------
def deterministic_quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        deterministic_quicksort(arr, low, pi - 1)
        deterministic_quicksort(arr, pi + 1, high)


# -----------------------------
# Randomized Quick Sort
# -----------------------------
def randomized_quicksort(arr, low, high):
    if low < high:

        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]

        pi = partition(arr, low, high)

        randomized_quicksort(arr, low, pi - 1)
        randomized_quicksort(arr, pi + 1, high)


# -----------------------------
# Test Runner
# -----------------------------
def run_test(sort_fn, arr):
    global comparisons

    a = arr[:]
    comparisons = 0

    start = time.perf_counter()

    sort_fn(a, 0, len(a) - 1)

    elapsed = (time.perf_counter() - start) * 1000

    return comparisons, round(elapsed, 2)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Quick Sort Analysis",
    layout="wide"
)

st.title("⚡ Deterministic vs Randomized Quick Sort")

st.write(
    "Compare Quick Sort variants using comparisons and execution time."
)

N = st.slider(
    "Array Size",
    min_value=100,
    max_value=10000,
    value=5000,
    step=100
)

if st.button("Run Experiment"):

    test_cases = {
        "Random":
            [random.randint(1, 100000) for _ in range(N)],

        "Sorted":
            list(range(N)),

        "Reverse":
            list(range(N, 0, -1)),

        "Nearly Sorted":
            list(range(N))
    }

    # Slightly shuffle Nearly Sorted
    ns = test_cases["Nearly Sorted"]

    for _ in range(N // 20):
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        ns[i], ns[j] = ns[j], ns[i]

    results = []

    with st.spinner("Running Quick Sort tests..."):

        for case, arr in test_cases.items():

            d_comps, d_time = run_test(
                deterministic_quicksort,
                arr
            )

            r_comps, r_time = run_test(
                randomized_quicksort,
                arr
            )

            results.append([
                case,
                d_comps,
                d_time,
                r_comps,
                r_time
            ])

    df = pd.DataFrame(
        results,
        columns=[
            "Input Type",
            "DQS Comparisons",
            "DQS Time (ms)",
            "RQS Comparisons",
            "RQS Time (ms)"
        ]
    )

    st.subheader("Results")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Observations")

    st.info(
        """
        • Deterministic Quick Sort performs poorly on sorted/reverse-sorted data.

        • Randomized Quick Sort avoids worst-case pivot choices.

        • Average complexity of both algorithms is O(n log n).

        • Worst-case complexity of Deterministic Quick Sort is O(n²).
        """
    )

st.markdown("---")
st.success(
    "Randomized pivot selection generally provides more stable performance."
)