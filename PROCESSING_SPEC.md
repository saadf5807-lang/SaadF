# Medical Lecture → Exam Summary: Processing Spec

Applied identically to every lecture. Reference format: `L1 Anatomy.pdf.pdf` (place in `reference/` once available).

## Workflow
1. Drop source lecture (PDF/PPTX/text) into `lectures/`.
2. Output summary goes to `summaries/<lecture-name>.md`, one file per lecture.

## Fixed section order
1. **Title / Objectives** — lecture aims + what is likely tested.
2. **Main Content Sections** — slide-faithful, original lecture order; each section labeled by lecture part.
   Between every two consecutive topics, insert a **Transition Bridge** block:
   > 🔁 **Recap — <finished topic>:** 3–5 bullets, the core takeaways only.
   > 🔗 **Link:** 1–2 sentences on *why* the next topic follows (cause→effect, structure→function, normal→abnormal, earlier→later stage).
   > ▶️ **Up next — <next topic>:** 1–2 sentences on what it covers and what to watch for.
3. **High-Yield Comparison Tables** — labeled Table A, B, C… (relationships, derivatives, timelines, classifications, contrasts).
4. **Rules, Exceptions, Patterns** — bullets: principle → exception.
5. **Clinical Correlations** — pathology / real-world links drawn from lecture content only.
6. **Rapid Revision (Last-Day)** — ultra-condensed bullets.
7. **Exam-Style Questions** — 3–5 (MCQ + short answer), each with answer + full explanation.
8. **Exam Pitfalls & Traps** — common misconceptions / confusable pairs.

## Formatting rules
- **Bold** key terms; mark exam targets with ⭐ **HIGH-YIELD**.
- Mnemonics where they exist or aid retention (e.g., "CALMEST POSE").
- Tables preferred for any comparison.
- Numbered lists for timelines / sequences (include weeks, days, metrics exactly as given).
- Preserve every specific detail, number, and named structure from the slides.
- Precise and exam-focused; no filler.
- Content not in the lecture (added clinical context, mnemonics) is flagged as *[added]* so it is never confused with slide content.
