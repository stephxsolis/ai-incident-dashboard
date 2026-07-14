

def analyze_ticket(title, details):
    #temp response

    if "vpn" in details.lower():
        category = "Network"
        ai_summary = "VPN connectivity issue detected"
        recommended_steps =["Clear saved VPN credentials", 
        "restart VPN client",
        "Verify VPN account perissions"]
        confidence = 0.85

    elif "password" in details.lower():
        category = "Account Access"
        ai_summary = "Possible password or authentication issue."
        recommended_steps = [
            "Verify password reset was completed",
            "Check account lock status",
            "Attempt login again"
        ]
        confidence = 0.90

    else:
        category = "General IT"
        ai_summary = "General technical issue requiring investigation."
        recommended_steps = [
            "Gather additional details",
            "Reproduce the issue",
            "Check system logs"
        ]
        confidence = 0.60

    return {
        "category": category,
        "ai_summary": ai_summary,
        "recommended_steps": recommended_steps,
        "ai_confidence": confidence
    }
    