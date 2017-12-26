*** Settings ***
Documentation  Google Calendar API: Calendars test
...
Library  ../steps/CalendarsSteps.py


*** Test Cases ***
Calendar insert
    ${calendar_model_initial}=    create calendar model initial
    ${calendar_model_response}=    create calendar    ${calendar_model_initial}
    set global variable    ${calendar_model_response}
    set global variable    ${calendar_model_initial}

Calendar get
    Compare Calendar with initial model  ${calendar_model_initial}

    ${calendar_model_actual}=    get calendar    ${calendar_model_response}
    compare models calendar    ${calendar_model_initial}    ${calendar_model_actual}

Calendar update
    ${calendar_model_initial_update}=    create calendar model initial
    update calendar by put    ${calendar_model_response}    ${calendar_model_initial_update}
    set global variable    ${calendar_model_initial_update}

Calendar get
    Compare Calendar with initial model    ${calendar_model_initial_update}

Calendar patch
    ${calendar_model_initial_patch}=    create calendar model initial
    update calendar by patch    ${calendar_model_response}    ${calendar_model_initial_patch}
    set global variable    ${calendar_model_initial_patch}

Calendar get
    Compare Calendar with initial model    ${calendar_model_initial_patch}

Calendar clear
    clear primary calendar

Calendar delete
    delete calendar    ${calendar_model_response.id}

Calendar full test
    ${calendar_model_response_insert}=    calendar insert
    calendar update    ${calendar_model_response_insert}
    calendar patch    ${calendar_model_response_insert}
    clear primary calendar
    delete calendar    ${calendar_model_response_insert.id}

*** Keywords ***
Compare Calendar with initial model
    [Arguments]     ${initial_model}
    ${calendar_model_actual}=    get calendar    ${calendar_model_response}
    compare models calendar    ${initial_model}    ${calendar_model_actual}