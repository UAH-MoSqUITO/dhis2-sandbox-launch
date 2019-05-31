#!/bin/bash
set -eu

for missing_environment_variable in KeyName ImageId
do
  : ${!missing_environment_variable:?$missing_environment_variable}
done

(
    set -x
    aws cloudformation create-stack \
        --stack-name dhis2-sandbox \
        --template-body "$(python3 assembletemplate.py | jq -S -c .)" \
        --parameters \
            ParameterKey=KeyName,ParameterValue="$KeyName" \
            ParameterKey=ImageId,ParameterValue="$ImageId"
)
