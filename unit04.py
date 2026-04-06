"""
Unit 4: Solving Linear Systems of Equations
============================================
Implements and tests Gaussian Elimination with Scaled Partial Pivoting
and Back Substitution (tools.solve_lsoe).

Test cases:
  1. Instructor's 4×4 system from ECE 5110 MATLAB code
  2. Identity matrix (trivial)
  3. 2×2 simple system
  4. Singular matrix (should return error)
  5. Condition number analysis — error vs matrix size
"""

from lib.tools import tools
import numpy as np
import matplotlib.pyplot as plt

tool = tools()

# ═══════════════════════════════════════════════════════════════════════
# TEST 1: Instructor's 4×4 system (from MATLAB unittest_lsoe.m)
# A = [1 1 1 1; 1 2 3 4; 0 2 0 1; -1 -2 1 2],  B = [4; 10; 12; 0]
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  TEST 1: Instructor's 4×4 System (ECE 5110 MATLAB)")
print("=" * 60)

A1 = np.array([[1, 1, 1, 1],
               [1, 2, 3, 4],
               [0, 2, 0, 1],
               [-1, -2, 1, 2]], dtype=float)
B1 = np.array([4, 10, 12, 0], dtype=float)

sol1, err1 = tool.solve_lsoe(A1.copy(), B1.copy())
ref1 = np.linalg.solve(A1, B1)

print(f"  Our solution:       {sol1}")
print(f"  numpy.linalg.solve: {ref1}")
print(f"  Max error:          {np.max(np.abs(sol1 - ref1)):.2e}")
print(f"  Error code:         {err1}")
assert err1 == 0, "Should succeed"
assert np.allclose(sol1, ref1, atol=1e-10), "Solution mismatch!"
print("  ✓ PASSED\n")

# ═══════════════════════════════════════════════════════════════════════
# TEST 2: Identity matrix — solution should equal B
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  TEST 2: Identity Matrix (3×3)")
print("=" * 60)

A2 = np.eye(3)
B2 = np.array([1.0, 2.0, 3.0])

sol2, err2 = tool.solve_lsoe(A2.copy(), B2.copy())
print(f"  Our solution: {sol2}")
print(f"  Expected:     {B2}")
assert err2 == 0
assert np.allclose(sol2, B2, atol=1e-10)
print("  ✓ PASSED\n")

# ═══════════════════════════════════════════════════════════════════════
# TEST 3: Simple 2×2 system
#   2x +  y = 5
#    x + 3y = 7   →  x = 1.6, y = 1.8
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  TEST 3: Simple 2×2 System")
print("=" * 60)

A3 = np.array([[2, 1], [1, 3]], dtype=float)
B3 = np.array([5, 7], dtype=float)

sol3, err3 = tool.solve_lsoe(A3.copy(), B3.copy())
ref3 = np.linalg.solve(A3, B3)
print(f"  Our solution:       {sol3}")
print(f"  numpy.linalg.solve: {ref3}")
assert err3 == 0
assert np.allclose(sol3, ref3, atol=1e-10)
print("  ✓ PASSED\n")

# ═══════════════════════════════════════════════════════════════════════
# TEST 4: Singular matrix — should return error code -1
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  TEST 4: Singular Matrix (should fail)")
print("=" * 60)

A4 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
B4 = np.array([1, 2, 3], dtype=float)

sol4, err4 = tool.solve_lsoe(A4.copy(), B4.copy())
print(f"  Error code: {err4}  (expected -1)")
assert err4 == -1, "Should detect singular matrix"
print("  ✓ PASSED\n")

# ═══════════════════════════════════════════════════════════════════════
# TEST 5: Larger system — 6×6 random well-conditioned
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  TEST 5: Random 6×6 Well-Conditioned System")
print("=" * 60)

np.random.seed(42)
A5 = np.random.randn(6, 6) + 3 * np.eye(6)  # diagonally dominant
B5 = np.random.randn(6)

