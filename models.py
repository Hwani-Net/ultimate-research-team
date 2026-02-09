"""
Pydantic Models for Structured Outputs (Antigravity v11.5)
"""
from pydantic import BaseModel, Field
from typing import Optional

class KillSwitchResult(BaseModel):
    """
    Kill Switch Decision Output (Machine-Readable)
    """
    decision: str = Field(description="PASS or KILL")
    gate_failed: Optional[int] = Field(default=None, description="Gate number (1-4) that failed, or None if PASS")
    gate_name: Optional[str] = Field(default=None, description="Name of the failed gate")
    reason: str = Field(description="Detailed reason for decision")
    evidence: Optional[str] = Field(default=None, description="Concrete evidence (e.g., trademark registration number, law citation)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "decision": "KILL",
                "gate_failed": 2,
                "gate_name": "Identical Trademark",
                "reason": "Project name 'Notion' is an exact match to registered trademark",
                "evidence": "USPTO Registration #87654321, active since 2016"
            }
        }

class BoardDecision(BaseModel):
    """
    Board of Directors Decision Output
    """
    decision: str = Field(description="APPROVED, REJECTED, or CONDITIONAL")
    conditions: Optional[list[str]] = Field(default=None, description="Conditions if conditional approval")
    concerns: list[str] = Field(description="Key concerns raised by board members")
    recommendations: list[str] = Field(description="Strategic recommendations")
    vote_breakdown: dict[str, str] = Field(description="Individual votes (e.g., {'CEO': 'APPROVED', 'CFO': 'CONDITIONAL'})")
    
    class Config:
        json_schema_extra = {
            "example": {
                "decision": "CONDITIONAL",
                "conditions": ["Rebrand to avoid trademark conflict", "Secure $100K seed funding"],
                "concerns": ["Market saturation", "High customer acquisition cost"],
                "recommendations": ["Focus on niche vertical", "Implement freemium model"],
                "vote_breakdown": {
                    "CEO": "APPROVED",
                    "CFO": "CONDITIONAL",
                    "CTO": "APPROVED",
                    "CMO": "CONDITIONAL",
                    "CLO": "REJECTED"
                }
            }
        }
