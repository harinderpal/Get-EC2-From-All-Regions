import boto3

dynamodbResource = boto3.resource('dynamodb')
def lambda_handler(event, context):
    regions = boto3.session.Session().get_available_regions('ec2')
    accountid = ((context.invoked_function_arn).split(':'))[4]
    for region in regions:
        print(region)
        ec2ListByRegion(region,accountid)
     
    
def ec2ListByRegion(regionName,accountid):
    ec2Resource = boto3.resource('ec2', region_name=regionName)
    instanceList = ec2Resource.instances.all()
    for instance in instanceList:
        
        instanceid = instance.id
        instancetype = instance.instance_type
        for i in instance.tags:
				if(i["Key"]=="Name"):
					print("instance is " + i["Value"])
					instancenaame = i["Value"]
        print("instance id:",instanceid," instance name:",instancenaame, "instance type:",instancetype)
        saveToDynamoDB(instanceid,instancenaame,instancetype,regionName,accountid)
        
def saveToDynamoDB(instanceid,instancenaame,instancetype,regionName,accountid):
    table = dynamodbResource.Table('EC2Information')
    response = table.put_item(
    Item={
              'instanceid':instanceid,
              'instancenaame' :instancenaame,
            	'instancetype' :instancetype,
            	'region' :regionName,
            	'accountid' :accountid
            	})
                        
