*** Settings ***
Documentation    This Suite tests the ACL service
Library  ../steps/AclStep.py


*** Variables ***
# all cases
${scope_value}    testg@gmail.com

# insert
${role}           reader
${scope_type}     user

# update data
${role_update}           writer
${scope_type_update}     user

# patch data
${role_patch}           owner
${scope_type_patch}     user

*** Test Cases ***
ACL rule life cycle test
   # Insert acl rule
   ${scope_value}    Create Random Scope Value
   ${expected_acl_model}    Insert Acl Rule    role=${role}
   ...                                         scope_value=${scope_value}
   ...                                         scope_type=${scope_type}
   ${actual_acl_model}    Get Acl Rule    scope_value=${scope_value}
   Check models are equal    ${expected_acl_model}    ${actual_acl_model}

   # Update acl rule
   ${expected_acl_model}    Update Acl Rule    role=${role_update}
   ...                                         scope_value=${scope_value}
   ...                                         scope_type=${scope_type_update}
   ${actual_acl_model}    Get Acl Rule    scope_value=${scope_value}
   Check models are equal    ${expected_acl_model}    ${actual_acl_model}

   # Get acl rules list
   ${actual_acl_models_array}    List Acl Rule
   Check Model In List    list_rules=${actual_acl_models_array}
   ...                    validate_rule=${expected_acl_model}

   # Patch acl rule
   ${expected_acl_model}    Patch Acl Rule    role=${role_patch}
   ...                                        scope_value=${scope_value}
   ...                                        scope_type=${scope_type_patch}

   ${actual_acl_model}    Get Acl Rule    scope_value=${scope_value}
   Check models are equal    ${expected_acl_model}    ${actual_acl_model}

   # Delete acl rule
   Delete acl rule    ${scope_value}
   ${actual_acl_models_array}    List Acl Rule
   Check that rule was deleted    list_rules=${actual_acl_models_array}
   ...                            validate_rule=${expected_acl_model}