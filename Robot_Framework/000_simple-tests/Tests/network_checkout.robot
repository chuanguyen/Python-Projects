*** Settings ***
Documentation       Post Maintenance Change Suite
Resource            ../Resources/resources.robot
Suite Setup         Set Up Test Environment
Suite Teardown      Clean Up Test Environment

*** Test Cases ***
Layer 3 Tests
    Internet Connectivity Ping Test
    Access Webpages
