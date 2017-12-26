*** Settings ***
Documentation    C1362: Create, get, list, delete from settingsFilters
...   https://testrail.a1qa.com/index.php?/cases/view/1362&group_by=cases:section_id&group_id=1295&group_order=asc
Library    ../steps/SettingsFiltersSteps.py
Library    ../steps/LabelsSteps.py


*** Variables ***
${user_id}          qacalendarapi@gmail.com


*** Test Cases ***
Test Settings Filters Service
    ${random_label_model} =    Create Random Label Model
    ${response_label_model} =    Create Label    ${user_id}    ${random_label_model}
    ${random_filter_model} =    Create Filters Model    ${response_label_model.label_id}
    ${response_create_filter_model} =    Create Filters    ${user_id}    ${random_filter_model}

    ${response_get_filter_model} =    Get Filters    ${user_id}    ${response_create_filter_model.filter_id}
    Check Model    ${random_filter_model}    ${response_get_filter_model}

    ${list_filters_models} =    List Filters    ${user_id}
    Check Model Is The List Models    ${list_filters_models}    ${random_filter_model}

    Delete Filters    ${user_id}    ${response_create_filter_model.filter_id}
    ${list_filters_models1} =    List Filters    ${user_id}
    Check Model Is Not The List Models    ${list_filters_models1}    ${random_filter_model}
    Delete Label    ${user_id}    ${response_label_model.label_id}
