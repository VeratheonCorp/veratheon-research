"""
EPS Validation Research Module

This module contains specialized EPS validation methods that complement the existing
comprehensive research system. It provides bottom-up, peer-relative, and sentiment-based
validation approaches for consensus EPS estimates.
"""

from .eps_validation_models import (
    # Enums
    EpsValidationVerdict,
    RevisionMomentum,
    ConfidenceLevel,
    SentimentAlignment,

    # Models
    BottomUpEpsValidation,
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
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