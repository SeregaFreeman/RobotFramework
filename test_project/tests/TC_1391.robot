*** Settings ***
Documentation    C1391: Display information about creating and deleting messages in history
...   https://testrail.a1qa.com/index.php?/cases/view/1391&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/UsersMessagesSteps.py
Library    ../steps/ThreadsSteps.py
Library    ../steps/HistorySteps.py
Variables    ../configurations/gmail_data.py


*** Test Cases ***
Display information about creating and deleting messages in history
    ${random_message}    Create Random Body Message Model
    ${exp_message_model}    Insert Message    ${user}    ${random_message}

    ${actual_message_model}    Get Message    ${user}    ${exp_message_model.message_id}
    Compare messages    ${actual_message_model}    ${exp_message_model}

    ${thread_model}    Get Thread    ${user}    ${actual_message_model.thread_id}

    ${random_message_second}    Create Random Body Message Model
    ${exp_message_model_second}    Insert Message    ${user}    ${random_message_second}
    ${actual_message_model_second}    Get Message    ${user}    ${exp_message_model_second.message_id}
    Compare Messages    ${actual_message_model_second}    ${exp_message_model_second}
    ${response}    ${history_model}    Get History List    ${user}    ${thread_model.history_id}
    Check That Message Added    ${response}    ${actual_message_model_second.message_id}

    Delete Message    ${user}    ${exp_message_model_second.message_id}
    ${response}    ${history_model}    Get History List    ${user}    ${thread_model.history_id}
    Check That Message Deleted    ${response}    ${actual_message_model_second.message_id}

    Delete Message    ${user}    ${exp_message_model.message_id}