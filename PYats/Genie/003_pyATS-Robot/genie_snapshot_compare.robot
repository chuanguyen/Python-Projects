# Take snapshot of the operational state of the device
# and compare against baseline

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        genie.libs.robot.GenieRobot
Library        pyats.robot.pyATSRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
${testbed}     testbed.yaml
${BASE}        baseline/baseline
${CURRENT}     change/snapshot

*** Test Cases ***
# Creating test cases from available keywords.

Connecting
  use genie testbed "${testbed}"

  # Connecting to devices
  connect to device "R3" via "mgmt"
  connect to device "R5" via "mgmt"

Profile devices for any operational state changes
  Profile the system for "interface;routing;arp" on devices "R3;R5" as "${CURRENT}"

Compare snapshots
  # Compare baseline snapshot against current state
  Compare profile "${BASE}" with "${CURRENT}" on devices "R3;R5"
