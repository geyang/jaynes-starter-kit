export QUERY='Quotas[*].{Adjustable:Adjustable,Name:QuotaName,Value:Value,Code:QuotaCode}'
for region in us-west-2 us-west-1 us-east-2 us-east-1 sa-east-1 eu-west-1 eu-central-1 ap-southeast-2 ap-southeast-1 ap-south-1 ap-northeast-2 ap-northeast-1
do
echo region $region \| >> spot_limit.md
aws service-quotas list-service-quotas --query $QUERY --service-code ec2 --output table --region $region | grep 'P Spot' >> spot_limit.md
done