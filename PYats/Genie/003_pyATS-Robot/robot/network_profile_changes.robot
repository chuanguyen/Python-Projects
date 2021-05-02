** Settings **
Documentation   Gathers network state and configuration and compares to baseline

# Importing test libraries, resource files and variable files.
Library        pyats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot

** Variables **
${BASELINE DIR}   ./robot/profile_baseline/baseline
${DIFF DIR}       ./robot/profile_diffs/diffs
${TESTBED}        testbed.yml

${DEVICES TO CONNECT}   SEPARATOR=
...                     cml-r1

${GENIE MODELS}   SEPARATOR=
...               config;interface;
...               vlan;routing

*** Test Cases ***
# Creating test cases from available keywords.

Connecting
  [Documentation]   Setup connections to devices
  use genie testbed "${testbed}"
  connect to devices "${devices To Connect}"

Profile changed config
  [Documentation]   Retrieves and stores state and configuration data post-change
  Profile the system for "${GENIE MODELS}" on devices "${DEVICES TO CONNECT}" as "${DIFF DIR}"

Compare changes to the baseline
  [Documentation]   Compares changes against baseline
  Compare profile "${BASELINE DIR}" with "${DIFF DIR}" on devices "${DEVICES TO CONNECT}"
