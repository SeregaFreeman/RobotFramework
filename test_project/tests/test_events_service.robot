*** Settings ***
Library  ../steps/EventsSteps.py
Variables    ../../test_project/configurations/test_data.py

*** Variables ***
${start_date}  2017-05-25T10:41:35
${end_date}  2017-05-30T10:41:35

*** Test Cases ***
Insert Event Test
    ${event}  create random event
    ${insert_event_response}  ${insert_event_model}  insert event  ${calendar_id}  ${event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${insert_event_model.id}
    compare events  ${event}  ${get_event_model}

Move Event Test
    ${event}  create random event
    ${insert_event_response}  ${insert_event_model}  insert event  ${calendar_id}  ${event}
    ${target_calendar}  create random calendar
    ${insert_target_calendar_response}  ${insert_target_calendar_model}  insert calendar  ${target_calendar}
    ${move_event_response}  ${move_event_model}  move event  ${calendar_id}  ${insert_event_model.id}  ${insert_target_calendar_model.id}
    ${get_event_response}  ${get_event_model}  get event  ${insert_target_calendar_model.id}  ${insert_event_model.id}
    compare events  ${event}  ${get_event_model}

Patch Event Test
    ${initial_event}  create random event
    ${insert_initial_event_response}  ${insert_initial_event_model}  insert event  ${calendar_id}  ${initial_event}
    ${new_event}  create random event
    ${patch_event_response}  ${patch_event_model}  patch event  ${calendar_id}  ${insert_initial_event_model.id}  ${new_event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${insert_initial_event_model.id}
    compare events  ${new_event}  ${get_event_model}

Update Event Test
    ${initial_event}  create random event
    ${insert_initial_event_response}  ${insert_initial_event_model}  insert event  ${calendar_id}  ${initial_event}
    ${new_event}  create random event
    ${update_event_response}  ${update_event_model}  update event  ${calendar_id}  ${insert_initial_event_model.id}  ${new_event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${insert_initial_event_model.id}
    compare events  ${new_event}  ${get_event_model}

Quick Add Event Test
    ${summary}  create random summary
    ${quick_add_response}  ${quick_add_model}  quick add event  ${calendar_id}  ${summary}
    ${get_event_response}  ${get_event_model}  get quick event  ${calendar_id}  ${quick_add_model.id}
    compare events  ${quick_add_model}  ${get_event_model}

List Event test
    ${event}  create random event
    ${insert_event_response}  ${insert_event_model}  insert event  ${calendar_id}  ${event}
    delete events by date  ${calendar_id}  ${start_date}  ${end_date}
    ${count_events}  get random digit value  1  3
    ${list_events}  create random list events  ${count_events}  ${start_date}  ${end_date}
    insert list events  ${calendar_id}  ${list_events}
    ${list_events_response}  ${act_list_events}  list events by date  ${calendar_id}  ${start_date}  ${end_date}
    compare list events  ${list_events}  ${act_list_events}

Get Event Test
    ${event}  create random event
    ${insert_event_response}  ${insert_event_model}  insert event  ${calendar_id}  ${event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${insert_event_model.id}
    compare events  ${event}  ${get_event_model}

Delete Event test
    ${event}  create random event
    ${insert_event_response}  ${insert_event_model}  insert event  ${calendar_id}  ${event}
    check that event was deleted  ${calendar_id}  ${insert_event_model.id}

Instances Event Test
    ${event}  create random recurrence event
    ${insert_event_response}  ${insert_event_model}  import recurrent event  ${calendar_id}  ${event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${insert_event_model.id}
    ${result}=   instances events    ${calendar_id}         ${get_event_model.id}
    should be true  ${result}

Import Event Test
    ${event}  create random event
    ${import_event_response}  ${import_event_model}  import recurrent event  ${calendar_id}  ${event}
    ${get_event_response}  ${get_event_model}  get event  ${calendar_id}  ${import_event_model.id}
    compare events  ${event}  ${get_event_model}
