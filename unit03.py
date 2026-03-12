"""
Unit 3: Numerical Differentiation & Integration — Optical Flow
===============================================================
Applies numerical differentiation and integration to a 2D optical
flow / mouse-tracking problem:

1. SINGLE INTEGRAL COMPARISON: Compare 4 integration methods
   (Trapezoidal, Simpson 1/3, Simpson 3/8, Midpoint) for
   n = 10:10:1000 steps against the exact answer.

2. DOUBLE INTEGRAL: Compute the total displacement magnitude
   over a 2D region using double integration.

3. OPTICAL FLOW + MATRIX CALCULATION: Use the Lucas-Kanade method
   to estimate velocity from spatial/temporal gradients, involving
   the matrix equation (A^T A)^{-1} A^T b.

4. NUMERICAL DIFFERENTIATION: Estimate velocity from position data
   and reconstruct position by integrating velocity.
"""

from lib.tools import tools
import numpy as np
import matplotlib.pyplot as plt

tool = tools()

# ═══════════════════════════════════════════════════════════════════════
# PART 1: Compare 4 single integral forms for n = 10:10:1000
# ═══════════════════════════════════════════════════════════════════════
# Test function: f(t) = 3*sin(2*t) + t*cos(t)
# This represents a 1D velocity component over time.
# Exact integral from 0 to pi:
#   F(t) = -3/2 cos(2t) + t*sin(t) + cos(t)
#   F(pi) - F(0) = -3/2*cos(2pi) + pi*sin(pi) + cos(pi)
#                 - (-3/2*cos(0) + 0 + cos(0))
#                = -3/2 + 0 - 1 - (-3/2 + 1) = -3/2 - 1 + 3/2 - 1 = -2

def f_single(t):
    return 3 * np.sin(2 * t) + t * np.cos(t)

a, b = 0.0, np.pi
exact_integral = -2.0  # computed analytically

step_counts = np.arange(10, 1001, 10)
errors_trap = []
errors_s13  = []
errors_s38  = []
errors_mid  = []

for n in step_counts:
    err_t = abs(tool.integrate_trapezoidal(f_single, a, b, n) - exact_integral)
    err_s13 = abs(tool.integrate_simpson13(f_single, a, b, n) - exact_integral)
    err_s38 = abs(tool.integrate_simpson38(f_single, a, b, n) - exact_integral)
    err_m = abs(tool.integrate_midpoint(f_single, a, b, n) - exact_integral)
    errors_trap.append(err_t)
    errors_s13.append(err_s13)
    errors_s38.append(err_s38)
    errors_mid.append(err_m)

print("=" * 60)
print("  PART 1: Single Integral — Error Comparison (n=10:10:1000)")
print("=" * 60)
print(f"  Test function: f(t) = 3*sin(2t) + t*cos(t)")
print(f"  Interval: [0, pi],  Exact integral = {exact_integral}")
print(f"  At n=100:")
print(f"    Trapezoidal:  error = {errors_trap[9]:.6e}")
print(f"    Simpson 1/3:  error = {errors_s13[9]:.6e}")
print(f"    Simpson 3/8:  error = {errors_s38[9]:.6e}")
print(f"    Midpoint:     error = {errors_mid[9]:.6e}")

# PLOT 1: Error vs number of steps for all 4 methods
plt.figure(figsize=(10, 6))
plt.loglog(step_counts, errors_trap, 'o-', markersize=2, label='Trapezoidal')
plt.loglog(step_counts, errors_s13,  's-', markersize=2, label="Simpson's 1/3")
plt.loglog(step_counts, errors_s38,  '^-', markersize=2, label="Simpson's 3/8")
plt.loglog(step_counts, errors_mid,  'd-', markersize=2, label='Midpoint')
plt.xlabel('Number of Steps (n)', fontsize=12)
plt.ylabel('Absolute Error', fontsize=12)
plt.title('Single Integral: Error vs Steps for 4 Quadrature Methods', fontsize=13)
plt.legend(fontsize=11)
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.tight_layout()
plt.savefig('unit03_single_integral_comparison.png', dpi=150)
plt.show()

