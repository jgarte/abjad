import collections


def analyze(argument):
    """
    Makes tonal analysis agent.

    Returns tonal analysis agent.
    """
    import abjad
    leaves = abjad.select(argument).leaves()
    return abjad.tonalanalysis.TonalAnalysis(leaves)
