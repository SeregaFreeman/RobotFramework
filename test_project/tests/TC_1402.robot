*** Settings ***
Documentation    C1402: Add and delete a lablel for a thread and message
...   https://testrail.a1qa.com/index.php?/cases/view/1402&group_by=cases:section_id&group_id=1295&group_order=asc
Library  ../steps/ThreadsSteps.py
Library  ../steps/UsersMessagesSteps.py
Variables  ../configurations/gmail_data.py

*** Variables ***


*** Test Cases ***
Modify Messages Labels In Thread
    ### 1 - Выполнить keyword = Insert message
    ${random_message}    Create Random Body Message Model
    ${exp_message_model}    Insert Message    ${user}    ${random_message}

    ### 2 - Выполнить keyword = Get message по id созданного сообщения, получить thread_id
    ${act_message_model}    Get Message    ${user}    ${exp_message_model.message_id}
    Compare Messages    ${exp_message_model}    ${act_message_model}

    ### 3 - Выполнить keyword = Get thread для полученного thread_id
    ${get_thread_response_model}    Get Thread    ${user}    ${act_message_model.thread_id}

    ### 4 - Добавить лейбл к thread. Выполнить keyword = Modify thread
    ${label}    Get Random Default Label To Add
    ${labels}    Create Labels List    ${label}
    Modify Thread    ${user}    ${get_thread_response_model.thread_id}    add_labels_list=${labels}

    ### 5 - Проверить, что лейбл добавлен для сообщения из thread.
    ### Для этого выполнить keyword = Get message для сообщения из шага 1
    ${modified_message_model}    Get Message    ${user}    ${exp_message_model.message_id}
    Check Label In Labels List    ${label}    ${modified_message_model.label_ids}

    ### 6 - Выполнить keyword = Trash thread
    Trash Thread    ${user}    ${get_thread_response_model.thread_id}
    ${threads_list_models_list}    List Threads    ${user}
    Check Thread Is Not In List    ${get_thread_response_model.thread_id}    ${threads_list_models_list}

    ### 7 - Выполнить keyword = Untrash thread
    Untrash Thread    ${user}    ${get_thread_response_model.thread_id}
    ${threads_list_models_list}    List Threads    ${user}
    Check Thread Is In List    ${get_thread_response_model.thread_id}    ${threads_list_models_list}

    ### 8 - Выполнить keyword = Delete thread
    Delete Thread    ${user}    ${get_thread_response_model.thread_id}
    Check Thread Is Deleted    ${user}    ${get_thread_response_model.thread_id}