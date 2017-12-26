*** Settings ***
Documentation    TC1393: Create, delete the frowarding address and the forwarding letter
...   https://testrail.a1qa.com/index.php?/cases/view/1393&group_by=cases:section_id&group_id=1295&group_order=asc
Library     ../steps/ForwardingSteps.py
Library     ../steps/UsersMessagesSteps.py
Variables   ../configurations/gmail_data.py


*** Variables ***
${file_name}   test.txt


*** Test Cases ***
Check Mail Forwarding
    ${old_list}             Get Messages List       ${user_second}      ${client_second}
    ${forwarding_list}      Get forwarding addresses list       ${user}
    Check address in list   ${forwarding_list}      ${user_second}

    ${message_body}         Create Random Body Message Model With Attach    ${file_name}        ${user}
    ${sended_message}       Send Message With Attach    ${user}     ${message_body}
    ${actual_message}       Get Message     ${user}             ${sended_message.message_id}        ${client}

    ${new_list}             Get Messages List       ${user_second}      ${client_second}
    ${new_messages}         Get New Messages    ${old_list}     ${new_list}
    Check Notification      ${user_second}      ${new_messages}     ${actual_message.snippet}       ${client_second}