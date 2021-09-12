import googleapiclient.discovery
from params_proto.neo_proto import ParamsProto, Proto


class Args(ParamsProto):
    project_id = Proto(env="JYNS_GCE_PROJECT")

compute = googleapiclient.discovery.build('compute', 'v1')
all_zones = compute.zones().list(project=Args.project_id).execute()['items']

print(all_zones)

with open('all_zones.txt', 'w') as f:
    print(*[z['name'] for z in all_zones], sep="\n", file=f)
