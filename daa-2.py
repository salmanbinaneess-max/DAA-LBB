import time
import random

# ---------------- Naive Search ----------------
def naive_search(text, pattern):
    if len(pattern) == 0 or len(pattern) > len(text):
        return [], 0

    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)

    return matches, comparisons


# ---------------- Compute LPS ----------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


# ---------------- KMP Search ----------------
def kmp_search(text, pattern):
    if len(pattern) == 0 or len(pattern) > len(text):
        return [], 0

    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# ---------------- Rabin-Karp Search ----------------
def rabin_karp(text, pattern, q=101):
    if len(pattern) == 0 or len(pattern) > len(text):
        return [], 0

    d = 256
    n, m = len(text), len(pattern)

    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:

            match = True

            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    match = False
                    break

            if match:
                matches.append(s)

        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------- Main Program ----------------
print("=" * 60)
print("      STRING MATCHING ALGORITHMS")
print("=" * 60)

text = input("Enter the Text    : ")
pattern = input("Enter the Pattern : ")

print("\nSearching...\n")

# Naive
start = time.perf_counter()
matches1, comp1 = naive_search(text, pattern)
time1 = time.perf_counter() - start

# KMP
start = time.perf_counter()
matches2, comp2 = kmp_search(text, pattern)
time2 = time.perf_counter() - start

# Rabin-Karp
start = time.perf_counter()
matches3, comp3 = rabin_karp(text, pattern)
time3 = time.perf_counter() - start

print("-" * 60)
print("Naive Search")
print("Matches      :", matches1)
print("Comparisons :", comp1)
print("Time (sec)  :", f"{time1:.8f}")

print("-" * 60)
print("KMP Search")
print("Matches      :", matches2)
print("Comparisons :", comp2)
print("Time (sec)  :", f"{time2:.8f}")

print("-" * 60)
print("Rabin-Karp Search")
print("Matches      :", matches3)
print("Comparisons :", comp3)
print("Time (sec)  :", f"{time3:.8f}")

# ---------------- Performance Comparison ----------------
print("\n")
print("=" * 75)
print("Performance Comparison on Random Text (Length = 10000)")
print("=" * 75)

text_large = ''.join(random.choices("ABCD", k=10000))
patterns = ["AB", "ABCD", "ABCDAB", "ABCDABCD"]

print(f"{'Pattern':<12}{'Naive':>12}{'KMP':>12}{'Rabin-Karp':>15}")
print("-" * 55)

for p in patterns:
    _, c1 = naive_search(text_large, p)
    _, c2 = kmp_search(text_large, p)
    _, c3 = rabin_karp(text_large, p)

    print(f"{p:<12}{c1:>12}{c2:>12}{c3:>15}")