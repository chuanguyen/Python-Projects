*** Settings ***
Library             SSHLibrary
Library             RPA.Robocorp.Vault
Library             OperatingSystem

*** Variables ***
# ${HOST}             %{ROBOT_SSH_HOST=localhost}
# ${USERNAME}         %{ROBOT_SSH_USERNAME}
# ${PASSWORD}         %{ROBOT_SSH_PASSWORD}
${local_RPA_SECRET_FILE}         %{RPA_SECRET_FILE}

*** Keywords ***
Set Up Test Environment
    [Documentation]     Preps environment for test suite
    Open Connection And Log In

Open Connection And Log In
    Open Connection         ${HOST}
    Login                   ${USERNAME}     ${PASSWORD}

Ping Internet
    [Documentation]     Ping Test To 8.8.8.8
    ${output}=          Execute Command     ping 8.8.8.8 -c 1
    Should Contain      ${output}           64 bytes from 8.8.8.8

Retrieve Secret
    Log variables
    # ${secret}=          Get Secret          credentials
    # Log                 $(secret)[username]
    # Log                 $(secret)[password]

Clean Up Test Environment
    [Documentation]     Cleanup of test environment
