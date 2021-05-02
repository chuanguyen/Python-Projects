** Settings ***
Documentation   Gathers network state and configuration for analysis

# Importing test libraries, resource files and variable files.
Library        pyats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot

** Variables **
# Define the pyATS testbed file to use for this run
# Location is relative to job runner
${BASELINE DIR}   robot/profile_baseline/baseline
${TESTBED}        testbed.yml

${DEVICES TO CONNECT}   SEPARATOR=
...                     cml-r1

${GENIE MODELS}   SEPARATOR=
...               config;interface;
...               vlan;routing

*** Test Cases ***

Connecting to devices
  [Documentation]   Setup connections to devices
  use genie testbed "${testbed}"
  connect to devices "${devices To Connect}"

Profile baseline config
  [Documentation]   Retrieves and stores state and configuration data
  Profile the system for "${GENIE MODELS}" on devices "${DEVICES TO CONNECT}" as "${BASELINE DIR}"
