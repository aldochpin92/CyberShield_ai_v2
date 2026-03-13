# tools/human_factor_protection.py

def calculate_risk_score(platform: str, behavior_flags: list):
    """
    Latin Passion, Cyber Strength. 
    This tool calculates if a social interaction is high-risk.
    """
    score = 0
    
    # Platform Risk
    high_risk_apps = ["Grindr", "Sniffies", "Telegram"]
    if platform in high_risk_apps:
        score += 3
        
    # Logic for Red Flags
    for flag in behavior_flags:
        f = flag.lower()
        if "money" in f or "gift card" in f:
            score += 5
        if "meet now" in f or "private" in f:
            score += 2
            
    return min(score, 10)
