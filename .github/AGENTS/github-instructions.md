# GitHub Instructions — ECE 5110 Numerical Modeling

## Repository Structure

```
NumericalModeling/
├── .github/
│   ├── SKILL/                    # Workflow instructions
│   │   ├── create-function-in-lib.md
│   │   ├── create-slides.md
│   │   ├── create-article.md
│   │   └── create-unit-test.md
│   └── AGENTS/
│       └── github-instructions.md  (this file)
├── templates/                    # LaTeX templates
│   ├── article_template.tex
│   └── slides_template.tex
├── lib/
│   └── tools.py                  # All numerical methods (no plots/prints)
├── article/                      # LaTeX articles (IS&T format)
│   ├── unit02.tex
│   └── unit03.tex
├── slides/                       # LaTeX slides (extarticle landscape)
│   ├── unit02_main.tex
│   └── unit03_main.tex
├── unit01.py                     # Unit test: bisection
├── unit01_newton.py              # Unit test: Newton root finding
├── unit02.py                     # Unit test: interpolation
└── unit03.py                     # Unit test: integration + optical flow
```

## Workflow for Each Unit

1. **Add methods** to `lib/tools.py` (follow `create-function-in-lib.md`)
2. **Create unit test** `unit<NN>.py` (follow `create-unit-test.md`)
3. **Run unit test** to generate `.png` plots
4. **Create article** `article/unit<NN>.tex` (follow `create-article.md`)
5. **Create slides** `slides/unit<NN>_main.tex` (follow `create-slides.md`)
6. **Upload** `.tex` + `.png` files to Overleaf and compile

## Conventions
- Methods in `tools.py` must NOT contain `print()` or `plt` calls
- Unit tests CAN have plots and prints
- Author: **Jacky Li**
- All `.tex` files should compile standalone on Overleaf
