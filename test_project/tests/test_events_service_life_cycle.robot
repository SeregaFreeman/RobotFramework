*** Settings ***
Library  ../steps/EventsSteps.py

*** Test Cases ***
Events Test

    ${calendar}  create random calendar
    ${exp_event_model}  create random event
    ${insert_calendar_response}  ${insert_calendar_model}  insert calendar  ${calendar}
    ${insert_event_response}  ${insert_event_model}  insert event  ${insert_calendar_model.id}  ${exp_event_model}
    ${get_event_response}  ${act_event_model}  get event  ${insert_calendar_model.id}  ${insert_event_model.id}
    compare events  ${exp_event_model}  ${act_event_model}

    ${exp_event_model1}  create random event
    ${patch_event_response}  ${patch_event_model}  patch event  ${insert_calendar_model.id}  ${insert_event_model.id}  ${exp_event_model1}
    ${get_event_response1}  ${act_event_model1}  get event  ${insert_calendar_model.id}  ${patch_event_model.id}
    compare events  ${exp_event_model1}  ${act_event_model1}

    ${exp_event_model2}  create random event
    ${update_event_response}  ${update_event_model}  update event  ${insert_calendar_model.id}  ${insert_event_model.id}  ${exp_event_model2}
    ${get_event_response2}  ${act_event_model2}  get event  ${insert_calendar_model.id}  ${update_event_model.id}
    compare events  ${exp_event_model2}  ${act_event_model2}

    ${target_calendar}  create random calendar
    ${insert_target_calendar_response}  ${insert_target_calendar_model}  insert calendar  ${target_calendar}
    ${move_event_response}  ${move_event_model}  move event  ${insert_calendar_model.id}  ${act_event_model2.id}  ${insert_target_calendar_model.id}
    ${get_event_response3}  ${act_event_model3}  get event  ${insert_target_calendar_model.id}  ${insert_event_model.id}
    compare events  ${act_event_model2}  ${act_event_model3}

    ${calendar}  create random calendar
    ${insert_calendar_response}  ${insert_calendar_model}  insert calendar  ${calendar}
    ${event}  create random event
    ${import_event_response}  ${import_event_model}  import recurrent event  ${insert_calendar_model.id}  ${event}
    ${get_event_response}  ${get_event_model}  get event  ${insert_calendar_model.id}  ${import_event_model.id}
    ${result}  instances events  ${insert_calendar_model.id}  ${get_event_model.id}
    compare events  ${event}  ${get_event_model}

    ${summary}  create random summary
    ${quick_add_response}  ${quick_add_model}  quick add event  ${insert_calendar_model.id}  ${summary}
    ${get_event_response4}  ${get_event_model4}  get quick event  ${insert_calendar_model.id}  ${quick_add_model.id}
    compare events  ${quick_add_model}  ${get_event_model4}

    delete event  ${insert_target_calendar_model.id}  ${insert_event_model.id}
    check_that_event_was_deleted  ${insert_target_calendar_model.id}  ${insert_event_model.id}

