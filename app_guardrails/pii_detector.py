from presidio_analyzer import (
    AnalyzerEngine
)


analyzer = AnalyzerEngine()


def detect_pii(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    findings = []

    for result in results:

        findings.append(
            {
                "entity_type":
                result.entity_type,

                "score":
                round(
                    result.score,
                    2
                ),

                "start":
                result.start,

                "end":
                result.end
            }
        )

    return findings