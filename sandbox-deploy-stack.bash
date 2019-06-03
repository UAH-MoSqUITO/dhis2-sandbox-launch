#!/bin/bash
set -eu

for missing_environment_variable in KeyName ImageId
do
  : ${!missing_environment_variable:?$missing_environment_variable}
done

stack_name=dhis2-sandbox
template_file=stack.$stack_name.json

python3 sandbox_generate_template.py | jq -S . > "$template_file"

(
    set -x
    aws cloudformation deploy \
        --no-execute-changeset \
        --stack-name "$stack_name" \
        --template-file "$template_file" \
        --parameter-overrides \
            KeyName="$KeyName" \
            ImageId="$ImageId"
)
