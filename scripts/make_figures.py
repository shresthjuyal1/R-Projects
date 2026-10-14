"""Generate the README figure from the hypothesis-test results in the report.

Uses only the Python standard library and writes an SVG to figures/.
P-values are copied from report/online_learning_survey_report.pdf.

    python3 scripts/make_figures.py
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures"

FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
INK, MUTED, GRID = "#1f2328", "#656d76", "#d0d7de"
SIG, NOT_SIG = "#1a7f37", "#8c959f"

# (survey item, one-sided p-value for H1: favourable proportion > 0.5)
ITEMS = [
    ("Used extra resources for help?", 4.433929e-05),
    ("Attend live lecture if it's recorded?", 0.0005643273),
    ("More or less stressed online?", 0.03861554),
    ("Prefer pre-recorded or live lectures?", 0.05502036),
    ("Satisfaction with online learning (1–5)", 0.6524579),
    ("Online tests reflect your knowledge?", 0.6524579),
    ("Experienced technical difficulties?", 0.9996335),
    ("Concentration during online lectures?", 0.9996335),
]


def text(x, y, s, size=13, fill=INK, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>\n')


def significance_chart():
    width, row_h = 820, 34
    left, right, top = 330, 740, 92
    height = top + row_h * len(ITEMS) + 60
    x_max = 5.0  # -log10(p)

    def px(v):
        return left + v / x_max * (right - left)

    body = text(24, 34, "Which survey items drew a significant majority response?", 18, weight="600")
    body += text(24, 56, "One-sided z-test of H₁: favourable-response proportion &gt; 50% (n = 54). Longer bar = stronger evidence.", 12, MUTED)

    axis_y = top + row_h * len(ITEMS)
    for p in (1, 0.1, 0.01, 0.001, 0.0001, 0.00001):
        v = -math.log10(p)
        body += f'<line x1="{px(v):.1f}" y1="{top - 8}" x2="{px(v):.1f}" y2="{axis_y}" stroke="{GRID}"/>\n'
        body += text(px(v), axis_y + 18, f"{p:g}", 11, MUTED, "middle")
    body += text((left + right) / 2, axis_y + 40, "p-value (log scale)", 12, MUTED, "middle")

    cut = px(-math.log10(0.05))
    body += f'<line x1="{cut:.1f}" y1="{top - 20}" x2="{cut:.1f}" y2="{axis_y}" stroke="{INK}" stroke-dasharray="4,3"/>\n'
    body += text(cut + 5, top - 10, "p = 0.05", 11, INK)

    for i, (label, p) in enumerate(ITEMS):
        y = top + i * row_h + 6
        v = -math.log10(p)
        color = SIG if p < 0.05 else NOT_SIG
        body += f'<rect x="{left}" y="{y}" width="{max(px(v) - left, 2):.1f}" height="{row_h - 12}" fill="{color}" rx="3"/>\n'
        body += text(left - 12, y + (row_h - 12) / 2 + 4, label, 12.5, INK, "end", "600" if p < 0.05 else "normal")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="{FONT}">\n'
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>\n{body}</svg>\n')


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "survey_item_tests.svg").write_text(significance_chart())
    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
