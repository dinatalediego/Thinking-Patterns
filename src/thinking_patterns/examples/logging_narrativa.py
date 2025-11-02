from thinking_patterns.core.patterns_catalog import LoggingComoNarrativa

if __name__ == "__main__":
    patron = LoggingComoNarrativa()
    print(patron.aplicar({
        "paso": "feature_engineering",
        "decision": "descartar outliers 99p",
        "evidencia": "AUC sube +0.03"
    }))
