from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from fpdf import FPDF

from app.schemas import ComicLayout


def save_pdf(
    layout: ComicLayout,
    static_dir: Path,
    exports_dir: Path,
) -> str:
    exports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"comic_{uuid4().hex}.pdf"
    output_path = exports_dir / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout.panels:
        pdf.add_page()
        pdf.set_font("helvetica", style="B", size=16)
        pdf.multi_cell(
            0,
            10,
            f"Panel {panel.panel_number}: {panel.title}",
        )

        image_name = Path(urlparse(panel.image_url).path).name
        image_path = static_dir / "panels" / image_name
        if image_path.is_file():
            image_width = 180
            image_x = (pdf.w - image_width) / 2
            pdf.image(str(image_path), x=image_x, w=image_width)
            pdf.ln(4)

        pdf.set_font("helvetica", size=11)
        for label, text in (
            ("Scene", panel.scene_description),
            ("Caption", panel.caption),
            ("Narration", panel.narration),
            ("Dialogue", panel.dialogue),
            ("Image Prompt Reference", panel.image_prompt),
        ):
            if text:
                pdf.set_font("helvetica", style="B", size=11)
                pdf.write(6, f"{label}: ")
                pdf.set_font("helvetica", size=11)
                pdf.multi_cell(0, 6, text)
                pdf.ln(2)

    pdf.output(str(output_path))
    return filename