# ═══════════════════════════════════════════════════════════════════════
# PART 2: Optical Flow Problem — Mouse/Movement Tracking in 2D
# ═══════════════════════════════════════════════════════════════════════
# Simulate a cursor moving along a figure-8 path:
#   x(t) = sin(t),   y(t) = sin(2t)/2
# True velocity:
#   vx(t) = cos(t),  vy(t) = cos(2t)

T = 2 * np.pi
N = 200
t = np.linspace(0, T, N)
dt = t[1] - t[0]

# True position and velocity
x_true = np.sin(t)
y_true = np.sin(2 * t) / 2
vx_true = np.cos(t)
vy_true = np.cos(2 * t)

# NUMERICAL DIFFERENTIATION: estimate velocity from position
vx_est = tool.differentiate(x_true, dt, method='central')
vy_est = tool.differentiate(y_true, dt, method='central')

print("\n" + "=" * 60)
print("  PART 2: Optical Flow — Numerical Differentiation")
print("=" * 60)
print(f"  Path: figure-8, x(t) = sin(t), y(t) = sin(2t)/2")
print(f"  N = {N} samples, dt = {dt:.4f} s")
print(f"  Max |vx_error|: {np.max(np.abs(vx_est - vx_true)):.6e}")
print(f"  Max |vy_error|: {np.max(np.abs(vy_est - vy_true)):.6e}")

# NUMERICAL INTEGRATION: reconstruct position from estimated velocity
# Use trapezoidal integration cumulatively
x_recon = np.zeros(N)
y_recon = np.zeros(N)
x_recon[0] = x_true[0]
y_recon[0] = y_true[0]
for i in range(1, N):
    x_recon[i] = x_recon[i-1] + tool.integrate_trapezoidal(
        lambda tau: np.interp(tau, t, vx_est), t[i-1], t[i], 1)
    y_recon[i] = y_recon[i-1] + tool.integrate_trapezoidal(
        lambda tau: np.interp(tau, t, vy_est), t[i-1], t[i], 1)

recon_err_x = np.max(np.abs(x_recon - x_true))
recon_err_y = np.max(np.abs(y_recon - y_true))
print(f"  Reconstruction error (x): {recon_err_x:.6e}")
print(f"  Reconstruction error (y): {recon_err_y:.6e}")

# PLOT 2: True path, estimated velocity, and reconstructed path
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# (a) True path
ax = axes[0]
ax.plot(x_true, y_true, 'b-', linewidth=2, label='True path')
ax.plot(x_recon, y_recon, 'r--', linewidth=2, label='Reconstructed')
ax.set_xlabel('x(t)', fontsize=12)
ax.set_ylabel('y(t)', fontsize=12)
ax.set_title('Figure-8 Trajectory', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, ls='--', alpha=0.5)
ax.set_aspect('equal')

# (b) Velocity comparison
ax = axes[1]
ax.plot(t, vx_true, 'b-', linewidth=2, label='True vx')
ax.plot(t, vx_est, 'r--', linewidth=1.5, label='Estimated vx')
ax.plot(t, vy_true, 'g-', linewidth=2, label='True vy')
ax.plot(t, vy_est, 'm--', linewidth=1.5, label='Estimated vy')
ax.set_xlabel('Time [s]', fontsize=12)
ax.set_ylabel('Velocity', fontsize=12)
ax.set_title('Velocity: True vs Differentiated', fontsize=13)
ax.legend(fontsize=9)
ax.grid(True, ls='--', alpha=0.5)

# (c) Position reconstruction error
ax = axes[2]
ax.plot(t, np.abs(x_recon - x_true), 'b-', label='|x_err|')
ax.plot(t, np.abs(y_recon - y_true), 'r-', label='|y_err|')
ax.set_xlabel('Time [s]', fontsize=12)
ax.set_ylabel('Absolute Error', fontsize=12)
ax.set_title('Position Reconstruction Error', fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, ls='--', alpha=0.5)

plt.tight_layout()
plt.savefig('unit03_optical_flow.png', dpi=150)
plt.show()

# ═══════════════════════════════════════════════════════════════════════
# PART 3: Lucas-Kanade Optical Flow — Matrix Calculation
# ═══════════════════════════════════════════════════════════════════════
# Simulate a 5x5 image patch with a known velocity (u=1.5, v=-0.8)
# The optical flow constraint equation: Ix*u + Iy*v = -It
# For a window of pixels: A * [u; v] = b
# Solution: [u; v] = (A^T A)^{-1} A^T b

