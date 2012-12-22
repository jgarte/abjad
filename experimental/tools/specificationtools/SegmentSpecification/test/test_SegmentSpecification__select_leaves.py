from abjad import *
from experimental.tools import *


def test_SegmentSpecification__select_leaves_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    timespan = red_segment.select_leaves('Voice 1', start=2, stop=4)
    rhythm = timespan.select_leaves('Voice 1')
    red_segment.set_rhythm(rhythm, contexts=['Voice 2'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_02():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures('Voice 1', 0, 1)
    second_measure = red_segment.select_background_measures('Voice 1', 1, 2)
    first_measure.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.select_leaves('Voice 1')
    second_measure.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves('Voice 1', start=4, stop=7)
    voice_1_rhythm = timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_leaves_03():
    '''Leaves select correctly across offset-positioned rhythm expression boundaries.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    first_measure = red_segment.select_background_measures('Voice 1', 0, 1)
    second_measure = red_segment.select_background_measures('Voice 1', 1, 2)
    first_measure.set_rhythm("{ c'32 [ c'16 c'16. c'8 ] }", contexts=['Voice 1'])
    cell = first_measure.select_leaves('Voice 1')
    second_measure.set_rhythm(cell.rotate(Duration(-1, 32)), contexts=['Voice 1'])
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures(2 * [(2, 8)])
    timespan = red_segment.select_leaves('Voice 1', start=4, stop=8)
    voice_1_rhythm = timespan.select_leaves('Voice 1')
    blue_segment.set_rhythm(voice_1_rhythm, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
