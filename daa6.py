def matrix_chain_order(dims):
&quot;&quot;&quot;
Matrix Chain Multiplication using DP
dims: list of dimensions, matrix i has dims[i-1] x dims[i]
Time: O(n^3), Space: O(n^2)
&quot;&quot;&quot;
n = len(dims) - 1
# m[i][j] = minimum multiplications for matrices i..j
m = [[0] * (n + 1) for _ in range(n + 1)]
s = [[0] * (n + 1) for _ in range(n + 1)]
# l is the chain length
for l in range(2, n + 1):
for i in range(1, n - l + 2):
j = i + l - 1
m[i][j] = float(&#39;inf&#39;)
for k in range(i, j):
cost = m[i][k] + m[k+1][j] + dims[i-1] * dims[k] * dims[j]
if cost &lt; m[i][j]:
m[i][j] = cost
s[i][j] = k
return m, s
def print_optimal_parens(s, i, j):
if i == j:
return f&#39;A{i}&#39;
k = s[i][j]
left = print_optimal_parens(s, i, k)
right = print_optimal_parens(s, k + 1, j)
return f&#39;({left} x {right})&#39;
def print_dp_table(m, n):
print(&#39;\nDP Cost Table m[i][j]:&#39;)
print(f&#39;{&quot;&quot;:&gt;6}&#39;, end=&#39;&#39;)
for j in range(1, n + 1):
print(f&#39;A{j:&gt;8}&#39;, end=&#39;&#39;)
print()
for i in range(1, n + 1):
print(f&#39;A{i:&lt;5}&#39;, end=&#39;&#39;)
for j in range(1, n + 1):
if j &lt; i: print(f&#39;{&quot;---&quot;:&gt;9}&#39;, end=&#39;&#39;)
else: print(f&#39;{m[i][j]:&gt;9}&#39;, end=&#39;&#39;)
print()
# A1(10x30), A2(30x5), A3(5x60), A4(60x10)
dims = [10, 30, 5, 60, 10]
n = len(dims) - 1
print(f&#39;Matrix Dimensions:&#39;)
for i in range(n):
print(f&#39; A{i+1}: {dims[i]} x {dims[i+1]}&#39;)
m, s = matrix_chain_order(dims)
print(f&#39;\nMinimum scalar multiplications: {m[1][n]}&#39;)
print(f&#39;Optimal parenthesization: {print_optimal_parens(s, 1, n)}&#39;)
print_dp_table(m, n)