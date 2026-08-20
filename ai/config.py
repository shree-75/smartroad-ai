"""
SmartRoad AI - Research System Configuration Parameters
Main Research Identity: Personalized + Weighted Multimodal Driver Risk Assessment
"""

# 1. Personalization Calibration Parameters
CALIBRATION_DURATION_SEC = 30  # Duration (seconds) of initial baseline calibration phase
EAR_SIGMA_FACTOR = 2.0         # k factor for dynamic EAR threshold (μ - k * σ)
MAR_SIGMA_FACTOR = 2.0         # k factor for dynamic MAR threshold (μ + k * σ)
YAW_DEVIATION_FACTOR = 1.8     # k factor for head yaw deviation threshold
ADAPTATION_RATE = 0.02         # Exponential moving average rate for baseline adaptation in NORMAL state

# 2. Multimodal Fusion Initial Research Weights (Must sum to 1.0)
VISION_WEIGHT = 0.50
BIOMETRIC_WEIGHT = 0.30
VEHICLE_WEIGHT = 0.20

# 3. Context & Road Risk Parameters (Tier 4 Architecture Interface)
ROAD_CONTEXT_WEIGHT = 0.0      # Active in Tier 4 context-aware risk integration
HOTSPOT_RISK_MULTIPLIER = 1.25 # Multiplier when vehicle enters a spatial accident hotspot zone

# 4. Research Hypothesis Statement
RESEARCH_HYPOTHESIS = (
    "A driver-specific adaptive baseline threshold combined with weighted multimodal sensor fusion "
    "can reduce false alerts and produce a more reliable driver-risk assessment than fixed-threshold camera-only monitoring."
)
