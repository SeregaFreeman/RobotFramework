*** Settings ***
Documentation    C1380: Create, modify, delete the message and check to a thread for him
...   https://testrail.a1qa.com/index.php?/cases/view/1380&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/ThreadsSteps.py
Library    ../steps/UsersMessagesSteps.py


*** Variables ***
${user_id}  qacalendarapi@gmail.com


*** Test Cases ***
Create, modify, delete, message and checking thread
    ### 1 - Выполнить keyword = "Send message"
    ${random_body_model} =    Create Random Body Message Model
    ${exp_message_model} =    Send Text Message    ${user_id}    ${random_body_model}


    ### 2 - Выполнить keyword = "Get message" по id созданного сообщения, получить thread_id
    ${working_message}    Get Message    ${user_id}    ${exp_message_model.message_id}
    Check Label Appears In Labels   ${working_message.label_ids}   SENT
    Compare Messages    ${working_message}    ${exp_message_model}

    ### 3 - Выполнить keyword = "Get thread" для полученного thread_id
    ${actual_thread}    Get Thread    ${user_id}    ${working_message.thread_id}

    ### 4 - Выполнить keyword = "Modify message", в котором добавить др. лэйбл
    ${labels}    Create Labels List    IMPORTANT
    ${modified_model}=      Modify Messages     ${user_id}    ${working_message.message_id}      ${labels}

    ### 5 - Выполнить keyword = "Get thread" для проверки добавленного лэйбла
    ${actual_thread}    Get Thread    ${user_id}    ${working_message.thread_id}
    Check Label In Thread Messages   ${actual_thread.messages}   SENT    ${working_message.message_id}
    Check Label In Thread Messages   ${actual_thread.messages}   IMPORTANT    ${working_message.message_id}

    ### 6 - Выполнить keyword = "Delete Message"
    Delete Message    ${user_id}    ${working_message.message_id}
    ${list_models} =    Get Messages List     ${user_id}
    Check Messages Not In Messages List    ${list_models}    ${working_message.message_id}