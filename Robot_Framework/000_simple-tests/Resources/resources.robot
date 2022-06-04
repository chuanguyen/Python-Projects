*** Settings ***
Library             SSHLibrary
Library             SeleniumLibrary
Variables           ./resources_variables.yml

*** Variables ***
${HOST}             %{ROBOT_SSH_HOST=localhost}
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

Ping Internet
    [Documentation]     Ping Test To 8.8.8.8
    ${output}=          Execute Command     ping 8.8.8.8 -c 1
    Should Contain      ${output}           64 bytes from 8.8.8.8

Access Webpages
    [Documentation]     Validates whether the page loads
    Log Variables
    FOR     ${site}     IN  @{Sites_to_Test}
        Go To               ${site["url"]}
        Run Keyword And Continue On Failure     Title Should Be     ${site["title"]}
    END


Clean Up Test Environment
    [Documentation]     Cleanup of test environment
    Close All Connections
    Close Browser
