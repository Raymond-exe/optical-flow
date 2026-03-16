# Presentation Script Workflow — ECE 5110

## When to Use
Use this workflow when preparing a **group presentation** for any unit seminar.

## Inputs
| Input | Example |
|-------|---------|
| Unit number | `03` |
| Topic | Numerical Differentiation & Integration |
| Speakers | Josiah, Jake, Jack, Jacky, Virgil, Elijah, Richie |
| Demo script (optional) | `webcam_demo.py` |

## Workflow

1. **Run the unit test** to generate all `.png` plots:
   ```
   python unit<NN>.py
   ```
2. **Read the existing slides** `slides/unit<NN>_main.tex` for slide content reference.
3. **Copy the template**:
   ```
   cp templates/presentation_template.tex slides/unit<NN>_presentation.tex
   ```
4. **Follow the SKILL** `.github/SKILL/create-presentation-script.md` to fill in all placeholders — equations, code, figures, speaker notes.
5. **Assign speakers** — distribute slides evenly (~2 per person).
6. **Write verbatim speech** for every slide using `\speakernotes{Name}{...}`.
7. **Add demo cues** if the unit has a live demo:
   - Insert `[DEMO CUE: ...]` in the speaker notes
   - Create a dedicated Demo slide
8. **Compile** — upload to Overleaf with `.png` files and `cpp_logo.png`.
9. **Generate two PDFs**:
   - `\shownotestrue` → speaker copy (with notes)
   - `\shownotesfalse` → projector copy (slides only)

## Output Files
```
slides/unit<NN>_presentation.tex   # Full script with notes
```

## References
- Template: `templates/presentation_template.tex`
- SKILL: `.github/SKILL/create-presentation-script.md`
- Example: `slides/unit03_presentation.tex`
