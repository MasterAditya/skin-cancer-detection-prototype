# app.py

import streamlit as st
import io

from model.loader import load_model
from model.predictor import predict_image
from utils.preprocessing import preprocess_image
from utils.constants import (
    APP_TITLE,
    APP_SUBTITLE,
    DISCLAIMER,
    MODEL_INFO,
    LABEL_NAMES
)
from decision.risk import assess_risk
from explainability.gradcam import GradCAM, overlay_heatmap
from utils.reports import generate_clinical_report_pdf, generate_gradcam_png
from utils.samples import get_sample_images, get_sample_image_description
from ui.components import (
    render_header,
    render_disclaimer,
    render_prediction_metrics,
    render_clinical_recommendation,
    render_explainability_section,
    render_technical_details,
    render_footer,
    render_image_metadata_details,
    render_compact_history,
    render_differential_diagnosis,
    render_followup_intervals
)
from ui.styling import apply_custom_css


# ========== PAGE CONFIGURATION ==========

st.set_page_config(
    page_title="Skin AI Clinical Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium CSS styling
st.markdown(apply_custom_css(), unsafe_allow_html=True)

# ========== SESSION STATE INITIALIZATION ==========

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "prediction_data" not in st.session_state:
    st.session_state.prediction_data = None
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = None
if "sample_images" not in st.session_state:
    st.session_state.sample_images = get_sample_images()
if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None
if "gradcam_data" not in st.session_state:
    st.session_state.gradcam_data = None

# ========== MODEL LOADING & INITIALIZATION ==========

@st.cache_resource
def get_model():
    """Load and cache model"""
    return load_model()

@st.cache_resource
def get_gradcam(_model):
    """Initialize Grad-CAM with model"""
    return GradCAM(
        model=_model,
        target_layer=_model.layer4[1].conv2
    )

model = get_model()
gradcam = get_gradcam(model)

# ========== MINIMAL SIDEBAR CONTROL PANEL ==========

# Upload image
uploaded_file = st.sidebar.file_uploader(
    "📁 Upload Image",
    type=["jpg", "jpeg", "png"],
    help="Dermoscopic image (JPG, PNG)"
)

st.sidebar.divider()

# Primary actions
col1, col2 = st.sidebar.columns(2, gap="small")

with col1:
    run_analysis = st.button(
        "🔍 Assess",
        use_container_width=True,
        key="analyze_button"
    )

with col2:
    if st.button("↻ Reset", use_container_width=True, key="reset_button"):
        st.session_state.analysis_complete = False
        st.session_state.prediction_data = None
        st.session_state.demo_mode = None
        st.rerun()

st.sidebar.divider()

# Collapsibles
with st.sidebar.expander("📋 History", expanded=False):
    render_compact_history(st.session_state.analysis_history)

with st.sidebar.expander("⚠️ Limitations", expanded=False):
    st.markdown(
        """
        - Research use only
        - Not validated for clinical decision
        - Variable with image quality
        - No demographic adjustment
        - No OOD detection
        """
    )

with st.sidebar.expander("⚙️ System Info", expanded=False):
    st.caption("**ResNet18 • Transfer Learning**")
    st.caption(f"Validation: 97.3%")
    st.caption(f"Training: HAM10000 + ISIC2018")
    st.caption(f"Inference: <100ms")

# ========== MAIN HEADER ==========

render_header(APP_TITLE, APP_SUBTITLE)
render_disclaimer(DISCLAIMER)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ========== MAIN TAB INTERFACE ==========

tab1, tab2, tab3 = st.tabs([
    "🔬 Clinical Assessment",
    "🔥 Explainability Analysis",
    "⚙️ Technical Intelligence"
])

# ========== TAB 1: CLINICAL ASSESSMENT ==========

with tab1:
    if uploaded_file and run_analysis:
        
        # Prepare image (from upload or demo)
        original_image, image_tensor = preprocess_image(uploaded_file)
        image_filename = uploaded_file.name
        image_size = uploaded_file.size
        
        # Run analysis with spinner
        with st.spinner("🔍 Performing AI-assisted clinical analysis..."):
            
            # Backend inference (preserved intact)
            prediction = predict_image(model, image_tensor)
            risk_result = assess_risk(
                prediction["label"],
                prediction["confidence"]
            )
            heatmap = gradcam.generate(
                image_tensor,
                prediction["class_index"]
            )
            overlay = overlay_heatmap(original_image, heatmap)
            
            # Store in session state
            st.session_state.analysis_complete = True
            st.session_state.prediction_data = {
                "original_image": original_image,
                "overlay": overlay,
                "prediction": prediction,
                "risk_result": risk_result,
                "filename": image_filename,
                "file_size": image_size,
                "heatmap": heatmap
            }
            
            # Add to history
            history_entry = {
                "label": prediction["label"],
                "confidence": prediction["confidence"],
                "timestamp": st.session_state.get("last_analysis_time", "N/A")
            }
            st.session_state.analysis_history.append(history_entry)
        
        st.success("✅ Analysis complete")
    
    # ===== DISPLAY RESULTS (if analysis is complete) =====
    if st.session_state.analysis_complete and st.session_state.prediction_data:
        # Extract data from session state
        original_image = st.session_state.prediction_data["original_image"]
        overlay = st.session_state.prediction_data["overlay"]
        prediction = st.session_state.prediction_data["prediction"]
        risk_result = st.session_state.prediction_data["risk_result"]
        image_filename = st.session_state.prediction_data["filename"]
        image_size = st.session_state.prediction_data["file_size"]
        
        # Display prediction metrics
        st.markdown("### 📋 Prediction Results")
        render_prediction_metrics(
            prediction["label"],
            prediction["confidence"],
            risk_result["risk"]
        )
        
        st.markdown("---")
        
        # Clinical recommendation
        render_clinical_recommendation(
            risk_result["recommendation"],
            risk_result["risk"]
        )
        
        st.markdown("---")
        
        # Differential diagnosis (all class probabilities)
        render_differential_diagnosis(prediction["probabilities"])
        
        st.markdown("---")
        
        # Follow-up intervals
        confidence_pct = prediction["confidence"] * 100
        render_followup_intervals(prediction["label"], confidence_pct)
        
        st.markdown("---")
        
        # Input image and metadata
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 🖼️ Input Image")
            st.image(original_image, use_container_width=True)
        with col2:
            render_image_metadata_details(
                image_filename,
                image_size,
                prediction,
                image_details={
                    "resolution": f"{original_image.size[0]}×{original_image.size[1]}",
                    "format": "PNG (internal)",
                    "mode": original_image.mode
                }
            )
        
        st.markdown("---")
        
        # Export section
        st.markdown("---")
        st.markdown("### 📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📄 Clinical Report (PDF)**")
            if st.button("Generate & Download PDF", use_container_width=True, key="export_pdf"):
                try:
                    pdf_bytes = generate_clinical_report_pdf(st.session_state.prediction_data)
                    st.session_state.pdf_data = pdf_bytes
                    st.success("✅ PDF ready to download!")
                except Exception as e:
                    st.error(f"❌ PDF Error: {str(e)}")
            
            # Show download button if PDF data exists
            if st.session_state.pdf_data:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=st.session_state.pdf_data,
                    file_name=f"clinical_report_{st.session_state.prediction_data['prediction']['label']}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="pdf_download_btn"
                )
        
        with col2:
            st.markdown("**🔥 Grad-CAM Heatmap (PNG)**")
            if st.button("Generate & Download Grad-CAM", use_container_width=True, key="export_gradcam"):
                try:
                    overlay_data = st.session_state.prediction_data.get("overlay")
                    if overlay_data is not None:
                        gradcam_bytes = generate_gradcam_png(overlay_data)
                        st.session_state.gradcam_data = gradcam_bytes
                        st.success("✅ Grad-CAM ready to download!")
                    else:
                        st.error("❌ No overlay data")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            # Show download button if Grad-CAM data exists
            if st.session_state.gradcam_data:
                st.download_button(
                    label="⬇️ Download Grad-CAM PNG",
                    data=st.session_state.gradcam_data,
                    file_name=f"gradcam_heatmap_{st.session_state.prediction_data['prediction']['label']}.png",
                    mime="image/png",
                    use_container_width=True,
                    key="gradcam_download_btn"
                )
    
    elif st.session_state.demo_mode and run_analysis:
        
        # Load demo image
        original_image = st.session_state.sample_images[st.session_state.demo_mode]
        
        # Convert PIL Image to bytes for preprocessing
        img_bytes = io.BytesIO()
        original_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Create a mock file object
        class MockFile:
            def __init__(self, image_bytes, filename):
                self.read = lambda: image_bytes.getvalue()
                self.name = filename
                self.size = len(image_bytes.getvalue())
        
        mock_file = MockFile(img_bytes, f"sample_{st.session_state.demo_mode}.png")
        
        # Run analysis with spinner
        with st.spinner("🔍 Performing AI-assisted clinical analysis (demo mode)..."):
            
            # Backend inference (preserved intact)
            original_image, image_tensor = preprocess_image(mock_file)
            prediction = predict_image(model, image_tensor)
            risk_result = assess_risk(
                prediction["label"],
                prediction["confidence"]
            )
            heatmap = gradcam.generate(
                image_tensor,
                prediction["class_index"]
            )
            overlay = overlay_heatmap(original_image, heatmap)
            
            # Store in session state
            st.session_state.analysis_complete = True
            st.session_state.prediction_data = {
                "original_image": original_image,
                "overlay": overlay,
                "prediction": prediction,
                "risk_result": risk_result,
                "filename": mock_file.name,
                "file_size": mock_file.size,
                "heatmap": heatmap
            }
            
            # Add to history
            history_entry = {
                "label": prediction["label"],
                "confidence": prediction["confidence"],
                "timestamp": "demo"
            }
            st.session_state.analysis_history.append(history_entry)
        
        st.success("✅ Demo analysis complete")
        st.info(f"Sample: {get_sample_image_description(st.session_state.demo_mode)}")
    
    else:
        st.info(
            "👆 **Getting Started**\n\n"
            "1. Upload a high-quality dermoscopic image from the sidebar\n"
            "2. Click the '🔍 Assess' button to run AI analysis\n"
            "3. View the clinical predictions and risk assessment\n"
            "4. Export the results as PDF or Grad-CAM heatmap"
        )

# ========== TAB 2: EXPLAINABILITY ==========

with tab2:
    if st.session_state.analysis_complete and st.session_state.prediction_data:
        render_explainability_section(
            st.session_state.prediction_data["original_image"],
            st.session_state.prediction_data["overlay"]
        )
    else:
        st.info(
            "Run an assessment first to view explainability analysis."
        )

# ========== TAB 3: TECHNICAL INTELLIGENCE ==========

with tab3:
    st.markdown("### 🏗️ System Architecture & Training Details")
    render_technical_details()

# ========== FOOTER ==========

st.markdown("---")
render_footer()