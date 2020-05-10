# Example
# -------
#
#   a simple, sequential job file

# To run the job:
# pyats run job {JOB FILE} --testbed-file {testbed_file.yaml}
# easypy {JOB FILE} -testbed_file {testbed_file.yaml}

import os
from pyats.easypy import run

# main() function must be defined in each job file
#   - it should have a runtime argument
#   - and contains one or more tasks
def main(runtime):

    # provide custom job name for reporting purposes (optional)
    runtime.job.name = 'my-job'

    # compute relative location of this file
    pwd = os.path.dirname(__file__)
    aeTestFileName = "aeTest-interfaces.py"
    testFilePath = os.path.join(pwd, aeTestFileName)

    # using run() api to run a task
    #
    # syntax
    # ------
    #   run(testscript = <testscript path/file>,
    #       runtime = <runtime object>,
    #       max_runtime = None,
    #       taskid = None,
    #       **kwargs)
    #
    #   any additional arguments (**kwargs) to run() api are propagated
    #   to AEtest as input arguments.
    # run this script as a task under this job
    # Note:
    #   if --testbed-file is provided, the corresponding loaded 'testbed'
    #   object will be provided to each script within this job automatically
    run(testscript=testFilePath)
