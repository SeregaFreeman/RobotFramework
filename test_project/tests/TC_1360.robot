*** Settings ***
Documentation   C1360: Create an attachemnt to the letter, send, delete
...   https://testrail.a1qa.com/index.php?/cases/view/1360&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/UsersMessagesSteps.py
Library    ../steps/AttachmentsStep.py


*** Variables ***
${user_id}    qacalendarapi@gmail.com
${img_file_name}    img.png
${txt_file_name}    test.txt


*** Test Cases ***
Test Life Cycle Message with attachments
    [Template]  Life Cycle Message With Attachments
    ${img_file_name}
    ${txt_file_name}


*** Keywords ***
Life Cycle Message with attachments
    [Arguments]  ${file_name}
    ${random_body_model} =    Create Random Body Message Model With Attach    ${file_name}
    ${send_message_model} =    Send Message With Attach    ${user_id}    ${random_body_model}
    ${list_message_model} =    Get Messages List    ${user_id}
    Check Message In List    ${list_message_model}    ${user_id}

    ${get_message_model} =    Get Iis Message With Attach    ${user_id}    ${send_message_model.message_id}
    ${act_body_message_model} =    Get Body Message Model From Message Model    ${get_message_model}
    Compare Body Message    ${random_body_model}    ${act_body_message_model}

    ${exp_attachment_model} =    Create Attachment By File Name    ${file_name}
    ${act_attachment_model} =    Get Attachment    ${user_id}    ${get_message_model.message_id}    ${get_message_model.attachment_id}
    Check Attachments Are Equal    ${exp_attachment_model}    ${act_attachment_model}
    Delete Message    ${user_id}    ${send_message_model.message_id}