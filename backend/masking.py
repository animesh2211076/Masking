from typing import Dict, Any
from presidio_anonymizer.entities import OperatorConfig

from config import SUPPORTED_ENTITIES, FIELDS_TO_MASK
from presidio_config import setup_presidio

analyzer, anonymizer = setup_presidio()


def presidio_mask_text(text: str, role: str) -> str:
  
    if role == "admin":
        return text  # Admin sees full

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=SUPPORTED_ENTITIES,
    )

    # Strict masking for normal user
    if role == "user":
        operators = {
            "DEFAULT": OperatorConfig("replace", {"new_value": "<MASKED>"}),
            "EMAIL_ADDRESS": OperatorConfig("mask", {"chars_to_mask": 6, "masking_char": "*", "from_end": False}),
            "PHONE_NUMBER": OperatorConfig("mask", {"chars_to_mask": 6, "masking_char": "*", "from_end": True}),
            "PAN": OperatorConfig("replace", {"new_value": "PAN_MASKED"}),
            "IFSC": OperatorConfig("replace", {"new_value": "IFSC_MASKED"}),
            "ACCOUNT_NUMBER": OperatorConfig("mask", {"chars_to_mask": 8, "masking_char": "*", "from_end": True}),
            "UPI_ID": OperatorConfig("replace", {"new_value": "UPI_MASKED"}),
        }

    # Partial masking for support
    elif role == "support":
        operators = {
            "DEFAULT": OperatorConfig("replace", {"new_value": "<MASKED>"}),
            "EMAIL_ADDRESS": OperatorConfig("mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": False}),
            "PHONE_NUMBER": OperatorConfig("mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": True}),
            "PAN": OperatorConfig("mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": False}),
            "IFSC": OperatorConfig("mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": False}),
            "ACCOUNT_NUMBER": OperatorConfig("mask", {"chars_to_mask": 6, "masking_char": "*", "from_end": True}),
            "UPI_ID": OperatorConfig("mask", {"chars_to_mask": 4, "masking_char": "*", "from_end": False}),
        }

    else:
        operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "<MASKED>"})}

    anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
    return anonymized.text


def mask_user_object(user_obj: Dict[str, Any], role: str) -> Dict[str, Any]:
 
    masked = user_obj.copy()

    for field in FIELDS_TO_MASK:
        if field in masked and masked[field] is not None:
            masked[field] = presidio_mask_text(str(masked[field]), role)

    return masked
