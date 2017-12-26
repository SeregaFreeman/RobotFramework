*** Settings ***
Documentation    Suite description
Library  ../steps/SettingsSteps.py

*** Test Cases ***
Test Settings get
    ${settings_list}=       Send Request Get Settings List
    ${expected_setting}=    Get Random Setting From Settings List   ${settings_list}
    ${responce_setting}=    Send Request Get Setting By Id          ${expected_setting.id}
    Compare Settings        ${responce_setting}                     ${expected_setting}

Test Settings List
    ${model_list}=          Send Request Get Settings List
    ${expected_model}=      Get Setting From File
    ${settings_exists}=     Check That Setting Exist        ${expected_model}
    Should Be True          ${settings_exists}