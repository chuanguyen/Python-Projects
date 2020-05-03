# To run the job:
# pyats run job {JOB FILE} --testbed-file {testbed_file.yaml}
# easypy {JOB FILE} -testbed_file {testbed_file.yaml}

import os
from ats.easypy import run

def main(runtime):
    'main entry point for a job is the main() function'

    # compute relative location of this file
    pwd = os.path.dirname(__file__)
    aeTestFileName = "aeTest.py"
    testFilePath = os.path.join(pwd, aeTestFileName)

    # run this script as a task under this job
    # Note:
    #   if --testbed-file is provided, the corresponding loaded 'testbed'
    #   object will be provided to each script within this job automatically
    run(testscript=testFilePath)
