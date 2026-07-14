import streamlit as st
import heapq
import pandas as pd

# ----------------------------
# Dijkstra Algorithm
# ----------------------------
def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n

    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path
    return []


# ----------------------------
# Sample Graph
# ----------------------------
graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Dijkstra Visualizer", layout="wide")

st.title("🚀 Dijkstra's Shortest Path Algorithm")
st.write("Find shortest paths from a selected source vertex.")

source = st.selectbox(
    "Select Source Vertex",
    options=list(graph.keys()),
    index=0
)

if st.button("Run Dijkstra"):
    dist, prev = dijkstra(graph, source)

    results = []

    for v in range(len(graph)):
        path = reconstruct_path(prev, source, v)

        results.append({
            "Vertex": v,
            "Distance": dist[v] if dist[v] != float('inf') else "INF",
            "Path": " -> ".join(map(str, path)) if path else "No Path"
        })

    st.success("Algorithm Completed!")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    st.subheader("Detailed Results")

    for row in results:
        st.write(
            f"**Vertex {row['Vertex']}** | "
            f"Distance: **{row['Distance']}** | "
            f"Path: **{row['Path']}**"
        )

st.markdown("---")
st.caption("Time Complexity: O((V + E) log V)")