sol5, err5 = tool.solve_lsoe(A5.copy(), B5.copy())
ref5 = np.linalg.solve(A5, B5)
print(f"  Our solution:       {np.round(sol5, 6)}")
print(f"  numpy.linalg.solve: {np.round(ref5, 6)}")
print(f"  Max error:          {np.max(np.abs(sol5 - ref5)):.2e}")
assert err5 == 0
assert np.allclose(sol5, ref5, atol=1e-10)
print("  ✓ PASSED\n")

# ═══════════════════════════════════════════════════════════════════════
# PLOT 1: Solution accuracy vs matrix size
# ═══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  Generating accuracy plots...")
print("=" * 60)

sizes = [3, 5, 10, 20, 30, 50, 75, 100]
errors = []
cond_nums = []

np.random.seed(123)
for n in sizes:
    A_test = np.random.randn(n, n) + n * np.eye(n)  # well-conditioned
    x_true = np.random.randn(n)
    B_test = A_test @ x_true

    sol_test, _ = tool.solve_lsoe(A_test.copy(), B_test.copy())
    errors.append(np.max(np.abs(sol_test - x_true)))
    cond_nums.append(np.linalg.cond(A_test))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Error vs matrix size
ax1 = axes[0]
ax1.semilogy(sizes, errors, 'bo-', linewidth=2, markersize=8, label='Max |error|')
ax1.set_xlabel('Matrix Size n', fontsize=12)
ax1.set_ylabel('Max Absolute Error', fontsize=12)
ax1.set_title('Gaussian Elimination Accuracy vs Matrix Size', fontsize=13)
ax1.grid(True, ls='--', lw=0.6, which='both')
ax1.legend(fontsize=10)

# Right: Condition number vs matrix size
ax2 = axes[1]
ax2.semilogy(sizes, cond_nums, 'rs-', linewidth=2, markersize=8, label='cond(A)')
ax2.set_xlabel('Matrix Size n', fontsize=12)
ax2.set_ylabel('Condition Number κ(A)', fontsize=12)
ax2.set_title('Matrix Condition Number vs Size', fontsize=13)
ax2.grid(True, ls='--', lw=0.6, which='both')
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('unit04_accuracy_analysis.png', dpi=150)
plt.show()

# ═══════════════════════════════════════════════════════════════════════
# PLOT 2: Step-by-step elimination visualization (4×4 instructor system)
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  Step-by-step Gaussian elimination on instructor's system")
print("=" * 60)

A_vis = np.array([[1, 1, 1, 1],
                  [1, 2, 3, 4],
                  [0, 2, 0, 1],
                  [-1, -2, 1, 2]], dtype=float)
B_vis = np.array([4, 10, 12, 0], dtype=float)

print(f"\n  Original system [A|B]:")
aug = np.column_stack([A_vis, B_vis])
for row in aug:
    print(f"    [{' '.join(f'{v:8.4f}' for v in row)}]")

sol_vis, _ = tool.solve_lsoe(A_vis.copy(), B_vis.copy())
print(f"\n  Solution: x = {sol_vis}")
print(f"  Verify:   A·x = {A_vis @ sol_vis}")
print(f"  Expected:   B = {B_vis}")

# ═══════════════════════════════════════════════════════════════════════
# Summary table
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  Summary: All Tests")
print("=" * 60)
print(f"  {'Test':<40} {'Status':<10}")
print("-" * 60)
print(f"  {'1. Instructor 4×4 system':<40} {'✓ PASSED':<10}")
print(f"  {'2. Identity matrix 3×3':<40} {'✓ PASSED':<10}")
print(f"  {'3. Simple 2×2 system':<40} {'✓ PASSED':<10}")
print(f"  {'4. Singular matrix detection':<40} {'✓ PASSED':<10}")
print(f"  {'5. Random 6×6 well-conditioned':<40} {'✓ PASSED':<10}")
print("=" * 60)
print("\nDONE!")
