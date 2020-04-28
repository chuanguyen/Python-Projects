# Take snapshot of the operational state of the device
# and compare against baseline

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        genie.libs.robot.GenieRobot
Library        pyats.robot.pyATSRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
${testbed}  testbed.yaml

# Define verification datafile to use
${verification_datafile}  %{VIRTUAL_ENV}/genie_yamls/ios/verification_datafile_ios.yaml

*** Test Cases ***
# Creating test cases from available keywords.

Connecting
  use genie testbed "${testbed}"

  # Connecting to devices
  connect to device "R3" via "mgmt"
  connect to device "R5" via "mgmt"

Testing
  # Verify counts
  [Tags]  noncritical
  verify count "6" "interface up" on device "R3"

  # Verify version; fails on GNS3; most likely because it's a virtual device
  # run verification "Verify_Version" on device "R3"

  # Like the learn Keyword, no output to analyze; doesn't seem useful
  ${output}=  parse "show version" on device "R3"

  # Doesn't seem too useful to me; no output to analyze
  ${output}=  learn "interface" on device "R3"