print("\n" + "=" * 60)
print("  PART 3: Lucas-Kanade Optical Flow — Matrix Calculation")
print("=" * 60)

# Ground truth velocity
u_true, v_true = 1.5, -0.8

# Create a synthetic intensity gradient field (5x5 window)
np.random.seed(123)
N_pixels = 25
Ix = np.random.randn(N_pixels)  # spatial gradient in x
Iy = np.random.randn(N_pixels)  # spatial gradient in y
# Temporal gradient consistent with true velocity + small noise
It = -(Ix * u_true + Iy * v_true) + 0.05 * np.random.randn(N_pixels)

# Build the system A * [u; v] = -It
A = np.column_stack([Ix, Iy])
b = -It

# Matrix calculations
ATA = A.T @ A       # 2x2 matrix
ATb = A.T @ b       # 2x1 vector

print("\n  A^T A (2x2 matrix):")
print(f"    [{ATA[0,0]:10.4f}  {ATA[0,1]:10.4f}]")
print(f"    [{ATA[1,0]:10.4f}  {ATA[1,1]:10.4f}]")

print(f"\n  A^T b = [{ATb[0]:.4f}, {ATb[1]:.4f}]")

# Solve using matrix inverse: (A^T A)^{-1} A^T b
ATA_inv = np.linalg.inv(ATA)
flow = ATA_inv @ ATb

print(f"\n  (A^T A)^{{-1}}:")
print(f"    [{ATA_inv[0,0]:10.6f}  {ATA_inv[0,1]:10.6f}]")
print(f"    [{ATA_inv[1,0]:10.6f}  {ATA_inv[1,1]:10.6f}]")

print(f"\n  Estimated flow:  u = {flow[0]:.4f},  v = {flow[1]:.4f}")
print(f"  True flow:       u = {u_true:.4f},  v = {v_true:.4f}")
print(f"  Error:           |Δu| = {abs(flow[0]-u_true):.4e},  |Δv| = {abs(flow[1]-v_true):.4e}")

# Eigenvalue analysis (determines reliability of flow estimate)
eigenvalues = np.linalg.eigvals(ATA)
print(f"\n  Eigenvalues of A^T A: λ1 = {eigenvalues[0]:.4f}, λ2 = {eigenvalues[1]:.4f}")
print(f"  Condition number: {max(eigenvalues)/min(eigenvalues):.4f}")
print(f"  Both λ > 0 → good corner/texture region for optical flow")

# ═══════════════════════════════════════════════════════════════════════
# PART 4: Double Integral — Total Displacement Energy over 2D Region
# ═══════════════════════════════════════════════════════════════════════
# Compute the total kinetic energy proxy over (x, y) region:
# E = ∬ (vx^2 + vy^2) dx dy over the figure-8 bounding box

def velocity_magnitude_sq(x, y):
    """Squared velocity at a point on the figure-8."""
    # Parameterize: at point (x,y), find closest t
    # For simplicity, use analytic: vx = cos(t), vy = cos(2t)
    # where t = arcsin(x)
    t_approx = np.arcsin(np.clip(x, -0.99, 0.99))
    vx = np.cos(t_approx)
    vy = np.cos(2 * t_approx)
    return vx**2 + vy**2

# Double integral over bounding box [-1, 1] x [-0.5, 0.5]
E_trap = tool.integrate_double_trapezoidal(velocity_magnitude_sq, -0.9, 0.9, -0.45, 0.45, 50, 50)
E_simp = tool.integrate_double_simpson(velocity_magnitude_sq, -0.9, 0.9, -0.45, 0.45, 50, 50)

print("\n" + "=" * 60)
print("  PART 4: Double Integral — Velocity Energy over 2D Region")
print("=" * 60)
print(f"  Region: [-0.9, 0.9] x [-0.45, 0.45]")
print(f"  Trapezoidal 2D:  E = {E_trap:.6f}")
print(f"  Simpson 2D:      E = {E_simp:.6f}")
print(f"  Difference:      {abs(E_trap - E_simp):.6e}")

print("\nDONE!")
