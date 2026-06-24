from presidio_analyzer import (
    AnalyzerEngine
)

from presidio_anonymizer import (
    AnonymizerEngine
)


analyzer = AnalyzerEngine()

anonymizer = (
    AnonymizerEngine()
)


def mask_output(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    if not results:

        return text

    anonymized = (
        anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
    )

    return anonymized.text