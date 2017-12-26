*** Settings ***
Documentation   C1401: Create, update, delete an account for "Send as"
...   https://testrail.a1qa.com/index.php?/cases/view/1401&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/SendAsSteps.py
Variables  ../configurations/gmail_data.py


*** Variables ***
${user_added_allias}    test2


*** Test Cases ***
Checking accounts for "Send as"
    ${expected_model_send_as}=    Patch Send As    ${user}    ${user}
    ${actual_model_send_as}=    Get Send As    ${user}    ${user}
    Check Models Equals    ${expected_model_send_as}    ${actual_model_send_as}

    ${expected_model_send_as}=    Update Send As    ${user}    ${user}
    ${actual_model_send_as}=    Get Send As    ${user}    ${user}
    Check Models Equals    ${expected_model_send_as}    ${actual_model_send_as}

    ${send_as_list_models}=    Get Send As List    ${user}
    Check Send As In List    ${send_as_list_models}    ${user_added_allias}    ${user_second}