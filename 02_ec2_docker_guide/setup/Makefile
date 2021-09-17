.EXPORT_ALL_VARIABLES:
AWS_PROFILE=ttic-bstadie
#AWS_PROFILE=improbable
#AWS_PAGER=""
ROLE_NAME=${USER}-jaynes-worker-role
POLICY_NAME=TagAndTermination
INSTANCE_PROFILE=${USER}-jaynes-worker-profile
INSTANCE_TAGS=Key=Jaynes,Value=Worker

list_instance_profiles:
	aws iam list-instance-profiles --output yaml >> private.yml
	cat private.yml
create_s3_bucket:
	aws s3api create-bucket --acl public-read-write --bucket $$USER-jaynes-improbable --region us-east-1
	aws s3api create-bucket --acl public-read-write --bucket $$USER-data-improbable --region us-east-1
remove_s3_bucket:
	aws s3api delete-bucket --bucket $$USER-jaynes-improbable
	aws s3api delete-bucket --bucket $$USER-data-improbable
create_iam_role:
	aws iam create-role --role-name $$ROLE_NAME --assume-role-policy-document file://role-policy.json
	aws iam attach-role-policy --role-name $$ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
	aws iam attach-role-policy --role-name $$ROLE_NAME --policy-arn arn:aws:iam::aws:policy/ResourceGroupsandTagEditorFullAccess
	aws iam put-role-policy --role-name $$ROLE_NAME --policy-name $$POLICY_NAME --policy-document file://additional-policies.json
create_instance_profile:
	aws iam create-instance-profile --instance-profile-name $$INSTANCE_PROFILE --tags=$$INSTANCE_TAGS
	aws iam add-role-to-instance-profile --instance-profile-name $$INSTANCE_PROFILE --role-name $$ROLE_NAME
list_iam_role_policies:
	aws iam list-attached-role-policies --role-name $$ROLE_NAME
clean_iam_roles:
	aws iam remove-role-from-instance-profile --instance-profile-name $$INSTANCE_PROFILE --role-name $$ROLE_NAME
	aws iam delete-instance-profile --instance-profile-name $$INSTANCE_PROFILE
	aws iam detach-role-policy --role-name $$ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
	aws iam detach-role-policy --role-name $$ROLE_NAME --policy-arn arn:aws:iam::aws:policy/ResourceGroupsandTagEditorFullAccess
	aws iam delete-role-policy --role-name $$ROLE_NAME --policy-name $$POLICY_NAME
	aws iam delete-role --role-name $$ROLE_NAME
create_security_group:
	echo "create security group"
create_key_pairs:
	yes | python setup_aws.py