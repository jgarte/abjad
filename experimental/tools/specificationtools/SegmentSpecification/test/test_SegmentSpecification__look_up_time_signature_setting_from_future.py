from abjad import *
from experimental.tools import *


def test_SegmentSpecification__look_up_time_signature_setting_from_future_01():
    '''From-future time signature command reqeust.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_command = blue_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    red_segment.set_time_signatures(blue_time_signature_command)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_future_02():
    '''From-future time signature command request with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_command = blue_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    blue_time_signature_command = blue_time_signature_command.reflect()
    red_segment.set_time_signatures(blue_time_signature_command)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_future_03():
    '''From-future time signature command request with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_command = blue_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    blue_time_signature_command = blue_time_signature_command.reflect()
    red_segment.set_time_signatures(blue_time_signature_command)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__look_up_time_signature_setting_from_future_04():
    '''From-future time signature command request with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    blue_time_signature_command = blue_segment.timespan.start_offset.look_up_time_signature_setting('Voice 1')
    blue_time_signature_command = blue_time_signature_command.reflect()
    blue_time_signature_command = blue_time_signature_command.reflect()
    red_segment.set_time_signatures(blue_time_signature_command)
    blue_segment.set_time_signatures([(3, 8), (4, 8)])
    blue_segment.set_divisions([(2, 16), (6, 16)])
    blue_segment.set_rhythm(library.sixteenths)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
