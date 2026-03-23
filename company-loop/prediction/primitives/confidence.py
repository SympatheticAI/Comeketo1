"""
Confidence Primitive — Explicit Uncertainty Quantification

This is the foundation of trustworthy prediction.

Every prediction, recommendation, or decision made by the system includes
an explicit confidence score. This enables:
- Appropriate human oversight
- Graceful degradation
- Shadow mode validation
- Promotion criteria evaluation

Confidence is NOT just a number. It's a structured assessment that includes:
- Numerical score (0.0 - 1.0)
- Contributing factors
- Data quality indicators
- Historical accuracy
- Abstention conditions
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    """Categorical confidence levels for human-readable interpretation."""
    VERY_LOW = "very_low"      # 0.0 - 0.3: High uncertainty, always flag for review
    LOW = "low"                 # 0.3 - 0.5: Significant uncertainty, suggest review
    MEDIUM = "medium"           # 0.5 - 0.7: Moderate confidence, approval recommended
    HIGH = "high"               # 0.7 - 0.9: High confidence, may automate if validated
    VERY_HIGH = "very_high"     # 0.9 - 1.0: Very high confidence, safe for automation


@dataclass
class ConfidenceScore:
    """
    Structured confidence assessment.

    This is NOT just a float. It's a rich object that explains
    the confidence level and enables appropriate action.
    """

    # Core score
    score: float  # 0.0 - 1.0

    # Categorical level
    level: ConfidenceLevel

    # Contributing factors (weights should sum to 1.0)
    factors: Dict[str, float]

    # Data quality indicators
    data_quality: Dict[str, Any]

    # Historical accuracy (if available)
    historical_accuracy: Optional[float] = None

    # Abstention flag
    should_abstain: bool = False
    abstention_reason: Optional[str] = None

    # Explanation
    explanation: str = ""

    def __post_init__(self):
        """Validate score and derive level if not provided."""
        # Validate score range
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Confidence score must be between 0.0 and 1.0, got {self.score}")

        # Derive level from score if not explicitly set
        if self.level is None:
            self.level = self._score_to_level(self.score)

        # Check abstention conditions
        if self.score < 0.3:
            self.should_abstain = True
            if not self.abstention_reason:
                self.abstention_reason = "Confidence below minimum threshold (0.3)"

    @staticmethod
    def _score_to_level(score: float) -> ConfidenceLevel:
        """Convert numerical score to categorical level."""
        if score < 0.3:
            return ConfidenceLevel.VERY_LOW
        elif score < 0.5:
            return ConfidenceLevel.LOW
        elif score < 0.7:
            return ConfidenceLevel.MEDIUM
        elif score < 0.9:
            return ConfidenceLevel.HIGH
        else:
            return ConfidenceLevel.VERY_HIGH

    def requires_approval(self) -> bool:
        """
        Determine if action should require approval based on confidence.

        Rules:
        - VERY_LOW, LOW: Always require approval
        - MEDIUM: Require approval unless explicitly promoted
        - HIGH, VERY_HIGH: May be automated if validated in shadow mode
        """
        return self.level in [ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "score": self.score,
            "level": self.level.value,
            "factors": self.factors,
            "data_quality": self.data_quality,
            "historical_accuracy": self.historical_accuracy,
            "should_abstain": self.should_abstain,
            "abstention_reason": self.abstention_reason,
            "explanation": self.explanation
        }


def calculate_confidence(
    base_factors: Dict[str, float],
    data_quality_indicators: Dict[str, Any],
    historical_accuracy: Optional[float] = None,
    abstention_conditions: Optional[List[str]] = None
) -> ConfidenceScore:
    """
    Calculate confidence score from multiple factors.

    This is the primary interface for building confidence scores.

    Args:
        base_factors: Dict of factor name -> weight (should sum to 1.0)
                     Example: {
                         "data_completeness": 0.4,
                         "historical_accuracy": 0.3,
                         "recency": 0.2,
                         "sample_size": 0.1
                     }

        data_quality_indicators: Information about data quality
                                Example: {
                                    "missing_fields": 0,
                                    "stale_data_count": 2,
                                    "source_reliability": 0.9
                                }

        historical_accuracy: Optional accuracy from past predictions (0.0 - 1.0)

        abstention_conditions: Optional list of reasons to abstain
                              Example: ["insufficient_data", "conflicting_sources"]

    Returns:
        ConfidenceScore object
    """
    # Validate factors sum to 1.0
    factor_sum = sum(base_factors.values())
    if not 0.99 <= factor_sum <= 1.01:  # Allow small floating point error
        raise ValueError(f"Base factors must sum to 1.0, got {factor_sum}")

    # Calculate weighted score
    score = sum(base_factors.values())

    # Apply historical accuracy adjustment if available
    if historical_accuracy is not None:
        # Blend historical accuracy with current factors (70% current, 30% historical)
        score = 0.7 * score + 0.3 * historical_accuracy

    # Check abstention conditions
    should_abstain = False
    abstention_reason = None

    if abstention_conditions:
        should_abstain = True
        abstention_reason = "; ".join(abstention_conditions)

    # Generate explanation
    explanation = _generate_explanation(base_factors, data_quality_indicators, score)

    return ConfidenceScore(
        score=score,
        level=ConfidenceScore._score_to_level(score),
        factors=base_factors,
        data_quality=data_quality_indicators,
        historical_accuracy=historical_accuracy,
        should_abstain=should_abstain,
        abstention_reason=abstention_reason,
        explanation=explanation
    )


def _generate_explanation(
    factors: Dict[str, float],
    data_quality: Dict[str, Any],
    score: float
) -> str:
    """
    Generate human-readable explanation of confidence score.

    Args:
        factors: Contributing factors
        data_quality: Data quality indicators
        score: Final confidence score

    Returns:
        Explanation string
    """
    # Find top 2 contributing factors
    sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
    top_factors = sorted_factors[:2]

    level_name = ConfidenceScore._score_to_level(score).value.replace("_", " ")

    explanation = f"Confidence is {level_name} ({score:.2f}). "
    explanation += f"Primary factors: {top_factors[0][0]} ({top_factors[0][1]:.2f}), "
    explanation += f"{top_factors[1][0]} ({top_factors[1][1]:.2f}). "

    # Add data quality notes
    if "missing_fields" in data_quality and data_quality["missing_fields"] > 0:
        explanation += f"{data_quality['missing_fields']} fields missing. "

    if "stale_data_count" in data_quality and data_quality["stale_data_count"] > 0:
        explanation += f"{data_quality['stale_data_count']} stale data sources. "

    return explanation


# Example usage
if __name__ == "__main__":
    # Example: Lead quality prediction confidence

    # Scenario 1: High confidence prediction
    high_conf = calculate_confidence(
        base_factors={
            "source_quality": 0.9,     # Known good source (venue referral)
            "data_completeness": 0.95,  # All fields populated
            "engagement_level": 0.85,   # Quick response to initial outreach
            "event_timing": 0.8         # Event in ideal booking window
        },
        data_quality_indicators={
            "missing_fields": 0,
            "stale_data_count": 0,
            "source_reliability": 0.95
        },
        historical_accuracy=0.88  # Historical predictions 88% accurate
    )

    print("High Confidence Example:")
    print(f"  Score: {high_conf.score:.2f}")
    print(f"  Level: {high_conf.level.value}")
    print(f"  Requires Approval: {high_conf.requires_approval()}")
    print(f"  Explanation: {high_conf.explanation}")
    print()

    # Scenario 2: Low confidence prediction (should abstain)
    low_conf = calculate_confidence(
        base_factors={
            "source_quality": 0.3,      # Unknown source
            "data_completeness": 0.4,   # Missing key fields
            "engagement_level": 0.2,    # No response yet
            "event_timing": 0.5         # Far future or unclear
        },
        data_quality_indicators={
            "missing_fields": 3,
            "stale_data_count": 1,
            "source_reliability": 0.5
        },
        abstention_conditions=["insufficient_data", "unverified_source"]
    )

    print("Low Confidence Example (Abstention):")
    print(f"  Score: {low_conf.score:.2f}")
    print(f"  Level: {low_conf.level.value}")
    print(f"  Should Abstain: {low_conf.should_abstain}")
    print(f"  Abstention Reason: {low_conf.abstention_reason}")
    print(f"  Requires Approval: {low_conf.requires_approval()}")
    print(f"  Explanation: {low_conf.explanation}")
