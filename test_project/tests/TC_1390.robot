*** Settings ***
Documentation    C1390: Changing messages count in profile
...   https://testrail.a1qa.com/index.php?/cases/view/1390&group_by=cases:section_id&group_id=1295&group_order=asc
Library  ../steps/UsersSteps.py
Library  ../steps/UsersMessagesSteps.py


*** Variables ***
${user_id}                   qacalendarapi@gmail.com
${added_messages_count}    0
${deleted_messages_count}    0


*** Test Cases ***
Modify Messages Count In Profile
    ### 1 - Выполнить keyword = Get profile и получить количество сообщений в ящике
    ${user_model_previous}   Get Profile    user_id=${user_id}

    ### 2 - Выполнить keyword = Insert message
    ${random_message}    Create Random Body Message Model
    ${message_model}    Insert Message    user_id=${user_id}    insert_model=${random_message}
    ${added_messages_count}    Increase Int For One    ${added_messages_count}

    ### 3 - Проверить, что количество сообщений увеличилось на число созданных ( 1 ). Выполнить keyword = Get Profile
    ${user_model_increased}    Get Profile    user_id=${user_id}
    Check Messages Count Increased    previous_count=${user_model_increased.messages_total}
    ...                               actual_count=${user_model_previous.messages_total}
    ...                               changed_count_added=${added_messages_count}

    ### 4 - Удалить любое сообщение из ящика. Выполнить keyword = Delete message
    Delete Message   user_id=${user_id}    message_id=${message_model.message_id }
    ${deleted_messages_count}    Increase Int For One    ${deleted_messages_count}

    ### 5 - Проверить, что количество сообщений уменьшилось на число удаленных ( 1 ). Выполнить keyword = Get Profile
    ${user_model_decreased}    Get Profile    user_id=${user_id}
    Check Messages Count Decreased    previous_count=${user_model_previous.messages_total}
    ...                               actual_count=${user_model_decreased.messages_total}
    ...                               changed_count_added=${added_messages_count}
    ...                               changed_count_deleted=${deleted_messages_count}



