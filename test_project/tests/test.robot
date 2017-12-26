*** Settings ***
Documentation  Google Calendar API: Calendars list test
Library    ../steps/CalendarListSteps.py
Library    ../steps/CalendarsSteps.py
Variables    ../configurations/test_data.py

*** Test Cases ***
Life Cycle Calendar List
    ${calendar_list_model} =    Create Random Calendar List Model    ${calendar_id}
    ${list_cal_list_response}    ${list_cal_list_model} =      List Calendar List

