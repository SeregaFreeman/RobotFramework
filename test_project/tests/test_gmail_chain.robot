*** Settings ***
Documentation    Suite description
Library  ../steps/EventsSteps.py
Library  ../steps/UsersMessagesSteps.py
Variables  ../configurations/gmail_data.py
Variables  ../configurations/test_data.py

*** Variables ***
${send_notifications}   True
${response_status}      accepted

*** Test Cases ***
Users Events Chain Test
    ${old_first_acc}          Get Messages List        ${user}       ${client}
    ${old_second_acc}         Get Messages List        ${user_second}          ${client_second}

    ${event}                  Create Random Event      ${user_second}
    ${insert_event_response}  ${insert_event_model}         Insert Event        ${user}     ${event}
    ...                                                                         ${client}        ${send_notifications}

    ${new_event}    Change Response Status      ${insert_event_model}   ${response_status}
    ${update_event_response}  ${update_event_model}         Update Event        ${user_second}   ${insert_event_model.id}
    ...                                                                         ${new_event}    ${client_second}
    ...                                                                         ${send_notifications}

    ${new_first_acc}                Get Messages List       ${user}      ${client}
    ${new_messages_first}           Get New Messages        ${old_first_acc}        ${new_first_acc}
    ${event_notif_result}           Check Notification        ${user}                      ${new_messages_first}
    ...                                                       ${event_notification_message}     ${client}       ${user_second}
    Should Be True  ${event_notif_result}

    Delete Event  ${user}   ${insert_event_model.id}     ${client}      ${send_notifications}
    ${new_second_acc}               Get Messages List        ${user_second}        ${client_second}
    ${new_messages_second}          Get New Messages        ${old_second_acc}       ${new_second_acc}
    ${delete_notif_result}          Check Notification          ${user_second}                       ${new_messages_second}
    ...                                                         ${delete_notification_message}      ${client_second}
    Should Be True  ${delete_notif_result}

    Check That Event Was Deleted    ${user_second}     ${update_event_model.id}    ${client_second}
