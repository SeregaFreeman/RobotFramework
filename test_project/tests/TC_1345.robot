*** Settings ***
Documentation   C1345: Create, update, send draft, delete and delete from trash
...   https://testrail.a1qa.com/index.php?/cases/view/1345&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/UserDraftsSteps.py
Library    ../steps/UsersMessagesSteps.py


*** Variables ***
${user_id}     qacalendarapi@gmail.com
${trash_label}    TRASH


*** Test Cases ***
Create, update, send draft, delete and delete from trash
    ${expected_draft_model}=    create draft message    ${user_id}
    ${actual_draft_model}=    get draft message    ${user_id}    ${expected_draft_model.draft_message_id}
    check models equals    ${expected_draft_model}    ${actual_draft_model}

    ${expected_update_draft_model}=    update draft message    ${user_id}    ${expected_draft_model.draft_message_id}
    ${actual_draft_update_model}=    get draft message    ${user_id}    ${expected_draft_model.draft_message_id}
    check models equals    ${expected_update_draft_model}    ${actual_draft_update_model}

    ${expected_sent_draft_model}=    send draft message    ${user_id}    ${expected_draft_model.draft_message_id}

    ${messages_list_models}=    get messages list    ${user_id}
    check message appear in list    ${messages_list_models}    ${expected_sent_draft_model.message_id}

    trash message    ${user_id}    ${expected_sent_draft_model.message_id}
    ${message_model}=    get message    ${user_id}    ${expected_sent_draft_model.message_id}
    check label appears in labels    ${message_model.label_ids}    ${trash_label}

    untrash message    ${user_id}    ${expected_sent_draft_model.message_id}
    check message appear in list    ${messages_list_models}    ${expected_sent_draft_model.message_id}

    delete message    ${user_id}    ${expected_sent_draft_model.message_id}
    check message is deleted    ${user_id}    ${expected_sent_draft_model.message_id}