*** Settings ***
Documentation    C1375: Get and update POP settings, Imap, auto-forwarding, vacation
...   https://testrail.a1qa.com/index.php?/cases/view/1375&group_by=cases:section_id&group_id=1295&group_order=asc
Library  ../steps/GmailSettingsSteps.py


*** Variables ***
${user_id}    qacalendarapi@gmail.com


*** Test Cases ***
Changing and getting POP, IMAP, vacation settings
    ${exp_pop}              Create Pop Model
    ${updated_pop}          Update Pop Model        ${exp_pop}      ${user_id}
    ${actual_pop}           Get Pop Model           ${user_id}
    Compare Models          ${updated_pop}      ${actual_pop}

    ${exp_imap}             Create Imap Model
    ${updated_imap}         Update Imap Model       ${exp_imap}     ${user_id}
    ${actual_imap}          Get Imap Model          ${user_id}
    Compare Models          ${updated_imap}      ${actual_imap}

    ${exp_vacation}         Create Vacation Model
    ${updated_vacation}     Update Vacation Model   ${exp_vacation}     ${user_id}
    ${actual_vacation}      Get Vacation Model          ${user_id}
    Compare Models          ${updated_vacation}      ${actual_vacation}