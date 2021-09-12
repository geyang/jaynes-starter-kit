.EXPORT_ALL_VARIABLES:
#AWS_PROFILE=$$ORGANIZAION
#AWS_PAGER=""
ORGANIZATION=improbable
ROLE_NAME=${USER}-jaynes-worker-role
POLICY_NAME=TagAndTermination
INSTANCE_PROFILE=${USER}-jaynes-worker-profile
INSTANCE_TAGS=Key=Jaynes,Value=Worker

create_gce_bucket:
	gsutil mb gs://$$USER-jaynes-$$ORGANIZATION
	gsutil mb gs://$$USER-data-$$ORGANIZATION
remove_gce_bucket:
	gsutil rb gs://$$USER-jaynes-$$ORGANIZATION
	gsutil rb gs://$$USER-data-$$ORGANIZATION