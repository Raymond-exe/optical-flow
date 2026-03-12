---
description: How to create an article for a seminar unit
---

# Create Article

1. Create a new file in `article/` named `unit<NN>.tex`
2. Use the IS&T two-column template:
   - Document class: `\documentclass[letterpaper,twocolumn,fleqn]{article}`
   - Requires `ist.sty` in the same folder
   - Standard packages: amsmath, graphicx, listings, booktabs, etc.
3. Author: `Jacky Li; Cal Poly Pomona; Pomona, California \\ <Date>`
4. Structure: Abstract → Introduction → Background/Theory → Problem Formulation → Implementation (code listings) → Results (figures) → Discussion → Conclusion → References
5. Reference template: `article/unit02.tex`
6. Figures: Use `\includegraphics[width=0.5\textwidth]{filename.png}`
7. No page numbers (`\pagestyle{empty}`)
