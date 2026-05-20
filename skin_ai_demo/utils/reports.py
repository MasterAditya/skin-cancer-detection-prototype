# reports.py - PDF report generation for clinical analysis

import io
from datetime import datetime
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_clinical_report_pdf(
    analysis_data: dict,
    label_names: dict = None
) -> bytes:
    """
    Generate a professional PDF clinical report.
    
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
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#6db3f2'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#5b9fd4'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#d0d5dd'),
        spaceAfter=6
    )
    
    # Title
    story.append(Paragraph("Clinical AI Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = analysis_data.get("filename", "Unknown")
    story.append(Paragraph(f"<b>Report Generated:</b> {timestamp}", normal_style))
    story.append(Paragraph(f"<b>Image File:</b> {filename}", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Clinical findings
    prediction = analysis_data.get("prediction", {})
    risk_result = analysis_data.get("risk_result", {})
    
    story.append(Paragraph("Clinical Assessment", heading_style))
    story.append(Paragraph(
        f"<b>Predicted Classification:</b> {prediction.get('label', 'N/A').upper()}",
        normal_style
    ))
    story.append(Paragraph(
        f"<b>Model Confidence:</b> {prediction.get('confidence', 0)*100:.2f}%",
        normal_style
    ))
    story.append(Paragraph(
        f"<b>Risk Assessment:</b> {risk_result.get('risk', 'N/A')}",
        normal_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Clinical recommendation
    story.append(Paragraph("Recommendation", heading_style))
    story.append(Paragraph(
        risk_result.get("recommendation", "See technical details"),
        normal_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # Probability distribution table
    story.append(Paragraph("Classification Probabilities", heading_style))
    probabilities = prediction.get("probabilities", [])
    prob_data = [["Classification", "Probability"]]
    
    # Handle numpy array or dict
    if hasattr(probabilities, 'items'):
        for label, prob in probabilities.items():
            prob_data.append([label.capitalize(), f"{prob*100:.2f}%"])
    else:
        # Numpy array - use LABEL_NAMES
        from utils.constants import LABEL_NAMES
        for i, prob in enumerate(probabilities.flat if hasattr(probabilities, 'flat') else probabilities):
            if i < len(LABEL_NAMES):
                prob_data.append([LABEL_NAMES[i].capitalize(), f"{prob*100:.2f}%"])
    
    prob_table = Table(prob_data, colWidths=[3*inch, 2*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5b9fd4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#1a2635')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#404d5e')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#1a2635'), colors.HexColor('#232d3d')]),
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Images
    story.append(PageBreak())
    story.append(Paragraph("Analysis Visualization", heading_style))
    
    try:
        # Original image
        original = analysis_data.get("original_image")
        if original:
            img_buffer = io.BytesIO()
            original.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            rl_img = RLImage(img_buffer, width=3.5*inch, height=3.5*inch)
            story.append(Paragraph("Original Dermoscopic Image", normal_style))
            story.append(rl_img)
            story.append(Spacer(1, 0.15*inch))
        
        # Grad-CAM overlay
        overlay = analysis_data.get("overlay")
        if overlay:
            img_buffer = io.BytesIO()
            overlay.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            rl_img = RLImage(img_buffer, width=3.5*inch, height=3.5*inch)
            story.append(Paragraph("Grad-CAM Attention Heatmap", normal_style))
            story.append(rl_img)
    except Exception as e:
        story.append(Paragraph(f"<i>Image rendering: {str(e)}</i>", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<i>This report is for research purposes only. Clinical decisions require qualified medical review.</i>",
        normal_style
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
