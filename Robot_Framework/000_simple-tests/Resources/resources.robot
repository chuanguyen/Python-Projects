*** Settings ***
Library             SSHLibrary
Library             SeleniumLibrary

*** Variables ***
${HOST}             localhost
${USERNAME}         %{ROBOT_SSH_USERNAME}
${PASSWORD}         %{ROBOT_SSH_PASSWORD}
${BROWSER}          Chrome

*** Keywords ***
Set Up Test Environment
    [Documentation]     Preps environment for test suite
    Open Connection And Log In
    Open Browser       browser=${BROWSER}

Open Connection And Log In
    Open Connection         ${HOST}
    Login                   ${USERNAME}     ${PASSWORD}

Internet Connectivity Ping Test
    [Documentation]     Ping Test To 8.8.8.8
    ${output}=          Execute Command     ping 8.8.8.8 -c 1
    Should Contain      ${output}           64 bytes from 8.8.8.8

Access Google.ca
    [Documentation]     Validates whether the page loads
    Go To               https://www.google.ca
    Run Keyword And Continue On Failure     Title Should Be     Google
    Run Keyword And Continue On Failure     Page Should Contain Button      Google Search


Clean Up Test Environment
    [Documentation]     Cleanup of test environment
    Close All Connections
    Close Browser