*** Settings ***
Documentation  TC1344: Create a message, label, change it, delete the label and message
...   https://testrail.a1qa.com/index.php?/cases/view/1344&group_by=cases:section_id&group_id=1295&group_order=asc
Library  ../steps/UsersMessagesSteps.py
Library  ../steps/LabelsSteps.py
Variables    ../configurations/test_data.py


*** Variables ***
${user_id}        qacalendarapi@gmail.com
${trash}          TRASH


*** Test Cases ***
Test C1344
    ${random_body_message_model} =    Create Random Body Message Model
    ${insert_message_model} =    Insert Message    ${user_id}    ${random_body_message_model}
    ${get_message_model} =    Get Iis Message    ${user_id}    ${insert_message_model.message_id}
    ${act_body_message_model} =    Get Body Message Model From Message Model     ${get_message_model}
    Compare Body Message    ${random_body_message_model}    ${act_body_message_model}

    ${random_label_model} =    Create Random Label Model
    ${create_label_model} =    Create Label    ${user_id}    ${random_label_model}
    ${act_label_model} =    Get Label    ${create_label_model.label_id}    ${user_id}
    Check That Models Labels Are Equal    ${random_label_model}    ${act_label_model}

    ${labels_list_name} =     Get Labels List Name    ${labels}
    ${modified_model} =    Modify Messages    ${user_id}    ${insert_message_model.message_id}    ${labels_list_name}
    ${actual_model} =    Get Message    ${user_id}    ${insert_message_model.message_id}
    Check Lists Is Equal    ${labels_list_name}    ${actual_model.label_ids}

    ${random_label_model_for_update}    Create Random Label Model
    ${update_label_model} =    Update Label    ${user_id}    ${act_label_model.label_id}    ${random_label_model_for_update}
    ${get_label_model} =    Get Label    ${update_label_model.label_id}    ${user_id}
    Check That Models Labels Are Equal    ${random_label_model_for_update}    ${get_label_model}

    Delete Label    ${user_id}    ${get_label_model.label_id}
    ${list_labels} =    List Label    ${user_id}
    Check Label Not In Labels List    ${get_label_model.label_id}    ${list_labels}

    Trash Message    ${user_id}    ${insert_message_model.message_id}
    ${trash_message_model} =    Get Message    ${user_id}    ${insert_message_model.message_id}
    Check List Contains Element    ${trash_message_model.label_ids}    ${trash}

    Delete Message    ${user_id}    ${insert_message_model.message_id}
    ${list_message_model} =    Get Messages List    ${user_id}
    Check Message Not In List    ${list_message_model}    ${insert_message_model.message_id}
