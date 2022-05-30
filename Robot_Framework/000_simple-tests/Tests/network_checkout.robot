*** Settings ***
Documentation       Post Maintenance Change Suite
Resource            ../Resources/resources.robot
Suite Setup         Open Connection And Log In
Suite Teardown      Close All Connections

*** Test Cases ***
Basic Layer 3 Tests
    Ping Internet
