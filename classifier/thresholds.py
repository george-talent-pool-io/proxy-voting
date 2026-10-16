from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Thresholds:
    high: float=.98
    review: float=.70
    automation_enabled: bool=False
    def __post_init__(self):
        if not (math.isfinite(self.high) and math.isfinite(self.review) and 0<=self.review<=self.high<=1):
            raise ValueError('Require 0 <= review <= high <= 1')
    def action(self, confidence, blocked=False):
        if confidence is None or not math.isfinite(confidence) or not 0<=confidence<=1 or blocked:
            return 'MANUAL_REVIEW'
        if self.automation_enabled and confidence>=self.high: return 'AUTO_CLASSIFY'
        return 'CLASSIFY_AND_REVIEW' if confidence>=self.review else 'MANUAL_REVIEW'
