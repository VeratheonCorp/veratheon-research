"""
EPS Validation Research Module

This module contains specialized EPS validation methods that complement the existing
comprehensive research system. It provides peer-relative, sentiment-based, and technical
validation approaches for consensus EPS estimates.
"""

from .eps_validation_models import (
    ConfidenceLevel,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    MarketSentimentEpsCheck,
    PeerRelativeEpsValidation,
    RevisionMomentum,
    SentimentAlignment,
    TechnicalEpsValidation,
)

__all__ = [
    # Enums
    "EpsValidationVerdict",
    "RevisionMomentum",
    "ConfidenceLevel",
    "SentimentAlignment",
    # Models
    "PeerRelativeEpsValidation",
    "MarketSentimentEpsCheck",
    "TechnicalEpsValidation",
    "EpsValidationSynthesis",
]
