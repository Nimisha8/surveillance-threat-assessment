class ThreatEngine:
    """
    Combines suspicious-behavior signals into a weighted threat score,
    then classifies it. Weights/thresholds are configurable.
    """
    WEIGHTS = {
        "unknown": 40,
        "loitering": 25,
        "unattended": 30,
        "multiple_unknown": 20,
    }

    def score(self, is_unknown=False, is_loitering=False,
              unattended_count=0, unknown_count=0):
        pts = 0
        if is_unknown:
            pts += self.WEIGHTS["unknown"]
        if is_loitering:
            pts += self.WEIGHTS["loitering"]
        if unattended_count > 0:
            pts += self.WEIGHTS["unattended"]
        if unknown_count >= 2:
            pts += self.WEIGHTS["multiple_unknown"]
        return min(pts, 100)

    def classify(self, score):
        if score >= 90:
            return "CRITICAL", (0, 0, 255)
        elif score >= 60:
            return "HIGH", (0, 80, 255)
        elif score >= 30:
            return "MEDIUM", (0, 200, 255)
        else:
            return "LOW", (0, 200, 0)