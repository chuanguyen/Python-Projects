*** Settings ***
Library             SSHLibrary

*** Variables ***
${HOST}             %{ROBOT_SSH_HOST=localhost}
${USERNAME}         %{ROBOT_SSH_USERNAME}
${PASSWORD}         %{ROBOT_SSH_PASSWORD}

*** Keywords ***
Open Connection And Log In
    Open Connection         ${HOST}
    Login                   ${USERNAME}     ${PASSWORD}

Ping Internet
    [Documentation]     Ping Test To 8.8.8.8
    ${output}=          Execute Command     ping 8.8.8.8 -c 4
    Run Keyword And Continue On Failure        Should Contain      ${output}           64 bytes from 8.8.8.8
