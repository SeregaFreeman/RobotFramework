*** Settings ***
Documentation    C1407: Create a message, add and return from spam, delete the message
...   https://testrail.a1qa.com/index.php?/cases/view/1407&group_by=cases:section_id&group_id=1295&group_order=asc
Library  ../steps/ThreadsSteps.py
Library  ../steps/UsersMessagesSteps.py
Variables  ../configurations/gmail_data.py

*** Test Cases ***
Modify Messages Labels In Thread
    ### 1
    ${random_message}    Create Random Body Message Model
    ${exp_message_model}    Insert Message    ${user}    ${random_message}

    ### 2
    ${label}    Get Random Label From List    INBOX    IMPORTANT
    ${labels}    Create Labels List    ${label}
    ${act_message_model}    Modify Messages    ${user}    ${exp_message_model.message_id}    add_labels_list=${labels}
    ${modified_message_model}    Get Message    ${user}    ${exp_message_model.message_id}
    Check Label In Labels List    ${label}    ${modified_message_model.label_ids}

    ### 3
    ${labels}    Create Labels List    SPAM
    ${thread_model}    Modify Thread    ${user}    ${modified_message_model.thread_id}    add_labels_list=${labels}
    ${modified_message_model}    Get Message    ${user}    ${exp_message_model.message_id}
    Check Labels Lists Are Equal    ${labels}    ${modified_message_model.label_ids}

    ### 4
    Full Modify Messages    ${user}    ${exp_message_model.message_id}    remove_labels_list=${labels}

    ### 5
    ${thread_model}    Get Thread    ${user}    ${modified_message_model.thread_id}
    Check Messages Without Labels    ${thread_model.messages}

    ### 6
    Delete Thread    ${user}    ${thread_model.thread_id}
    Check Thread Is Deleted    ${user}    ${thread_model.thread_id}

    ### 7
    ${messages_list}    Get Messages List    ${user}
    Check Message Not In List    ${messages_list}    ${modified_message_model.message_id}
