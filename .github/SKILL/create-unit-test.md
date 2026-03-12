---
description: How to create a unit test file
---

# Create Unit Test

1. Create a new file in the project root named `unit<NN>.py`
2. Structure:
   ```python
   from lib.tools import tools
   import numpy as np
   import matplotlib.pyplot as plt

   tool = tools()
   ```
3. Define the test problem (choose an EE-relevant application)
4. Call the methods from `tools.py` — do NOT re-implement them
5. Print results with clear formatting (use `=` and `-` borders)
6. Generate plots with:
   - `plt.savefig('unit<NN>_<description>.png', dpi=150)` for the article/slides
   - `plt.show()` for interactive viewing
7. End with `print("DONE!")`
8. Test by running: `python3 unit<NN>.py`
