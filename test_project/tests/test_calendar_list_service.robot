*** Settings ***
Documentation  Google Calendar API: Calendars list test
Library    ../steps/CalendarListSteps.py
Library    ../steps/CalendarsSteps.py
Variables  ../configurations/test_data.py

*** Test Cases ***
Insert Calendar List Test
    ${calendar_list_model} =    Create Random Calendar List Model    ${calendar_id}
    ${insert_cal_list_response}  ${insert_cal_list_model} =    Insert Calendar List    ${calendar_list_model}
    ${get_cal_list_model} =     Get Calendar List    ${calendar_id}
    Check Model    ${calendar_list_model}
    ...            ${get_cal_list_model}

Patch Calendar List Test
    ${calendar_list_model} =    Create Random Calendar List Model    ${calendar_id}
    ${patch_cal_list_response}   ${patch_cal_list_model} =   Patch Calendar List    ${calendar_list_model}
    ${get_cal_list_model} =     Get Calendar List    ${calendar_id}
    Check Model    ${calendar_list_model}
    ...            ${get_cal_list_model}

Update Calendar List Test
    ${calendar_list_model} =    Create Random Calendar List Model    ${calendar_id}
    ${update_cal_list_response}  ${update_cal_list_model} =    Update Calendar List    ${calendar_list_model}
    ${get_cal_list_model} =     Get Calendar List    ${calendar_id}
    Check Model    ${calendar_list_model}
    ...            ${get_cal_list_model}

List Calendar List Test
    ${calendar_list_model} =    Create Random Calendar List Model    ${calendar_id}
    ${insert_cal_list_response}  ${insert_cal_list_model} =    Insert Calendar List    ${calendar_list_model}
    ${list_cal_list_response}    ${list_cal_list_model} =      List Calendar List
    Check Model In The List Models    ${list_cal_list_model}
    ...                               ${insert_cal_list_model}

Delete Calendar List Test
    Delete Calendar List    ${calendar_id}
    ${list_cal_list_response}    ${list_cal_list_model} =      List Calendar List
    Check Delete Calendar List In List    ${list_cal_list_model}
    ...                                   ${calendar_id}
