from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PDF_SB = ROOT / "HSK-5-SB-2.pdf"
PDF_WB = ROOT / "HSK-5-Workbook2.pdf"
OUT_DIR = ROOT / "scripts"

def dump(pdf_path, out_path):
    if not pdf_path.exists():
        print("Not found:", pdf_path)
        return
    reader = PdfReader(str(pdf_path))
    with open(out_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages, 1):
            f.write("\n===== PAGE " + str(i) + " =====\n")
            f.write(page.extract_text() or "")
    print("Saved:", out_path, "pages:", len(reader.pages))

if __name__ == "__main__":
    dump(PDF_SB, OUT_DIR / "_sb_dump.txt")
    dump(PDF_WB, OUT_DIR / "_wb_dump.txt")
    print("Done.")