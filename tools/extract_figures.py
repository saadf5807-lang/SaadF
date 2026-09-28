"""Crop lecture slides into high-resolution figures: figures/<tag>/sNN.jpg.
Crop = (x0, y0, x1, y1) as fractions of the slide; default drops the title bar.
Usage: python3 tools/extract_figures.py   (requires: pip install pymupdf)"""
import os, pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DPI = 150

LECTURES = {
    "cad": ("lectures/Reihan_CAD.pdf", 0.23, {
        6: None, 8: (0, .44, 1, 1), 10: None, 12: (0, .15, 1, 1), 13: (0, 0, 1, 1),
        14: (0, 0, 1, 1), 15: (0, 0, 1, 1), 16: (0, 0, 1, 1), 17: None, 18: None,
        19: (0, .74, 1, 1), 21: None, 24: (0, 0, 1, 1), 25: None, 26: None,
        27: (.52, .2, 1, 1), 30: None, 31: (.37, .2, 1, 1), 35: (.47, .2, 1, 1), 36: None,
        37: (.4, .23, 1, 1), 39: None, 40: None, 41: None, 43: None, 44: None,
        45: (.33, .22, 1, 1), 48: None, 51: None, 53: (0, .12, 1, 1), 54: (0, .47, 1, 1),
        57: None, 58: (.64, .32, 1, .9), 59: (0, .4, 1, 1), 61: None, 62: None}),
    "cvd": ("lectures/Reihan_CVD_RR.pdf", 0.11, {
        7: (.43, .2, 1, 1), 11: None, 13: (.22, .11, 1, 1), 14: (0, 0, 1, 1),
        15: (.22, .11, 1, 1), 16: (.55, .11, 1, 1), 18: None, 29: (.48, .45, 1, .9),
        33: (.5, .15, 1, .95), 34: None}),
    "pv": ("lectures/Kotb_Pulmonary_Vascular.pdf", 0.23, {
        5: None, 6: (.63, .2, 1, 1), 7: None, 9: (.3, .23, 1, 1), 11: (.2, .23, 1, 1),
        12: (0, .4, 1, 1), 13: (0, .55, 1, 1), 14: (.36, .42, 1, 1), 15: None, 16: None,
        17: None, 18: None, 21: (0, .35, 1, 1), 22: None, 24: None, 25: (.53, .23, 1, 1),
        26: (.5, .23, 1, 1), 27: (.63, .23, 1, 1), 29: (.64, .3, 1, 1), 30: (0, .4, 1, 1),
        31: (.38, .23, 1, 1), 32: (.6, .23, 1, 1), 33: (.53, .23, 1, 1), 34: None}),
    "t1": ("lectures/Thyroid1_Goiter_TFT_Hyperthyroidism.pdf", 0.11, {
        5: (0, .11, 1, .72), 6: None, 7: (0, .11, 1, .8), 9: (.64, .11, 1, 1), 11: None,
        14: (.5, .11, 1, 1), 15: (.45, .38, 1, 1), 17: None, 18: (0, .5, 1, 1), 20: (.64, .3, 1, 1),
        27: (0, .53, 1, 1), 28: (.6, .36, 1, 1), 30: None, 31: None, 39: (0, .44, 1, 1)}),
    "t2": ("lectures/Thyroid2_Hypothyroidism_Thyroiditis_Cancer_Nodule.pdf", 0.11, {
        12: None, 14: None, 19: None, 20: None, 28: None, 30: None, 31: None,
        34: None, 35: None, 37: None, 38: None, 39: None, 40: (0, .02, 1, 1)}),
}

for tag, (src, head, pages) in LECTURES.items():
    doc = pymupdf.open(os.path.join(ROOT, src))
    out = os.path.join(ROOT, "figures", tag)
    os.makedirs(out, exist_ok=True)
    for n, crop in pages.items():
        page = doc[n - 1]
        x0, y0, x1, y1 = crop or (0, head, 1, 1)
        r = page.rect
        clip = pymupdf.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height,
                            r.x0 + x1 * r.width, r.y0 + y1 * r.height)
        page.get_pixmap(dpi=DPI, clip=clip).save(os.path.join(out, f"s{n:02d}.jpg"), jpg_quality=82)
    print(tag, len(pages), "figures")
