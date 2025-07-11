from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel, Field
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from typing import Optional
from io import BytesIO
import os

app = FastAPI(
    title="LC Draft Generator",
    description="Creates LC draft as 2-page PDF with fields and background",
    version="1.0.0"
)

class LCDraftData(BaseModel):
    document_credit_no: Optional[str] = ""
    date_of_issue: Optional[str] = ""
    applicant: Optional[str] = ""
    beneficiary: Optional[str] = ""
    currency_amount: Optional[str] = ""
    available_with: Optional[str] = ""
    drafts_at: Optional[str] = ""
    drawee: Optional[str] = ""
    partial_shipments: Optional[str] = ""
    transshipment: Optional[str] = ""
    port_of_loading: Optional[str] = ""
    port_of_discharge: Optional[str] = ""
    latest_shipment_date: Optional[str] = ""
    goods_description: Optional[str] = ""
    documents_required: Optional[str] = ""
    additional_conditions: Optional[str] = ""
    charges: Optional[str] = ""
    presentation_period: Optional[str] = ""
    confirmation: Optional[str] = ""
    negotiating_bank_instructions: Optional[str] = ""
    advise_through: Optional[str] = ""
    goods_quantity: Optional[str] = ""
    goods_price: Optional[str] = ""
    goods_incoterm: Optional[str] = ""

@app.post("/generate-lc-draft-pdf/")
def generate_lc_pdf(data: LCDraftData):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        def draw_image(path):
            if os.path.exists(path):
                c.drawImage(ImageReader(path), 0, 0, width=width, height=height)
            else:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(100, 800, f"⚠️ Missing background: {path}")

        def draw_text(value, x, y):
            c.setFont("Helvetica", 8)
            c.drawString(x, y, value)

        # === Page 1 ===
        bg1 = os.path.join("static", "1.jpg")
        draw_image(bg1)
        draw_text(data.document_credit_no, 200, 710)
        draw_text(data.date_of_issue, 220, 690)
        draw_text(data.applicant, 80, 580)
        draw_text(data.beneficiary, 80, 540)
        draw_text(data.currency_amount, 240, 530)
        draw_text(data.available_with, 80, 490)
        draw_text(data.drafts_at, 400, 470)
        draw_text(data.drawee, 380, 450)
        draw_text(data.partial_shipments, 340, 420)
        draw_text(data.transshipment, 340, 390)
        draw_text(data.port_of_loading, 460, 370)
        draw_text(data.port_of_discharge, 560, 340)
        draw_text(data.latest_shipment_date, 360, 310)
        draw_text(data.goods_description, 240, 290)
        draw_text(data.goods_quantity, 120, 260)
        draw_text(data.goods_price, 100, 250)
        draw_text(data.goods_incoterm, 130, 230)
        c.showPage()

        # === Page 2 ===
        bg2 = os.path.join("static", "2.jpg")
        draw_image(bg2)
        draw_text(data.additional_conditions, 240, 610)
        draw_text(data.charges, 160, 510)
        draw_text(data.presentation_period, 420, 410)
        draw_text(data.confirmation, 210, 380)
        draw_text(data.advise_through, 180, 160)

        c.save()
        buffer.seek(0)

        return Response(
            content=buffer.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=lc_draft.pdf"}
        )
    except Exception as e:
        print("⚠️ PDF generation failed:", str(e))
        raise HTTPException(status_code=500, detail="PDF generation failed")
