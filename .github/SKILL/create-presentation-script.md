---
description: How to create a presentation script with speaker notes for a seminar unit
---

# Create Presentation Script

Use this skill to generate a `.tex` file containing **slide content + word-for-word speaker notes** for a group presentation.

## Steps

1. **Copy the template**
   ```
   cp templates/presentation_template.tex slides/unit<NN>_presentation.tex
   ```

2. **Fill in placeholders**
   Replace every `<<...>>` marker:
   - `<<NN>>` → unit number (e.g., `03`)
   - `<<SEMINAR TITLE>>` → main title
   - `<<UNIT TOPIC>>` → subtitle from the syllabus
   - `<<SPEAKER_1>>` through `<<SPEAKER_7>>` → actual names
   - `<<Date>>` → presentation date
   - Equations, code listings, figure paths, bullet points

3. **Assign slides to speakers** (~2 slides per person for 7 speakers / 15 slides)
   - Speaker 1: Title + Outline + one Results slide
   - Speaker 2: Introduction + one Results slide
   - Speaker 3: Theory slides (×2)
   - Speaker 4: Problem Definition + Live Demo
   - Speaker 5: Matrix / Formula + Comparison Table
   - Speaker 6: Implementation slides (×2)
   - Speaker 7: Additional Code + Conclusion

4. **Write speaker notes** using the `\speakernotes{Name}{...}` command:
   - Write complete sentences — the speaker reads this verbatim
   - Include `[DEMO CUE: ...]` markers for live demonstrations
   - Reference slide content explicitly ("as you can see on the left panel…")
   - Transition to next speaker at the end ("Now I'll hand it to …")

5. **Include both formats** on every slide:
   - **Bullet points** (visible on projected slide)
   - **Verbatim speech** (inside `\speakernotes{}`, printed below the slide)

6. **Toggle notes visibility**
   - `\shownotestrue` → prints notes (for rehearsal / speaker copy)
   - `\shownotesfalse` → hides notes (for projector PDF)

7. **Reference demos**
   - Add a dedicated Demo slide with pipeline bullets
   - Include `[DEMO CUE]` markers in the speaker notes
   - List the demo script filename (e.g., `webcam_demo.py`)

8. **Compile in Overleaf** — upload the `.tex` file plus all referenced `.png` figures and `cpp_logo.png`

## File Naming
```
slides/unit<NN>_presentation.tex
```

## Reference
- Template: `templates/presentation_template.tex`
- Example: `slides/unit03_presentation.tex`
