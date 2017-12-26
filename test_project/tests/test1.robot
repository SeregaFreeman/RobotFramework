*** Settings ***
Documentation  Suite description
Library  ../steps/ColorSteps.py


*** Test Cases ***
Test colors service
    ${exp_color_model}    Get Colors Model From File
    ${status}    ${act_color_model}    Get Color From Api
    Compare Colors    ${exp_color_model}    ${act_color_model}