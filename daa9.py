import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Bin Packing Visualizer", layout="wide")


# -----------------------------
# Algorithms
# -----------------------------
def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:
        placed = False

        for i, space in enumerate(bins):
            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    return first_fit(sorted(items, reverse=True), capacity)


def best_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):
            if space >= item and space - item < best_space:
                best_space = space - item
                best_idx = i

        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# -----------------------------
# Helper Function
# -----------------------------
def create_df(bins):
    rows = []

    for i, b in enumerate(bins, start=1):
        used = round(sum(b), 2)

        rows.append({
            "Bin": f"Bin {i}",
            "Items": str([round(x, 2) for x in b]),
            "Used Space": used,
            "Free Space": round(1 - used, 2)
        })

    return pd.DataFrame(rows)


# -----------------------------
# UI
# -----------------------------
st.title("📦 Bin Packing Problem")

default_items = "0.5,0.7,0.3,0.9,0.2,0.6,0.8,0.4,0.1,0.5"

item_text = st.text_input(
    "Enter item sizes",
    default_items
)

capacity = st.number_input(
    "Bin Capacity",
    min_value=0.1,
    value=1.0,
    step=0.1
)

if st.button("Run Bin Packing"):

    items = [float(x.strip()) for x in item_text.split(",")]

    total = sum(items)
    lower_bound = math.ceil(total / capacity)

    ff = first_fit(items, capacity)
    ffd = first_fit_decreasing(items, capacity)
    bfd = best_fit_decreasing(items, capacity)

    st.subheader("Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Lower Bound", lower_bound)
    c2.metric("FF", len(ff))
    c3.metric("FFD", len(ffd))
    c4.metric("BFD", len(bfd))

    comparison = pd.DataFrame({
        "Algorithm": ["Lower Bound", "FF", "FFD", "BFD"],
        "Bins Used": [lower_bound, len(ff), len(ffd), len(bfd)]
    })

    st.subheader("Algorithm Comparison")
    st.bar_chart(
        comparison.set_index("Algorithm")
    )

    tab1, tab2, tab3 = st.tabs([
        "First Fit",
        "FFD",
        "BFD"
    ])

    with tab1:
        st.write(f"Bins Used: {len(ff)}")
        st.dataframe(create_df(ff), use_container_width=True)

    with tab2:
        st.write(f"Bins Used: {len(ffd)}")
        st.dataframe(create_df(ffd), use_container_width=True)

    with tab3:
        st.write(f"Bins Used: {len(bfd)}")
        st.dataframe(create_df(bfd), use_container_width=True)

st.markdown("---")
st.info(
    "FFD and BFD typically outperform FF by sorting items before packing."
)