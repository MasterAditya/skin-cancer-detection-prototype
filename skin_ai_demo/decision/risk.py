# decision/risk.py

def assess_risk(pred_label, confidence):
    """
    Rule-based clinical triage logic
    """

    confidence_pct = confidence * 100

    # ---------------- MELANOMA ----------------
    if pred_label == "melanoma":

        if confidence_pct >= 85:
            return {
                "risk": "HIGH RISK",
                "recommendation": (
                    "Urgent dermatologist review recommended."
                )
            }

        elif confidence_pct >= 70:
            return {
                "risk": "MODERATE-HIGH RISK",
                "recommendation": (
                    "Further specialist evaluation advised."
                )
            }

        else:
            return {
                "risk": "UNCERTAIN",
                "recommendation": (
                    "Low-confidence melanoma suspicion. "
                    "Refer specialist for further assessment."
                )
            }

    # ---------------- BCC ----------------
    elif pred_label == "bcc":

        if confidence_pct >= 85:
            return {
                "risk": "MODERATE-HIGH RISK",
                "recommendation": (
                    "Clinical review strongly advised."
                )
            }

        else:
            return {
                "risk": "UNCERTAIN",
                "recommendation": (
                    "Basal cell carcinoma suspicion requires confirmation."
                )
            }

    # ---------------- NEVUS ----------------
    elif pred_label == "nevus":

        if confidence_pct >= 90:
            return {
                "risk": "LOW RISK",
                "recommendation": (
                    "Benign-appearing lesion prediction, "
                    "but clinical review is still advised."
                )
            }

        else:
            return {
                "risk": "UNCERTAIN",
                "recommendation": (
                    "Low-confidence benign prediction. "
                    "Specialist review recommended."
                )
            }

    # ---------------- OTHER ----------------
    else:
        return {
            "risk": "UNCERTAIN",
            "recommendation": (
                "Ambiguous lesion category detected. "
                "Specialist evaluation recommended."
            )
        }