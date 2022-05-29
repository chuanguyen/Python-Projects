*** Settings ***
Library             SSHLibrary

*** Variables ***
${HOST}             localhost
${USERNAME}         %{ROBOT_SSH_USERNAME}
${PASSWORD}         %{ROBOT_SSH_PASSWORD}

*** Keywords ***
Open Connection And Log In
    Open Connection         ${HOST}
    Login                   ${USERNAME}     ${PASSWORD}

Internet Connectivity Ping Test
    [Documentation]     Ping Test To 8.8.8.8
    ${output}=          Execute Command     ping 8.8.8.8 -c 1
    Should Contain      ${output}           64 bytes from 8.8.8.8