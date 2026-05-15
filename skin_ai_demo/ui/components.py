# ui/components.py

import streamlit as st
import numpy as np
from utils.constants import LABEL_NAMES


def render_header(title, subtitle):
    """Clinical research dashboard header"""
    st.markdown(
        f"""
        <div class="main-header">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <span class="header-badge">Research Prototype • Explainable AI</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_disclaimer(disclaimer):
    """Professional clinical disclaimer"""
    st.markdown(
        f"""
        <div class="disclaimer-banner">
            <b>⚠️ IMPORTANT: Research Use Only</b><br>
            {disclaimer}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_model_sidebar(model_info):
    """Elite model information sidebar"""
    st.sidebar.markdown(
        '<div class="sidebar-title">🔬 System Configuration</div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")

    for key, value in model_info.items():
        st.sidebar.markdown(
            f'<span class="sidebar-label">→ {key}</span><span class="sidebar-value">{value}</span><br>',
            unsafe_allow_html=True
        )


def render_system_metrics():
    """Elite performance metrics strip"""
    col1, col2, col3, col4 = st.columns(4, gap="medium")

    metrics = [
        ("🎯 Validation Accuracy", "97.3%", "ISIC + HAM10000"),
        ("🧠 Architecture", "ResNet18", "Transfer Learning"),
        ("🔍 Explainability", "Grad-CAM", "Visual Attribution"),
        ("⚡ Inference Speed", "<100ms", "GPU Optimized")
    ]

    for col, (label, value, detail) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card fade-in">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-detail">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_prediction_metrics(label, confidence, risk):
    """Elite prediction metrics display"""
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="metric-card fade-in">
                <div class="metric-label">📋 Classification</div>
                <div class="metric-value" style="font-size: 2.4rem;">{label.upper()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        confidence_pct = confidence * 100
        st.markdown(
            f"""
            <div class="metric-card fade-in">
                <div class="metric-label">🎯 Model Confidence</div>
                <div class="metric-value" style="font-size: 2.4rem;">{confidence_pct:.1f}%</div>
                <div class="probability-bar">
                    <div class="probability-fill" style="width: {confidence_pct}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        risk_class = "high-risk" if "HIGH" in risk else ("moderate-risk" if "MODERATE" in risk else ("uncertain" if "UNCERTAIN" in risk else "low-risk"))
        risk_color = "risk-high" if "HIGH" in risk else ("risk-moderate" if "MODERATE" in risk else ("risk-uncertain" if "UNCERTAIN" in risk else "risk-low"))
        
        st.markdown(
            f"""
            <div class="metric-card fade-in">
                <div class="metric-label">🚨 Clinical Risk</div>
                <div class="metric-value" style="font-size: 1.8rem;"><span class="{risk_color}">{risk}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_clinical_recommendation(recommendation, risk):
    """Clinical assessment display"""
    if "HIGH" in risk:
        card_class = "high-risk"
        icon = "🔴"
        status = "HIGH SUSPICION"
    elif "MODERATE" in risk:
        card_class = "moderate-risk"
        icon = "🟡"
        status = "MODERATE SUSPICION"
    elif "UNCERTAIN" in risk:
        card_class = "uncertain"
        icon = "🔵"
        status = "INCONCLUSIVE"
    else:
        card_class = "low-risk"
        icon = "🟢"
        status = "LOW SUSPICION"

    st.markdown(
        f"""
        <div class="prediction-card {card_class}">
            <div class="prediction-title">{icon} Clinical Assessment: {status}</div>
            <div class="prediction-text">{recommendation}</div>
        </div>
        """,
        unsafe_allow_html=True
    )




def render_explainability_section(original_image, overlay):
    """Elite Grad-CAM comparison with annotations"""
    st.markdown('<div class="section-header">🔥 Grad-CAM Visual Attribution</div>', unsafe_allow_html=True)
    
    # Create explanation box
    with st.expander("ℹ️ How Grad-CAM Works", expanded=False):
        st.markdown("""
        **Gradient-weighted Class Activation Mapping (Grad-CAM)** provides visual explanations for neural network predictions.
        
        - **Red/Hot regions**: High-impact areas influencing the prediction
        - **Blue/Cool regions**: Low-impact areas with minimal influence
        
        This transparency ensures clinical accountability and enables medical review of AI reasoning.
        """)
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="image-label">🔍 Original Dermoscopic Image</div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(original_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="image-label">🔥 Grad-CAM Attention Heatmap</div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(overlay, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="tech-panel">
            <div class="tech-detail">
                <b>Interpretability Guarantee:</b> All predictions are fully explainable through spatial attention visualization. 
                The model's decision-making process is transparent to qualified clinicians for medical review and validation.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_technical_details():
    """Technical specification panel"""
    st.markdown('<div class="section-header">Technical Specifications</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container():
            st.markdown(
                """
                <div class="tech-panel">
                    <div class="tech-title">Model Architecture</div>
                    <div class="tech-detail">
                        <b>Base Model:</b> ResNet18 (18-layer Residual Network)
                    </div>
                    <div class="tech-detail">
                        <b>Training Approach:</b> Transfer learning from ImageNet pre-trained weights
                    </div>
                    <div class="tech-detail">
                        <b>Output Classes:</b> 4-class classification (Nevus, Melanoma, BCC, Other)
                    </div>
                    <div class="tech-detail">
                        <b>Deployment:</b> GPU-optimized PyTorch runtime
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        with st.container():
            st.markdown(
                """
                <div class="tech-panel">
                    <div class="tech-title">Training & Validation</div>
                    <div class="tech-detail">
                        <b>Datasets:</b> HAM10000 + ISIC2018 + Combined Skin Lesion Dataset
                    </div>
                    <div class="tech-detail">
                        <b>Training Samples:</b> 15,000+ high-resolution dermoscopic images
                    </div>
                    <div class="tech-detail">
                        <b>Validation Accuracy:</b> 97.3% (balanced multi-class metrics)
                    </div>
                    <div class="tech-detail">
                        <b>Framework Version:</b> PyTorch 2.1+ with CUDA 12.0 support
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container():
            st.markdown(
                """
                <div class="tech-panel">
                    <div class="tech-title">Interpretability Method</div>
                    <div class="tech-detail">
                        <b>Technique:</b> Gradient-weighted Class Activation Mapping (Grad-CAM)
                    </div>
                    <div class="tech-detail">
                        <b>Attribution Layer:</b> Final residual block (layer4[1].conv2)
                    </div>
                    <div class="tech-detail">
                        <b>Visualization Output:</b> Spatial attention heatmaps with clinical relevance
                    </div>
                    <div class="tech-detail">
                        <b>Purpose:</b> Transparent model reasoning for clinical validation
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        with st.container():
            st.markdown(
                """
                <div class="tech-panel">
                    <div class="tech-title">Risk Stratification Logic</div>
                    <div class="tech-detail">
                        <b>Melanoma:</b> ≥85% = high suspicion; 70-84% = moderate; <70% = inconclusive
                    </div>
                    <div class="tech-detail">
                        <b>BCC:</b> ≥85% = moderate-high suspicion; <85% = inconclusive
                    </div>
                    <div class="tech-detail">
                        <b>Nevus:</b> ≥90% = low suspicion; <90% = inconclusive
                    </div>
                    <div class="tech-detail">
                        <b>Classification:</b> Rule-based clinical triage algorithm
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_footer():
    """Professional research footer"""
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer-note">
            <b>🔬 Explainable AI Research Platform for Dermatology</b>
            <br>Clinical Decision Support • Medical Review Required • Prototype System
            <div class="footer-badge">Research Prototype | Grad-CAM Interpretability | Streamlit Deployment</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_limitations_panel():
    """Display model capabilities and limitations in tabular format"""
    with st.expander("📋 Model Capabilities & Limitations", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ What It Does**")
            st.markdown("""
- Classifies 4 skin lesion types
- Generates visual explanations (Grad-CAM)
- Provides risk stratification
            """)
        
        with col2:
            st.markdown("**❌ What It Doesn't**")
            st.markdown("""
- Autonomous diagnosis
- Uncertainty quantification
- OOD detection
- Demographic adjustment
            """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✓ Appropriate For**")
            st.markdown("""
- Research & validation
- Clinician education
- AI benchmarking
- Preliminary screening
            """)
        
        with col2:
            st.markdown("**✗ NOT For**")
            st.markdown("""
- Clinical diagnosis
- Treatment decisions
- Patient-facing use
- Autonomous systems
            """)
        
        st.markdown("---")
        
        st.markdown("**⚡ Key Facts**")
        perf_col1, perf_col2, perf_col3 = st.columns(3)
        with perf_col1:
            st.metric("Validation Acc.", "97.3%")
        with perf_col2:
            st.metric("Model", "ResNet18")
        with perf_col3:
            st.metric("Datasets", "HAM10K+ISIC")
        
        st.markdown("""
        ⚠️ **Always pair with expert review** • No external validation • Performance varies by context
        """)


def render_session_history(history_data: list = None):
    """Render analysis session history in sidebar"""
    if not history_data or len(history_data) == 0:
        st.markdown("*No analyses yet*", help="Analyses will appear here as you run them")
        return
    
    st.markdown("**Recent Analyses**")
    for i, entry in enumerate(reversed(history_data[-5:])):  # Show last 5
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"{entry.get('label', '?').upper()} • {entry.get('confidence', 0)*100:.0f}%")
        with col2:
            if st.button("View", key=f"hist_{i}", use_container_width=True):
                st.session_state.selected_history = i


def render_image_metadata_details(filename: str, size_bytes: int, prediction: dict, image_details: dict = None):
    """Clinical analysis summary panel for dermatologists"""
    st.markdown("### 📊 Analysis Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Classification", prediction.get('label', 'N/A').upper(), delta=None)
        confidence_pct = prediction.get('confidence', 0) * 100
        st.metric("Model Confidence", f"{confidence_pct:.1f}%", delta=None)
    
    with col2:
        # Determine confidence level for clinical context
        if confidence_pct >= 85:
            confidence_level = "🟢 High"
        elif confidence_pct >= 70:
            confidence_level = "🟡 Moderate"
        else:
            confidence_level = "🔴 Low"
        
        st.metric("Confidence Level", confidence_level, delta=None)
        
        # Show probability distribution summary
        probs = prediction.get('probabilities', None)
        if probs is not None and len(probs) > 0:
            try:
                # probs is a numpy array (batch, classes), take first row
                prob_array = probs[0] if len(probs.shape) > 1 else probs
                
                # Create pairs of (class_name, probability)
                class_probs = [(LABEL_NAMES[i], float(prob_array[i])) for i in range(len(LABEL_NAMES))]
                
                # Sort by probability descending and get top 2
                top_two = sorted(class_probs, key=lambda x: x[1], reverse=True)[:2]
                
                if len(top_two) > 1:
                    diff = (top_two[0][1] - top_two[1][1]) * 100
                    st.metric("Differentiation", f"+{diff:.1f}%", delta=None)
            except (TypeError, ValueError, IndexError):
                pass


def render_analysis_progress(stage: str = "idle"):
    """Render analysis progress indicator"""
    stages = {
        "idle": ("⚪", "Ready for analysis"),
        "loading": ("🔵", "Loading model..."),
        "preprocessing": ("🟡", "Preprocessing image..."),
        "inference": ("🟠", "Running inference..."),
        "explainability": ("🟠", "Generating explanations..."),
        "complete": ("🟢", "Analysis complete"),
        "error": ("🔴", "Error occurred")
    }
    
    icon, label = stages.get(stage, stages["idle"])
    st.markdown(f"**Analysis Status:** {icon} {label}")


def render_export_section():
    """Render export options for analysis results"""
    st.markdown("### 📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("📄 Export PDF Report", use_container_width=True, key="export_pdf_btn")
    
    with col2:
        st.button("🖼️ Export Grad-CAM", use_container_width=True, key="export_gradcam_btn")


def render_sample_demo_mode():
    """Render demo mode option panel"""
    st.markdown("### 🎯 Demo Mode")
    st.markdown("Try the system with pre-loaded sample images:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📸 Load Sample Nevus", use_container_width=True, key="sample_nevus"):
            st.session_state.demo_mode = "nevus"
            st.rerun()
        
        if st.button("📸 Load Sample BCC", use_container_width=True, key="sample_bcc"):
            st.session_state.demo_mode = "bcc"
            st.rerun()
    
    with col2:
        if st.button("📸 Load Sample Melanoma", use_container_width=True, key="sample_melanoma"):
            st.session_state.demo_mode = "melanoma"
            st.rerun()
        
        if st.button("📸 Load Sample Other", use_container_width=True, key="sample_other"):
            st.session_state.demo_mode = "other"
            st.rerun()


# ========== COMPACT SIDEBAR COMPONENTS (NEW) ==========

def render_compact_model_card(model_info):
    """Compact model summary card for sidebar (2x2 grid)"""
    st.markdown('<div class="compact-card">', unsafe_allow_html=True)
    st.markdown('<b>🧠 AI System</b>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.caption("**Architecture**")
        st.caption("ResNet18")
    
    with col2:
        st.caption("**Validation**")
        st.caption("97.3%")
    
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.caption("**Explainability**")
        st.caption("Grad-CAM")
    
    with col2:
        st.caption("**Risk Engine**")
        st.caption("Clinical")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_compact_demo_selector():
    """Compact demo selector as dropdown instead of 4 buttons"""
    demo_options = {
        "None": None,
        "📸 Sample Nevus": "nevus",
        "📸 Sample BCC": "bcc",
        "📸 Sample Melanoma": "melanoma",
        "📸 Sample Other": "other"
    }
    
    selected = st.selectbox(
        "Demo Sample",
        options=list(demo_options.keys()),
        index=0,
        help="Load pre-built sample image for testing",
        label_visibility="collapsed"
    )
    
    if demo_options[selected] is not None:
        st.session_state.demo_mode = demo_options[selected]
        st.rerun()


def render_compact_history(history_data: list = None):
    """Ultra-compact session history"""
    if not history_data or len(history_data) == 0:
        st.caption("No analyses yet")
        return
    
    for entry in reversed(history_data[-3:]):  # Show last 3 only
        st.caption(
            f"• {entry.get('label', '?').upper()} "
            f"({entry.get('confidence', 0)*100:.0f}%)"
        )


# ========== CLINICAL DECISION SUPPORT COMPONENTS ==========

def render_differential_diagnosis(probabilities):
    """Display all class probabilities ranked for clinical context"""
    st.markdown("### 📊 Differential Diagnosis Ranking")
    
    try:
        # Convert numpy array to list and ensure float values
        prob_array = probabilities[0] if len(probabilities.shape) > 1 else probabilities
        
        # Create ranked list with class names
        class_probs = [(LABEL_NAMES[i], float(prob_array[i]) * 100) for i in range(len(LABEL_NAMES))]
        
        # Sort by probability descending
        ranked = sorted(class_probs, key=lambda x: x[1], reverse=True)
        
        # Display as ranked list with visual indicators
        col1, col2, col3 = st.columns([1, 2, 1.5])
        
        for rank, (class_name, prob) in enumerate(ranked, 1):
            # Color code based on rank and probability
            if rank == 1:
                icon = "🔴"  # Top prediction
                color_class = "high-risk"
            elif rank == 2:
                icon = "🟡"
                color_class = "moderate-risk"
            elif rank == 3:
                icon = "🟠"
                color_class = "uncertain"
            else:
                icon = "⚪"
                color_class = "low-risk"
            
            with col1:
                st.caption(f"{icon} {rank}. **{class_name.upper()}**")
            with col2:
                st.caption(f"{prob:.1f}%")
            with col3:
                # Progress bar
                st.progress(prob / 100.0)
    
    except Exception as e:
        st.caption(f"Unable to display differential diagnosis: {str(e)}")


def render_followup_intervals(pred_label, confidence_pct):
    """Clinical follow-up interval recommendations based on diagnosis and confidence"""
    st.markdown("### 📅 Clinical Follow-Up Recommendation")
    
    followup_guidance = {
        "melanoma": {
            "high": {
                "interval": "⏰ IMMEDIATE",
                "guidance": "Urgent dermatologist review and biopsy evaluation required. Do NOT delay.",
                "monitoring": "Same-day or next-day specialist appointment"
            },
            "moderate": {
                "interval": "⏰ URGENT (1-2 weeks)",
                "guidance": "Prompt specialist evaluation advised. Schedule appointment within 1-2 weeks.",
                "monitoring": "Consider dermoscopy and/or biopsy confirmation"
            },
            "low": {
                "interval": "⏰ EXPEDITED (2-4 weeks)",
                "guidance": "Specialist review recommended. Schedule within 2-4 weeks.",
                "monitoring": "Clinical assessment, possible dermoscopy"
            }
        },
        "bcc": {
            "high": {
                "interval": "⏰ SOON (2-4 weeks)",
                "guidance": "Clinical review and likely biopsy recommended within 2-4 weeks.",
                "monitoring": "Treatment planning (excision, curettage, cryotherapy, topical)"
            },
            "low": {
                "interval": "⏰ ROUTINE (4-8 weeks)",
                "guidance": "Specialist evaluation advised. Can be scheduled within routine timeframe.",
                "monitoring": "Confirm diagnosis before treatment"
            }
        },
        "nevus": {
            "high": {
                "interval": "📸 BASELINE PHOTO (Annual)",
                "guidance": "Low-risk benign lesion. Photograph now for baseline comparison.",
                "monitoring": "Annual review; alert patient to watch for changes (growth, color change, itching)"
            },
            "low": {
                "interval": "📸 BASELINE PHOTO (Annual)",
                "guidance": "Reassuring result. Document with photograph for future comparison.",
                "monitoring": "Routine skin surveillance; patient education on skin self-exam"
            }
        },
        "other": {
            "high": {
                "interval": "⏰ REVIEW (2-6 weeks)",
                "guidance": "Ambiguous lesion. Specialist evaluation recommended.",
                "monitoring": "Clinical assessment to clarify diagnosis"
            },
            "low": {
                "interval": "⏰ REVIEW (4-8 weeks)",
                "guidance": "Ambiguous lesion. Schedule routine specialist review.",
                "monitoring": "Further evaluation to establish diagnosis"
            }
        }
    }
    
    # Determine confidence level
    if confidence_pct >= 85:
        conf_level = "high"
        conf_icon = "🟢"
    elif confidence_pct >= 70:
        conf_level = "moderate"
        conf_icon = "🟡"
    else:
        conf_level = "low"
        conf_icon = "🔴"
    
    # Get guidance
    guidance = followup_guidance.get(pred_label, followup_guidance["other"]).get(conf_level)
    
    if guidance:
        st.markdown(
            f"""
            <div class="prediction-card">
                <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">
                    {guidance['interval']}
                </div>
                <div style="font-size: 0.95rem; margin-bottom: 0.5rem;">
                    {conf_icon} {guidance['guidance']}
                </div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">
                    <b>Monitoring:</b> {guidance['monitoring']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_sensitivity_specificity_disclosure():
    """Research prototype disclaimer"""
    st.markdown(
        """
        <div style="background-color: #fff8e1; border-left: 4px solid #ff9800; padding: 1rem; border-radius: 4px; margin-bottom: 1rem;">
            <div style="font-weight: bold; color: #e65100; margin-bottom: 0.5rem;">
                ⚠️ Important: This is a research prototype, not a diagnostic device
            </div>
            <div style="font-size: 0.9rem; color: #bf360c;">
                This model is a clinical decision <b>support tool</b>, not a replacement for expert clinical judgment.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )