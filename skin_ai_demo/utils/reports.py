# reports.py - PDF report generation for clinical analysis

import io
from datetime import datetime
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas


def generate_clinical_report_pdf(
    analysis_data: dict,
    label_names: dict = None
) -> bytes:
    """
    Generate a professional PDF clinical report with medical styling.
    
    Args:
        analysis_data: Dict with keys:
            - original_image: PIL Image
            - overlay: PIL Image (Grad-CAM)
            - prediction: Dict with label, confidence, probabilities
            - risk_result: Dict with risk, recommendation
            - filename: str (original filename)
    
    Returns:
        PDF bytes ready for download
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Professional color scheme (clinical green/teal)
    PRIMARY_COLOR = '#007766'     # Clinical teal
    SECONDARY_COLOR = '#00AA88'   # Lighter teal
    TEXT_COLOR = '#1a3a3a'        # Dark text
    LIGHT_BG = '#f5f9f8'          # Light background
    
    # Custom styles - Light theme, professional
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor(PRIMARY_COLOR),
        spaceAfter=2,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subheader_style = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor(SECONDARY_COLOR),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.white,
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor(PRIMARY_COLOR),
        leftIndent=8,
        rightIndent=8,
        topPadding=6,
        bottomPadding=6
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor(TEXT_COLOR),
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor(TEXT_COLOR),
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Header with title and subtitle
    story.append(Paragraph("🔬 Skin Lesion AI Assessment", header_style))
    story.append(Paragraph("Clinical Decision Support Report", subheader_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Report details section
    prediction = analysis_data.get("prediction", {})
    risk_result = analysis_data.get("risk_result", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = analysis_data.get("filename", "Unknown")
    
    details_data = [
        ["Report ID:", f"AI-{timestamp.replace(' ', 'T').replace(':', '')}"],
        ["Report Date:", timestamp],
        ["Image File:", filename],
    ]
    
    details_table = Table(details_data, colWidths=[1.5*inch, 3.5*inch])
    details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor(PRIMARY_COLOR)),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor(TEXT_COLOR)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(LIGHT_BG)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ddeedd')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor(LIGHT_BG)]),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Clinical Assessment Section
    story.append(Paragraph("📋 Clinical Assessment", section_style))
    
    assessment_data = [
        ["Predicted Classification:", prediction.get('label', 'N/A').upper()],
        ["Model Confidence:", f"{prediction.get('confidence', 0)*100:.1f}%"],
        ["Risk Level:", risk_result.get('risk', 'UNCERTAIN')],
    ]
    
    assess_table = Table(assessment_data, colWidths=[2.5*inch, 2.5*inch])
    assess_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor(PRIMARY_COLOR)),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor(TEXT_COLOR)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafbfa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ddeedd')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(assess_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Clinical Recommendation
    story.append(Paragraph("📝 Clinical Recommendation", section_style))
    story.append(Paragraph(risk_result.get("recommendation", "See technical details"), normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Probability distribution table
    story.append(Paragraph("📊 Classification Probabilities", section_style))
    probabilities = prediction.get("probabilities", [])
    prob_data = [["Diagnosis", "Probability", "Confidence"]]
    
    # Handle numpy array or dict
    if hasattr(probabilities, 'items'):
        for label, prob in probabilities.items():
            confidence_bar = "█" * int(prob * 20) + "░" * (20 - int(prob * 20))
            prob_data.append([label.capitalize(), f"{prob*100:.1f}%", confidence_bar])
    else:
        # Numpy array - use LABEL_NAMES
        from utils.constants import LABEL_NAMES
        for i, prob in enumerate(probabilities.flat if hasattr(probabilities, 'flat') else probabilities):
            if i < len(LABEL_NAMES):
                confidence_bar = "█" * int(prob * 15) + "░" * (15 - int(prob * 15))
                prob_data.append([LABEL_NAMES[i].capitalize(), f"{prob*100:.1f}%", confidence_bar])
    
    prob_table = Table(prob_data, colWidths=[1.8*inch, 1.2*inch, 2*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PRIMARY_COLOR)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(LIGHT_BG)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ddeedd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fafbfa'), colors.HexColor(LIGHT_BG)]),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Images
    story.append(PageBreak())
    story.append(Paragraph("🔥 Explainability Analysis", section_style))
    story.append(Spacer(1, 0.15*inch))
    
    try:
        # Original image with caption
        original = analysis_data.get("original_image")
        if original is not None:
            img_buffer = io.BytesIO()
            original.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            rl_img = RLImage(img_buffer, width=3*inch, height=3*inch)
            story.append(Paragraph("<b>Original Dermoscopic Image</b>", label_style))
            story.append(rl_img)
            story.append(Spacer(1, 0.1*inch))
        
        # Grad-CAM overlay
        overlay = analysis_data.get("overlay")
        if overlay is not None:
            img_buffer = io.BytesIO()
            overlay.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            rl_img = RLImage(img_buffer, width=3*inch, height=3*inch)
            story.append(Paragraph("<b>Grad-CAM Attention Heatmap</b>", label_style))
            story.append(Paragraph("<i>Areas with warm colors indicate regions the model focuses on for diagnosis.</i>", normal_style))
            story.append(rl_img)
    except Exception as e:
        story.append(Paragraph(f"<i>Error displaying images: {str(e)}</i>", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Disclaimer Footer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    story.append(Paragraph(
        "⚠️ RESEARCH PROTOTYPE ONLY - NOT FOR CLINICAL USE",
        disclaimer_style
    ))
    story.append(Paragraph(
        "This report is generated by a research AI system and is intended for research purposes only. "
        "Clinical decisions must be made by qualified medical professionals based on comprehensive evaluation.",
        disclaimer_style
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_gradcam_png(heatmap_array) -> bytes:
    """Convert Grad-CAM heatmap to PNG bytes for download."""
    try:
        if isinstance(heatmap_array, Image.Image):
            img = heatmap_array
        else:
            # Convert numpy array to PIL Image
            img = Image.fromarray((heatmap_array * 255).astype('uint8'), mode='RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        raise ValueError(f"Failed to generate Grad-CAM PNG: {str(e)}")
