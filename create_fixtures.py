import numpy as np
import yaml

import lif_meanfield_tools as lmt
ureg = lmt.ureg

fixture_path = 'tests/fixtures/'

cases = [0, 1]
for case in cases:
    if case == 0:
        parameters = 'examples/network_params_microcircuit.yaml'
        regime = 'noise_driven'
    elif case == 1:
        parameters = 'examples/minimal_negative.yaml'
        regime = 'negative_firing_rate'
    elif case == 2:
        parameters = 'examples/small_network.yaml'
        regime = 'mean_driven'
    else:
        print('Case not defined! Choose existing case, '
              'otherwise nothing happens!')

    network = lmt.Network(parameters, 'examples/analysis_params_test.yaml')

    network.working_point()

    network.transfer_function(method='shift')
    tf_shift = network.results.pop('transfer_function')

    network.transfer_function(method='taylor')
    tf_taylor = network.results.pop('transfer_function')

    params = network.network_params

    fixtures = dict(params, **network.results)
    fixtures = dict(fixtures, **network.analysis_params)

    fixtures = lmt.input_output.quantities_to_val_unit(fixtures)

    for k, v in fixtures.items():
        try:
            fixtures[k] = v.tolist()
        except AttributeError:
            try:
                fixtures[k]['val'] = v['val'].tolist()
            except AttributeError:
                pass
            except TypeError:
                pass

    with open('{}{}_regime.yaml'.format(fixture_path, regime), 'w') as file:
        yaml.dump(fixtures, file)

    np.save('{}transfer_function_shift_{}.npy'.format(fixture_path, regime),
            tf_shift)
    np.save('{}transfer_function_taylor_{}.npy'.format(fixture_path, regime),
            tf_taylor)
