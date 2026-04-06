class tools:
    def get_val(self, f, x):
        return f(x)
    def solve_bisection_rec(self, f, a, b, precision, max_steps):
        if max_steps <= 0:
            return 0, -2
        if a > b:
            return 0, -1
        if f(a)*f(b) >= 0:
            return 0, -1
        
        if abs(f(a)) < precision:
            return a, 0
        if abs(f(b)) < precision:
            return b, 0

        mid = (a + b) / 2
        if f(a)*f(mid) > 0:
            return self.solve_bisection_rec(f, mid, b, precision, max_steps - 1)

        return self.solve_bisection_rec(f, a, mid, precision, max_steps - 1)

    def solve_bisection_loop(self, f, a, b, precision, max_steps=100):
        if abs(f(a)) < precision:
            return a, 0
        if abs(f(b)) < precision:
            return b, 0
        if f(a)*f(b) >= 0:
            return 0, -1

        for _ in range(max_steps):
            c = (a + b) / 2.0
            if abs(f(c)) < precision:
                return c, 0
            if f(a)*f(c) < 0:
                b = c
            else:
                a = c
        return  (a+b)/2.0, 0  

    def solve_newton(self, f, df, x0, precision=1e-6, max_steps=100):
        """Newton's method for finding roots of f(x) = 0.

        Args:
            f:  The function whose root we seek.
            df: The derivative of f.
            x0: Initial guess.
            precision: Stopping tolerance on |f(x)|.
            max_steps: Maximum number of iterations.

        Returns:
            (solution, error_code, history)
            error_code:  0 = converged, -1 = did not converge, -2 = zero derivative
            history: list of (step, x, f(x)) tuples
        """
        x = x0
        history = []

        for step in range(1, max_steps + 1):
            fx = f(x)
            dfx = df(x)

            history.append((step, x, fx))

            if abs(fx) < precision:
                return x, 0, history

            if abs(dfx) < 1e-15:
                return x, -2, history

            x = x - fx / dfx

        # Final check after last iteration
        fx = f(x)
        history.append((max_steps + 1, x, fx))
        if abs(fx) < precision:
            return x, 0, history

        return x, -1, history

    def solve_lsoe(self, A, B):
        """Solve a linear system Ax = B using Gaussian elimination
        with scaled partial pivoting + back substitution.

        Based on the MATLAB function_solve_lsoe from ECE 5110.

        Steps:
            1. Row normalization (scale each row by its max abs value)
            2. Partial pivoting (swap rows to maximize pivot)
            3. Forward elimination (zero out below-diagonal entries)
            4. Back substitution (solve the upper-triangular system)

        Args:
            A: n×n coefficient matrix (list of lists or numpy array).
            B: n×1 right-hand side vector.

        Returns:
            (solution, error_code)
            error_code:  0 = success, -1 = singular or incompatible
        """
        import numpy as np

        A = np.array(A, dtype=np.float64)
        B = np.array(B, dtype=np.float64).flatten()
        n = A.shape[0]

        # Dimension check
        if A.shape[0] != A.shape[1] or len(B) != n:
            return np.zeros(n), -1

        # ─── Forward Elimination ───
        for ix in range(n - 1):
            # 1. NORMALIZE — scale rows ix..n-1 by their max absolute value
            for r in range(ix, n):
                max_row = np.max(np.abs(A[r, ix:]))
                if max_row < 1e-15:
                    continue  # skip near-zero rows
                A[r, ix:] = A[r, ix:] / max_row
                B[r] = B[r] / max_row

            # 2. PARTIAL PIVOTING — find the row with largest |A[r, ix]|
            pivot_row = ix + np.argmax(np.abs(A[ix:, ix]))
            if pivot_row != ix:
                # Swap rows in A and B
                A[[ix, pivot_row]] = A[[pivot_row, ix]]
                B[[ix, pivot_row]] = B[[pivot_row, ix]]

            # Check for zero pivot (singular matrix)
            if abs(A[ix, ix]) < 1e-15:
                return np.zeros(n), -1

            # 3. ELIMINATE — zero out entries below A[ix, ix]
            for r in range(ix + 1, n):
                factor = A[r, ix] / A[ix, ix]
                A[r, ix:] = A[r, ix:] - factor * A[ix, ix:]
                B[r] = B[r] - factor * B[ix]

        # Check last pivot
        if abs(A[n - 1, n - 1]) < 1e-15:
            return np.zeros(n), -1

        # ─── 4. BACK SUBSTITUTION ───
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (B[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

        return x, 0

    def lagrange_interpolate(self, x, y):
        import numpy as np
        n = len(x)
        P = np.zeros(n)

        for i in range(n):
            Li = np.array([1.0])
            denom = 1.0

            for j in range(n):
                if i != j:
                    Li = np.convolve(Li, np.array([1.0, -x[j]]))
                    denom *= (x[i] - x[j])

            P = P + Li * (y[i] / denom)

        return P, 0

    def newton_interpolate(self, x, y):
        """Newton's divided-difference interpolation.

        Args:
            x: array of x data points
            y: array of y data points

        Returns:
            (P, error_code)
            P: polynomial coefficients (highest degree first, for np.polyval)
            error_code: 0 = success
        """
        import numpy as np
        n = len(x)

        # Build divided difference table
        dd = np.copy(y).astype(float)
        coefs = [dd[0]]
        for j in range(1, n):
            for i in range(n - 1, j - 1, -1):
                dd[i] = (dd[i] - dd[i - 1]) / (x[i] - x[i - j])
            coefs.append(dd[j])

        # Convert Newton form to standard polynomial coefficients
        # P(x) = c0 + c1*(x-x0) + c2*(x-x0)*(x-x1) + ...
        P = np.array([coefs[0]])
        basis = np.array([1.0])
        for k in range(1, n):
            basis = np.convolve(basis, np.array([1.0, -x[k - 1]]))
            P = np.polyadd(P, coefs[k] * basis)

        return P, 0

    # ══════════════════════════════════════════════════════════════
    # Unit 3: Numerical Integration (Single Integral — 4 forms)
    # ══════════════════════════════════════════════════════════════

    def integrate_trapezoidal(self, f, a, b, n):
        """Composite trapezoidal rule for integral of f from a to b."""
        import numpy as np
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        return h * (y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2)

    def integrate_simpson13(self, f, a, b, n):
        """Composite Simpson's 1/3 rule (n must be even)."""
        import numpy as np
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        return (h / 3) * (y[0] + 4 * np.sum(y[1::2]) + 2 * np.sum(y[2:-1:2]) + y[-1])

    def integrate_simpson38(self, f, a, b, n):
        """Composite Simpson's 3/8 rule (n must be multiple of 3)."""
        import numpy as np
        while n % 3 != 0:
            n += 1
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])
        result = y[0] + y[-1]
        for i in range(1, n):
            if i % 3 == 0:
                result += 2 * y[i]
            else:
                result += 3 * y[i]
        return (3 * h / 8) * result

    def integrate_midpoint(self, f, a, b, n):
        """Composite midpoint rule for integral of f from a to b."""
        import numpy as np
        h = (b - a) / n
        result = 0.0
        for i in range(n):
            mid = a + (i + 0.5) * h
            result += f(mid)
        return h * result

    # ══════════════════════════════════════════════════════════════
    # Unit 3: Numerical Integration (Double Integral — 2 forms)
    # ══════════════════════════════════════════════════════════════

    def integrate_double_trapezoidal(self, f, ax, bx, ay, by, nx, ny):
        """Composite trapezoidal rule for double integral."""
        import numpy as np
        hx = (bx - ax) / nx
        hy = (by - ay) / ny
        result = 0.0
        for i in range(nx + 1):
            for j in range(ny + 1):
                xi = ax + i * hx
                yj = ay + j * hy
                w = 1.0
                if i == 0 or i == nx:
                    w *= 0.5
                if j == 0 or j == ny:
                    w *= 0.5
                result += w * f(xi, yj)
        return hx * hy * result

    def integrate_double_simpson(self, f, ax, bx, ay, by, nx, ny):
        """Composite Simpson's rule for double integral (nx, ny must be even)."""
        import numpy as np
        if nx % 2 != 0:
            nx += 1
        if ny % 2 != 0:
            ny += 1
        hx = (bx - ax) / nx
        hy = (by - ay) / ny
        result = 0.0
        for i in range(nx + 1):
            for j in range(ny + 1):
                xi = ax + i * hx
                yj = ay + j * hy
                if i == 0 or i == nx:
                    wx = 1
                elif i % 2 == 1:
                    wx = 4
                else:
                    wx = 2
                if j == 0 or j == ny:
                    wy = 1
                elif j % 2 == 1:
                    wy = 4
                else:
                    wy = 2
                result += wx * wy * f(xi, yj)
        return (hx * hy / 9) * result

    # ══════════════════════════════════════════════════════════════
    # Unit 3: Numerical Differentiation
    # ══════════════════════════════════════════════════════════════

    def differentiate(self, y, h, method='central'):
        """Numerical differentiation using finite differences.

        Args:
            y: array of function values at equally-spaced points
            h: step size
            method: 'forward', 'backward', or 'central'

        Returns:
            dy: array of derivative approximations
        """
        import numpy as np
        n = len(y)
        dy = np.zeros(n)

        if method == 'forward':
            for i in range(n - 1):
                dy[i] = (y[i + 1] - y[i]) / h
            dy[-1] = dy[-2]
        elif method == 'backward':
            for i in range(1, n):
                dy[i] = (y[i] - y[i - 1]) / h
            dy[0] = dy[1]
        else:  # central
            for i in range(1, n - 1):
                dy[i] = (y[i + 1] - y[i - 1]) / (2 * h)
            dy[0] = (y[1] - y[0]) / h
            dy[-1] = (y[-1] - y[-2]) / h

        return dy

    def optical_flow_lk(self, frame1, frame2, win=7, levels=3):
        """Pyramidal Lucas-Kanade optical flow (Bouguet, 2001).

        Uses a Gaussian image pyramid with `levels` scales.
        Spatial gradients use self.differentiate (central differences).
        Flow is computed coarse-to-fine: estimate at the top level, then
        upsample and refine at each finer level.
        """
        import numpy as np
        import cv2

        # Ensure float32 and clean NaN/Inf
        f1 = np.nan_to_num(np.float32(frame1), nan=0.0, posinf=0.0, neginf=0.0)
        f2 = np.nan_to_num(np.float32(frame2), nan=0.0, posinf=0.0, neginf=0.0)

        # Build Gaussian pyramids
        pyr1 = [cv2.GaussianBlur(f1, (5, 5), 0)]
        pyr2 = [cv2.GaussianBlur(f2, (5, 5), 0)]
        for _ in range(1, levels):
            pyr1.append(cv2.pyrDown(pyr1[-1]))
            pyr2.append(cv2.pyrDown(pyr2[-1]))

        # Initialize flow at coarsest level
        u = np.zeros(pyr1[-1].shape, dtype=np.float32)
        v = np.zeros(pyr1[-1].shape, dtype=np.float32)

        # Coarse-to-fine: compute/refine flow at each level
        for lev in range(levels - 1, -1, -1):
            p1 = pyr1[lev]
            p2 = pyr2[lev]
            h_rows, w_cols = p1.shape

            # Upsample previous level's flow to current resolution
            if u.shape != p1.shape:
                u = cv2.resize(u, (w_cols, h_rows)) * 2.0
                v = cv2.resize(v, (w_cols, h_rows)) * 2.0

            # Spatial gradients using OUR differentiate method
            Ix = np.zeros_like(p2)
            for r in range(h_rows):
                Ix[r, :] = self.differentiate(p2[r, :], 1.0, method='central')
            Iy = np.zeros_like(p2)
            for c in range(w_cols):
                Iy[:, c] = self.differentiate(p2[:, c], 1.0, method='central')

            # Temporal gradient with auto-exposure compensation
            It = p2 - p1
            It = It - np.mean(It)

            # Compute flow refinement at this level
            du, dv = self.lucas_kanade_matrix(Ix, Iy, It, win)
            u = u + du
            v = v + dv

        return u, v

    def lucas_kanade_matrix(self, Ix, Iy, It, win=7):
        import numpy as np
        h, w = Ix.shape
        u = np.zeros((h, w), dtype=np.float32)
        v = np.zeros((h, w), dtype=np.float32)
        half = win // 2
        tau = 0.5  # eigenvalue threshold (higher = less noise)

        for y in range(half, h - half):
            for x in range(half, w - half):
                ix = Ix[y-half:y+half+1, x-half:x+half+1].flatten()
                iy = Iy[y-half:y+half+1, x-half:x+half+1].flatten()
                it = It[y-half:y+half+1, x-half:x+half+1].flatten()

                # Skip windows with NaN/Inf
                if not (np.all(np.isfinite(ix)) and np.all(np.isfinite(iy))
                        and np.all(np.isfinite(it))):
                    continue

                # Build A^T A directly (2x2) — faster than full matmul
                sxx = np.dot(ix, ix)
                sxy = np.dot(ix, iy)
                syy = np.dot(iy, iy)

                # Fast eigenvalue check for 2x2: both eigenvalues > tau
                # if trace > 2*tau and determinant > tau^2
                trace = sxx + syy
                det = sxx * syy - sxy * sxy
                if trace < 2 * tau or det < tau * tau:
                    continue

                # Solve [sxx sxy; sxy syy] * [u; v] = -[dot(ix,it); dot(iy,it)]
                bx = -np.dot(ix, it)
                by = -np.dot(iy, it)

                inv_det = 1.0 / det
                u[y, x] = inv_det * (syy * bx - sxy * by)
                v[y, x] = inv_det * (-sxy * bx + sxx * by)

        return u, v
