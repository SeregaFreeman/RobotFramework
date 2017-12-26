*** Settings ***
Library    ../steps/UsersMessagesSteps.py
Variables    ../configurations/test_data.py

*** Variables ***
${user_id}    qacalendarapi@gmail.com
${img_file_name}    img.png
${txt_file_name}    test.txt

*** Test Cases ***
Batch Modify Test
    ${first_model} =            Create Random Body Message Model
    ${first_model_message} =    Insert Message   ${user_id}     ${first_model}
    ${second_model} =           Create Random Body Message Model
    ${second_model_message} =   Insert Message   ${user_id}        ${second_model}
    ${labels_list} =            Get Labels List Name  ${labels}
    ${list_id} =                Convert To List     ${first_model_message.message_id}
    ...                                             ${second_model_message.message_id}
    Batch Modify    ${user_id}    ${list_id}    ${labels_list}
    ${get_first_model} =    Get Message    ${user_id}
    ...                                    ${first_model_message.message_id}
    Should Be Equal As List    ${labels_list}    ${get_first_model.label_ids}    Model [${first_model_message.message_id}] don't contains ${labels_list}
    ${get_second_model} =    Get Message    ${user_id}
    ...                                     ${second_model_message.message_id}
    Should Be Equal As List    ${labels_list}    ${get_second_model.label_ids}    Model [${second_model_message.message_id}] don't contains ${labels_list}

Batch Delete Test
    ${first_model} =            Create Random Body Message Model
    ${first_model_message} =    Insert Message   ${user_id}     ${first_model}
    ${messages_id_list} =       Get Random Messages Id List    ${user_id}
    Batch Delete  ${user_id}    ${messages_id_list}
    ${messaged_models_list}=    Get Messages List    ${user_id}
    Check Messages Not In Messages List  ${messaged_models_list}    ${messages_id_list}

Trash Message Test
    ${random_body_model} =    Create Random Body Message Model
    ${model_message} =    Insert Message   ${user_id}    ${random_body_model}
    Trash Message    ${user_id}    ${model_message.message_id}
    ${list_models} =    Get Messages List     ${user_id}
    ${result} =    Check Message In List    ${list_models}    ${model_message.message_id}
    Should Not Be True    ${result}    Message {${model_message.message_id}} not moved to the trash

Untrash Message
    ${random_body_model} =    Create Random Body Message Model
    ${model_message} =    Insert Message   ${user_id}    ${random_body_model}
    Trash Message    ${user_id}    ${model_message.message_id}
    ${list_models} =    Get Messages List     ${user_id}
    ${result} =    Check Message In List    ${list_models}    ${model_message.message_id}
    Should Not Be True    ${result}    Message {${model_message.message_id}} not moved to the trash
    ${untrash_message} =    Untrash Message    ${user_id}    ${model_message.message_id}
    ${list_models_with_untrash} =    Get Messages List     ${user_id}
    ${result_with_untrash} =    Check Message In List    ${list_models_with_untrash}    ${untrash_message.message_id}
    Should Be True    ${result_with_untrash}    Error when untrash message {${untrash_message.message_id}}

Test Delete Message
    ${random_body_model} =    Create Random Body Message Model
    ${model_message} =    Insert Message   ${user_id}       ${random_body_model}
    Delete Message    ${user_id}    ${model_message.message_id}
    ${list_models} =    Get Messages List     ${user_id}
    ${result} =    Check Message In List    ${list_models}    ${model_message.message_id}
    Should Not Be True    ${result}    Message {${model_message.message_id}} not moved to the trash

Test Modify Message
    ${random_body_model} =  Create Random Body Message Model
    ${model_message} =      Insert Message   ${user_id}     ${random_body_model}
    ${labels} =             Get Labels List Name  ${labels}
    ${modified_model}=      Modify Messages     ${user_id}    ${model_message.message_id}      ${labels}
    ${actual_model}=        Get Message         ${user_id}    ${model_message.message_id}
    Compare Messages        ${modified_model}   ${actual_model}


Test Insert Message
    ${random_body_model} =    Create Random Body Message Model
    ${exp_message_model} =    Insert Message    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Message       ${user_id}    ${exp_message_model.message_id}
    Compare Messages    ${exp_message_model}    ${act_message_model}
    Delete Message    ${user_id}    ${exp_message_model.message_id}

Test Send Message
    ${random_body_model} =    Create Random Body Message Model
    ${exp_message_model} =    Send Text Message    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Iis Message    ${user_id}    ${exp_message_model.message_id}
    ${act_body_message} =    Get Body Message Model From Message Model    ${act_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message}
    Compare Messages    ${exp_message_model}    ${act_message_model}
    Delete Message    ${user_id}    ${exp_message_model.message_id}

Test Import Message
    ${random_body_model} =    Create Random Body Message Model
    ${exp_message_model} =    Import Text Message    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Iis Message    ${user_id}    ${exp_message_model.message_id}
    ${act_body_message} =    Get Body Message Model From Message Model    ${act_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message}
    Delete Message    ${user_id}    ${exp_message_model.message_id}

Test Insert Message With Attach
    [Template]  Test Insert Message With File
    ${txt_file_name}
    ${img_file_name}

Test Send Message With Attach
    [Template]  Test Send Message With File
    ${txt_file_name}
    ${img_file_name}

Test Import Message With Attach
    [Template]  Test Import Message With File
    ${txt_file_name}
    ${img_file_name}

*** Keywords ***
Test Send Message With File
    [Arguments]    ${file_name}
    ${random_body_model} =    Create Random Body Message Model With Attach    ${file_name}
    ${exp_message_model} =    Send Message With Attach    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Iis Message With Attach    ${user_id}    ${exp_message_model.message_id}
    ${act_body_message} =    Get Body Message Model From Message Model    ${act_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message}
    Compare Messages    ${exp_message_model}    ${act_message_model}
    ${exp_size_file}    Get File Size By Name    ${file_name}
    Compare Fields    ${file_name}     ${act_message_model.file_name}
    Compare Fields   ${exp_size_file}    ${act_message_model.file_size}
    Delete Message    ${user_id}    ${exp_message_model.message_id}

Test Insert Message With File
    [Arguments]    ${file_name}
    ${random_body_model} =    Create Random Body Message Model With Attach    ${file_name}
    ${exp_message_model} =    Insert Message With Attach    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Iis Message With Attach    ${user_id}    ${exp_message_model.message_id}
    ${act_body_message} =    Get Body Message Model From Message Model    ${act_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message}
    Compare Messages    ${exp_message_model}    ${act_message_model}
    ${exp_size_file}    Get File Size By Name    ${file_name}
    Compare Fields    ${file_name}     ${act_message_model.file_name}
    Compare Fields   ${exp_size_file}    ${act_message_model.file_size}
    Delete Message    ${user_id}    ${exp_message_model.message_id}

Test Import Message With File
    [Arguments]    ${file_name}
    ${random_body_model} =    Create Random Body Message Model With Attach    ${file_name}
    ${exp_message_model} =    Import Message With Attachment    ${user_id}    ${random_body_model}
    ${act_message_model} =    Get Iis Message With Attach    ${user_id}    ${exp_message_model.message_id}
    ${act_body_message} =    Get Body Message Model From Message Model    ${act_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message}
    ${exp_size_file}    Get File Size By Name    ${file_name}
    Compare Fields    ${file_name}     ${act_message_model.file_name}
    Compare Fields   ${exp_size_file}    ${act_message_model.file_size}
    Delete Message    ${user_id}    ${exp_message_model.message_id}
