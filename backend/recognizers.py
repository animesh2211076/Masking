from presidio_analyzer import PatternRecognizer, Pattern


def get_custom_recognizers():

    pan_pattern = Pattern(
        name="PAN",
        regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        score=0.85,
    )
    pan_recognizer = PatternRecognizer(supported_entity="PAN", patterns=[pan_pattern])

    ifsc_pattern = Pattern(
        name="IFSC",
        regex=r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        score=0.85,
    )
    ifsc_recognizer = PatternRecognizer(supported_entity="IFSC", patterns=[ifsc_pattern])

    account_pattern = Pattern(
        name="ACCOUNT_NUMBER",
        regex=r"\b\d{9,18}\b",
        score=0.60,
    )
    account_recognizer = PatternRecognizer(supported_entity="ACCOUNT_NUMBER", patterns=[account_pattern])

    upi_pattern = Pattern(
        name="UPI_ID",
        regex=r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b",
        score=0.80,
    )
    upi_recognizer = PatternRecognizer(supported_entity="UPI_ID", patterns=[upi_pattern])

    return [pan_recognizer, ifsc_recognizer, account_recognizer, upi_recognizer]
