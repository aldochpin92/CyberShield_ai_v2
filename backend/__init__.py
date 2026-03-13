# backend/__init__.py
# Exposing the Core Identity and Logic of CyberShield AI (El Guardián)

from .identity import CYBERSHIELD_PROMPT

# This allows other modules to import the prompt directly
__all__ = ["CYBERSHIELD_PROMPT"]