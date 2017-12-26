*** Settings ***
Documentation    Test FreeBusy service in the google calendar api
Library  ../steps/FreeBusyStep.py

*** Variables ***
${time_min}     2017-04-26T00:00:01+00:00
${time_max}     2017-04-26T20:00:01+00:00
${time_zone}    UTC


*** Test Cases ***
Test FreeBusy Sevice
    Query Freebusy    time_min=${time_min}
    ...               time_max=${time_max}
    ...               time_zone=${time_zone}