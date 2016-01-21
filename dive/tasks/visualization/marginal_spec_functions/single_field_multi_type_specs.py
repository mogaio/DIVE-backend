from itertools import combinations
from dive.tasks.visualization import GeneratingProcedure as GP, TypeStructure as TS, \
    TermType, aggregation_functions, VizType as VT

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def single_ct(c_field, t_field):
    logger.debug('Single C Single T - %s, %s', c_field['name'], t_field['name'])
    specs = []

    return specs


def single_cq(c_field, q_field):
    specs = []
    c_label = c_field['name']
    q_label = q_field['name']
    logger.debug('D: Single C Single Q')

    if c_field['is_unique']:
        spec = {
            'case': 'single_cq',
            'generating_procedure': GP.VAL_VAL.value,
            'type_structure': TS.C_Q.value,
            'viz_types': [ VT.BAR.value, VT.TREE.value, VT.PIE.value ],
            'field_ids': [ c_field['id'], q_field['id'] ],
            'args': {
                'field_a': c_field,
                'field_b': q_field,
            },
            'meta': {
                'desc': '%s vs. %s ' % (c_label, q_label),
                'construction': [
                    { 'string': c_label, 'type': TermType.FIELD.value },
                    { 'string': 'vs.', 'type': TermType.PLAIN.value },
                    { 'string': q_label, 'type': TermType.FIELD.value },
                ]
            }
        }
        specs.append(spec)
    else:
        for agg_fn in aggregation_functions.keys():
            if agg_fn == 'count':
                continue

            spec = {
                'case': 'single_cq',
                'generating_procedure': GP.VAL_AGG.value,
                'type_structure': TS.C_Q.value,
                'viz_types': [ VT.BAR.value ],
                'field_ids': [ c_field['id'], q_field['id'] ],
                'args': {
                    'agg_fn': agg_fn,
                    'grouped_field': c_field,
                    'agg_field': q_field,
                },
                'meta': {
                    'desc': '%s of %s by %s' % (agg_fn, q_label, c_label),
                    'construction': [
                        { 'string': agg_fn, 'type': TermType.OPERATION.value },
                        { 'string': 'of', 'type': TermType.PLAIN.value },
                        { 'string': q_label, 'type': TermType.FIELD.value },
                        { 'string': 'by', 'type': TermType.OPERATION.value },
                        { 'string': c_label, 'type': TermType.FIELD.value },
                    ]
                }
            }
            specs.append(spec)
    return specs


def single_tq(t_field, q_field):
    t_label = t_field['name']
    q_label = q_field['name']

    logger.debug('Single T Single Q - %s, %s', t_label, q_label)
    specs = []

    # Raw time vs. value
    if t_field['is_unique']:
        raw_time_series_spec = {
            'case': 'single_tq',
            'generating_procedure': GP.VAL_VAL.value,
            'type_structure': TS.T_Q.value,
            'viz_types': [ VT.LINE.value, VT.SCATTER.value ],
            'field_ids': [ c_field['id'], q_field['id'] ],
            'args': {
                'field_a': t_field,
                'field_b': q_field
            },
            'meta': {
                'desc': '%s vs. %s' % (t_label, q_label),
                'construction': [
                    { 'string': t_label, 'type': TermType.FIELD.value },
                    { 'string': 'vs.', 'type': TermType.PLAIN.value },
                    { 'string': q_label, 'type': TermType.FIELD.value },
                ]
            }
        }
        specs.append(raw_time_series_spec)

    for agg_fn in aggregation_functions.keys():
        aggregated_time_series_spec_on_value = {
            'case': 'single_tq',
            'generating_procedure': GP.VAL_AGG.value,
            'type_structure': TS.T_Q.value,
            'viz_types': [ VT.LINE.value, VT.SCATTER.value ],
            'field_ids': [ c_field['id'], q_field['id'] ],
            'args': {
                'agg_fn': agg_fn,
                'grouped_field': t_field,
                'agg_field': q_field
            },
            'meta': {
                'desc': '%s of %s by %s' % (agg_fn, q_label, c_label),
                'construction': [
                    { 'string': agg_fn, 'type': TermType.OPERATION.value },
                    { 'string': 'of', 'type': TermType.PLAIN.value },
                    { 'string': q_label, 'type': TermType.FIELD.value },
                    { 'string': 'by', 'type': TermType.OPERATION.value },
                    { 'string': t_label, 'type': TermType.FIELD.value },
                ]
            }
        }
        specs.append(aggregated_time_series_spec_on_value)

    return specs


def single_ctq(c_field, t_field, q_field):
    specs = []
    logger.debug('Single C Single T Single Q')
    return specs
