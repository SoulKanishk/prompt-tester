def exact_match(output, expected):
    return 1.0 if expected.lower() in output.lower() else 0.0

def partial_match(output, expected):
    output_words = output.lower().split()
    return 1.0 if expected.lower() in output_words else 0.0