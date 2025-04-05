from dataclasses import dataclass

@dataclass
class PersonalityParameters:
    """Parameters for the TARS robot's personality; similar to the movie"""
    assertiveness: float = 0.6
    confidence: float = 0.7
    creativity: float = 0.5
    curiosity: float = 0.5
    empathy: float = 0.5
    enthusiasm: float = 0.3
    honesty: float = 0.9
    humor: float = 0.7
    sarcasm: float = 0.6
    skepticism: float = 0.5
    
    def __str__(self):
        """Returns a string representation of the personality parameters."""
        return f"""
        Assertiveness: {self.assertiveness}
        Confidence: {self.confidence}
        Creativity: {self.creativity}
        Curiosity: {self.curiosity}
        Empathy: {self.empathy}
        Enthusiasm: {self.enthusiasm}
        Honesty: {self.honesty}
        Humor: {self.humor}
        Sarcasm: {self.sarcasm}
        Skepticism: {self.skepticism}"""