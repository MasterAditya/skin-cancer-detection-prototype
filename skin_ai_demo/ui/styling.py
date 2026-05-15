# ui/styling.py

def apply_custom_css():
    return """
    <style>
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: #f5f7fa;
        }

        .stApp {
            background: #f5f7fa;
            color: #2c3e50;
        }

        /* ============================================ 
           MAIN CONTAINERS & LAYOUT
           ============================================ */
        .main-header {
            background: #ffffff;
            padding: 2rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid #e0e7f1;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #2196F3, transparent);
        }

        /* ============================================ 
           TYPOGRAPHY & HEADERS
           ============================================ */
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #1976D2;
            margin-bottom: 0.5rem;
            letter-spacing: -0.3px;
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #5a6c7d;
            font-weight: 500;
            margin-bottom: 1.5rem;
            letter-spacing: 0.3px;
        }

        .section-header {
            font-size: 1.5rem;
            font-weight: 800;
            color: #64b5f6;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-header::after {
            content: '';
            flex-grow: 1;
            height: 2px;
            background: linear-gradient(90deg, #42a5f5 0%, transparent);
            border-radius: 2px;
        }

        /* ============================================ 
           BADGES & INDICATORS
           ============================================ */
        .header-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, rgba(66, 165, 245, 0.15) 0%, rgba(30, 136, 229, 0.1) 100%);
            border: 1px solid rgba(100, 181, 246, 0.4);
            color: #64b5f6;
            padding: 0.65rem 1.25rem;
            border-radius: 24px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            backdrop-filter: blur(8px);
            box-shadow: 0 8px 24px rgba(66, 165, 245, 0.1);
            margin-top: 1rem;
        }

        .badge-certified {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(56, 142, 60, 0.1) 100%);
            border-color: rgba(129, 199, 132, 0.4);
            color: #81c784;
        }

        .badge-research {
            background: linear-gradient(135deg, rgba(103, 58, 183, 0.15) 0%, rgba(63, 81, 181, 0.1) 100%);
            border-color: rgba(159, 168, 218, 0.4);
            color: #9fa8da;
        }

        /* ============================================ 
           DISCLAIMER & ALERTS
           ============================================ */
        .disclaimer-banner {
            background: #fff3e0;
            border-left: 4px solid #ff6f00;
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2.5rem;
            color: #e65100;
            font-size: 0.95rem;
            border: 1px solid #ffe0b2;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            line-height: 1.6;
        }

        .disclaimer-banner b {
            color: #ff6f00;
        }

        /* ============================================ 
           METRIC CARDS - PREMIUM
           ============================================ */
        .metric-card {
            background: #f5f8fb;
            border: 1px solid #e0e7f1;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            display: none;
        }

        .metric-card:hover {
            border-color: #90caf9;
            background: #ffffff;
            box-shadow: 0 2px 6px rgba(33, 150, 243, 0.12);
        }

        .metric-card:hover::before {
            display: none;
        }

        .metric-label {
            font-size: 0.8rem;
            font-weight: 700;
            color: #90caf9;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 0.75rem;
            opacity: 0.9;
        }

        .metric-value {
            font-size: 2.2rem;
            font-weight: 900;
            color: #64b5f6;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }

        .metric-detail {
            font-size: 0.8rem;
            color: #90caf9;
            opacity: 0.75;
            font-weight: 500;
        }

        /* ============================================ 
           PREDICTION CARDS - RISK BASED
           ============================================ */
        .prediction-card {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(56, 142, 60, 0.05) 100%);
            border: 1.5px solid rgba(129, 199, 132, 0.3);
            border-radius: 16px;
            padding: 1.75rem;
            margin-bottom: 1.5rem;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(129, 199, 132, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .prediction-card.high-risk {
            background: linear-gradient(135deg, rgba(229, 57, 53, 0.12) 0%, rgba(183, 28, 28, 0.06) 100%);
            border-color: rgba(244, 67, 54, 0.4);
            box-shadow: 
                0 20px 60px rgba(229, 57, 53, 0.15),
                inset 0 1px 0 rgba(244, 67, 54, 0.1);
        }

        .prediction-card.moderate-risk {
            background: linear-gradient(135deg, rgba(251, 140, 0, 0.12) 0%, rgba(230, 124, 15, 0.06) 100%);
            border-color: rgba(255, 152, 0, 0.4);
            box-shadow: 
                0 20px 60px rgba(251, 140, 0, 0.15),
                inset 0 1px 0 rgba(255, 152, 0, 0.1);
        }

        .prediction-card.low-risk {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(56, 142, 60, 0.06) 100%);
            border-color: rgba(129, 199, 132, 0.4);
        }

        .prediction-card.uncertain {
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.12) 0%, rgba(251, 140, 0, 0.06) 100%);
            border-color: rgba(255, 193, 7, 0.4);
            box-shadow: 
                0 20px 60px rgba(255, 193, 7, 0.1),
                inset 0 1px 0 rgba(255, 193, 7, 0.1);
        }

        .prediction-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: #e3f2fd;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .prediction-text {
            font-size: 0.95rem;
            color: #cfd8dc;
            line-height: 1.7;
            font-weight: 500;
        }

        /* ============================================ 
           RISK INDICATORS & COLORS
           ============================================ */
        .risk-high {
            color: #ff5252;
            font-weight: 900;
            text-shadow: 0 0 10px rgba(255, 82, 82, 0.3);
        }

        .risk-moderate {
            color: #ffb74d;
            font-weight: 900;
            text-shadow: 0 0 10px rgba(255, 183, 77, 0.3);
        }

        .risk-low {
            color: #81c784;
            font-weight: 900;
            text-shadow: 0 0 10px rgba(129, 199, 132, 0.3);
        }

        .risk-uncertain {
            color: #ffd54f;
            font-weight: 900;
            text-shadow: 0 0 10px rgba(255, 213, 79, 0.3);
        }

        /* ============================================ 
           PROBABILITY BARS & VISUALIZATION
           ============================================ */
        .probability-bar {
            height: 10px;
            background: #e0e7f1;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 0.75rem;
            border: 1px solid #c5d3e0;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.04);
        }

        .probability-fill {
            height: 100%;
            background: linear-gradient(90deg, #2196F3 0%, #1976D2 50%, #0d47a1 100%);
            transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            border-radius: 8px;
            box-shadow: 0 0 8px rgba(33, 150, 243, 0.3);
        }

        /* ============================================ 
           TABS - ADVANCED
           ============================================ */
        .stTabs [role="tablist"] {
            border-bottom: 2px solid #e0e7f1;
            gap: 1.5rem;
            padding-bottom: 1rem;
        }

        .stTabs [role="tab"] {
            background: transparent;
            border: none;
            color: #5a6c7d;
            font-weight: 700;
            padding: 0.85rem 1.75rem;
            border-bottom: 3px solid transparent;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.95rem;
            position: relative;
        }

        .stTabs [role="tab"]::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #2196F3, #1976D2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
            border-radius: 2px;
        }

        .stTabs [role="tab"]:hover {
            color: #1976D2;
            transform: translateY(-2px);
        }

        .stTabs [role="tab"][aria-selected="true"] {
            color: #1976D2;
            border-bottom-color: #1976D2;
        }

        /* ============================================ 
           SIDEBAR - PROFESSIONAL
           ============================================ */
        [data-testid="stSidebar"] {
            background: #f5f7fa;
            border-right: 1px solid #e0e7f1;
        }

        .sidebar-title {
            font-size: 0.95rem;
            font-weight: 900;
            color: #1976D2;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1.25rem;
            padding: 0.75rem 0;
            border-bottom: 2px solid #e0e7f1;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .sidebar-section {
            margin-bottom: 2rem;
            padding: 0.75rem 0;
            border-radius: 12px;
        }

        .sidebar-label {
            font-size: 0.8rem;
            font-weight: 700;
            color: #90caf9;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 0.75rem;
            display: block;
            opacity: 0.9;
        }

        .sidebar-value {
            font-size: 0.9rem;
            color: #cfd8dc;
            line-height: 1.7;
            font-weight: 500;
        }

        /* ============================================ 
           COMPACT SIDEBAR CARDS
           ============================================ */
        .compact-card {
            background: #ffffff;
            border: 1px solid #e0e7f1;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .compact-card b {
            font-size: 0.85rem;
            color: #1976D2;
        }

        .compact-card .stCaption {
            font-size: 0.7rem !important;
            margin: 0.25rem 0 !important;
        }

        /* ============================================ 
           BUTTONS - PREMIUM
           ============================================ */
        .stButton > button {
            background: rgba(80, 120, 160, 0.7);
            color: white;
            border: 1px solid rgba(120, 160, 200, 0.4);
            font-weight: 600;
            padding: 0.7rem 1.5rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            font-size: 0.85rem;
        }

        .stButton > button:hover {
            background: rgba(100, 140, 180, 0.8);
            border-color: rgba(120, 160, 200, 0.6);
        }

        .stButton > button::before {
            display: none;
        }

        .stButton > button:active {
            transform: none;
        }

        /* ============================================ 
           IMAGE CONTAINERS
           ============================================ */
        .image-container {
            background: #f5f8fb;
            border: 1.5px solid #e0e7f1;
            border-radius: 12px;
            padding: 1.25rem;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        .image-label {
            font-size: 0.9rem;
            font-weight: 800;
            color: #1976D2;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ============================================ 
           TECHNICAL PANELS
           ============================================ */
        .tech-panel {
            background: #f5f8fb;
            border: 1.5px solid #e0e7f1;
            border-radius: 12px;
            padding: 1.75rem;
            margin-top: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        .tech-title {
            font-size: 0.95rem;
            font-weight: 800;
            color: #1976D2;
            margin-bottom: 1.25rem;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tech-detail {
            font-size: 0.9rem;
            color: #5a6c7d;
            margin-bottom: 1rem;
            line-height: 1.7;
            font-weight: 500;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e0e7f1;
        }

        .tech-detail:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .tech-detail b {
            color: #ce93d8;
        }

        /* ============================================ 
           FOOTER - PROFESSIONAL
           ============================================ */
        .footer-note {
            text-align: center;
            color: #5a6c7d;
            margin-top: 4rem;
            padding-top: 2.5rem;
            border-top: 1px solid #e0e7f1;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        .footer-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: #e3f2fd;
            border: 1px solid #90caf9;
            color: #1976D2;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin-top: 1.25rem;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        /* ============================================ 
           ANIMATIONS & TRANSITIONS
           ============================================ */
        @keyframes fadeInSlideUp {
            from {
                opacity: 0;
                transform: translateY(25px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 10px rgba(66, 165, 245, 0.3);
            }
            50% {
                box-shadow: 0 0 20px rgba(66, 165, 245, 0.6);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .fade-in {
            animation: fadeInSlideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }

        .glow-effect {
            animation: glow 3s ease-in-out infinite;
        }

        /* ============================================ 
           SCROLLBAR - CUSTOM
           ============================================ */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(100, 181, 246, 0.05);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #42a5f5 0%, #64b5f6 100%);
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(66, 165, 245, 0.3);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #64b5f6 0%, #81c784 100%);
        }

        /* ============================================ 
           RESPONSIVE DESIGN
           ============================================ */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2rem;
            }

            .metric-card {
                padding: 1.25rem;
            }

            .metric-value {
                font-size: 1.6rem;
            }

            .section-header {
                font-size: 1.2rem;
            }

            .main-header {
                padding: 2rem 1.5rem;
            }
        }

        /* ============================================ 
           UTILITY CLASSES
           ============================================ */
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #e0e7f1, transparent);
            margin: 2rem 0;
            border-radius: 1px;
        }

        .glass-effect {
            background: #f5f8fb;
            border-radius: 12px;
            border: 1px solid rgba(100, 181, 246, 0.1);
        }
    </style>
    """