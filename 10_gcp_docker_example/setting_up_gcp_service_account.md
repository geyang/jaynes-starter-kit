# Setting up GCP Service Account

In order for docker to access the Google storage bucket (GS), it needs the credentials of a service account for reading from and writing to the bucket. Note that this is **within** the docker instance.

1. Setting up the service account:

	```bash
	gcloud iam service-accounts create $USER-improbable-gs-service \
	  --description="GS Service Account for improbable-ai" \
	  --display-name="gs-service"
	```

2. Granting the service account read and write access to the bucket

	```bash
	gsutil iam ch serviceAccount:$USER-improbable-gs-service@improbable-ai-4682.iam.gserviceaccount.com:roles/storage.objectAdmin gs://geyang-jaynes-improbable-a
	```

	The detailed API docs can be found here [[gsutil iam ch]](https://cloud.google.com/storage/docs/gsutil/commands/iam).

	To grant write access, use `storage.objectAdmin`. For read-only access, use `storage.objectViewer`. For detailed description over the available roles, refer to [[access-control/iam]](https://cloud.google.com/storage/docs/access-control/iam).

3. Setting up and downloading the json key file

   ```bash
   gcloud iam service-accounts keys create ~/.gce/$USER-improbable-gs-service.json \
       --iam-account=$USER-improbable-gs-service@improbable-ai-4682.iam.gserviceaccount.com
   ```

## Common Errors

### Service Account Does Not Exist

sometimes you see: 

```bash
BadRequestException: 400 Service account ge-improbable-gs-service@improbable-ai-4682.iam.gserviceaccount.com does not exist.
```

This means that you have created the service account in step 1 using a different GCP project. To correct this, you need to first delete the account you just created, fix your `gcloud` account setup, and then repeat the steps above.

1. Deleting the service account

   ```bash
   gcloud iam service-accounts delete ge-improbable-gs-service@sacred-vault-327317.iam.gserviceaccount.com
   ```

   Detailed API docs are here [[service-accounts/delete]](https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts/delete).

2. Setting Up Your `gcloud` configuration

   Follow the instructions here: 

   ```bash
   $ gcloud config configurations create config-name
   Created [demo-config].
   Activated [demo-config].
   
   $ gcloud config set project my-project-id
   Updated property [core/project].
   
   $ gcloud config set account my-account@example.com
   Updated property [core/account].
   ```

   