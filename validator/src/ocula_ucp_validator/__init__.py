"""Structural conformance validator for tech.ocula.shopping.descriptors."""

from ocula_ucp_validator.report import ValidationResult
from ocula_ucp_validator.schema import build_registry, load_capability_schema
from ocula_ucp_validator.validate import validate_manifest, validate_response

__all__ = [
    "ValidationResult",
    "build_registry",
    "load_capability_schema",
    "validate_manifest",
    "validate_response",
]
