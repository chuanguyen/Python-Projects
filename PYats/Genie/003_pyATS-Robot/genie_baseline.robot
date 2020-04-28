# Take initial snapshot of the operational state of the device
# and save the output to a file

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        genie.libs.robot.GenieRobot
Library        pyats.robot.pyATSRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
${testbed}     testbed.yaml
${PTS}         baseline/baseline

*** Test Cases ***
# Creating test cases from available keywords.

Connecting
  use genie testbed "${testbed}"

  # Connecting to devices
  connect to device "R3" via "mgmt"
  connect to device "R5" via "mgmt"

Profile devices for baseline
  Profile the system for "interface;routing;arp" on devices "R3;R5" as "${PTS}"
