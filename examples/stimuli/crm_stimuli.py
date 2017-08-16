# -*- coding: utf-8 -*-
"""
========================
Generate vocoded stimuli
========================

This shows how to use the CRM corpus functions.

@author: rkmaddox
"""

from expyfun._utils import _TempDir
from expyfun import ExperimentController, analyze
from expyfun.stimuli import (crm_prepare_corpus, crm_sentence, crm_info,
                             crm_response_menu, add_pad, CRMPreload)

print(__doc__)

crm_path = _TempDir()
fs = 40000
ec_args = dict()

# prepare the corpus for two talkers at the native 40000 Hz sampling rate
# NOTE: For your experiment, you only need to prepare the corpus once per
# sampling rate, you should probably use the default path, and you should just
# do all the talkers at once. For the example, we are using fs=40000 and only
# doing two talkers so that the stimulus preparation is very fast, and a temp
# directory so that we don't interfere with any other prepared corpuses. Your
# code will likely look like this commented line, and not appear in your
# actual experiment script:
# crm_prepare_corpus(fs)  # where fs is likely 24414 or 44100
crm_prepare_corpus(fs, path_out=crm_path, overwrite=True,
                   talker_list=[dict(sex=0, talker_num=0),
                                dict(sex=1, talker_num=0)])

# print the valid callsigns
print('Valid callsigns are {0}'.format(crm_info()['callsign']))

# read a sentence in from the hard drive
x1 = 0.5 * crm_sentence(fs, 'm', '0', 'c', 'r', '5', path=crm_path)

# preload all the talkers and get a second sentence
crm = CRMPreload(fs, path=crm_path)
x2 = crm.sentence('f', '0', 'ringo', 'green', '6')

x = add_pad([x1, x2], alignment='start')

with ExperimentController(
        exp_name='CRM corpus example', window_size=(720, 480),
        full_screen=False, participant='foo', session='foo', version='dev',
        output_dir=None, stim_fs=40000) as ec:
    ec.screen_text('Report the color and number spoken by the female '
                   'talker.', wrap=True)
    screenshot = ec.screenshot()
    ec.flip()
    ec.wait_secs(3)

    ec.load_buffer(x)
    ec.identify_trial(ec_id='', ttl_id=[])
    ec.start_stimulus()
    ec.wait_secs(x.shape[-1] / float(fs))

    resp = crm_response_menu(ec)
    if resp == ('g', '6'):
        ec.screen_prompt('Correct!', max_wait=1, min_wait=1)
    else:
        ec.screen_prompt('Incorrect.', max_wait=1, min_wait=1)
    ec.trial_ok()

analyze.plot_screen(screenshot)
