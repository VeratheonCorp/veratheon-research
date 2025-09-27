"""
EPS Validation Research Module

This module contains specialized EPS validation methods that complement the existing
comprehensive research system. It provides bottom-up, peer-relative, and sentiment-based
validation approaches for consensus EPS estimates.
"""

from .eps_validation_models import BottomUpEpsValidation  # Enums; Models
from .eps_validation_models import (
    ConfidenceLevel,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    MarketSentimentEpsCheck,
    PeerRelativeEpsValidation,
    RevisionMomentum,
    SentimentAlignment,
)

__all__ = [
    # Enums
    "EpsValidationVerdict",
    "RevisionMomentum",
    "ConfidenceLevel",
    "SentimentAlignment",
    # Models
    "BottomUpEpsValidation",
    "PeerRelativeEpsValidation",
    "MarketSentimentEpsCheck",
    "EpsValidationSynthesis",
]
