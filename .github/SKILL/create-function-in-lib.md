---
description: How to create a new function in the tools library (lib/tools.py)
---

# Create Function in lib/tools.py

1. Open `lib/tools.py`
2. Add a new method inside the `tools` class
3. The method should:
   - Accept `self` as first parameter
   - Import any needed libraries (e.g., `import numpy as np`) inside the method
   - Include a docstring with Args and Returns
   - **Not** contain any `print()` or `plt.plot()` calls
   - Return a tuple of `(result, error_code)` where error_code=0 means success
4. Follow the existing naming conventions (e.g., `integrate_trapezoidal`, `solve_newton`)
5. Test the function by calling it from a unit test file
