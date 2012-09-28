import py
from abjad import *
from experimental import *


def test_SegmentSpecification_request_division_command_from_future_between_voices_01():
    '''From-future division command request between voices.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_voice_2_division_command = blue_segment.request_division_command('Voice 2')
    red_segment.set_divisions(blue_voice_2_division_command, contexts=['Voice 1'])
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
