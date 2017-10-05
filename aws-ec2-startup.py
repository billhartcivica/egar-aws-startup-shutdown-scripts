import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g.; 'us-east-1'
region = 'eu-west-2'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
# instances = ['i-0382b18676bd12c22', 'i-065c65021713e3f26', 'i-07bde3bf4e55c5af7']

def lambda_handler(event, context):

	def get_tag_value(tags, key):
		for tag in tags:
			if tag['Key'] == key:
				return tag['Value']
		else:
			raise KeyError

	ec2 = boto3.client('ec2', region_name=region)
	# allInstances = [ i['InstanceId'] for i in ec2.describe_instances()['Reservations']['Instances'] ]
	# allInstances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
	instances = []
	ignored_instances = []
	for reservation in ec2.describe_instances()['Reservations']:
		for instance in reservation['Instances']:
			instance_id = instance['InstanceId']
			try:
				tags = instance['Tags']
				value = get_tag_value(tags, 'project')
				if value == 'egar':
					instances.append(instance_id)
			except KeyError:
				pass
			if instance_id not in instances:
				ignored_instances.append(instance_id)

	if instances:
		ec2.start_instances(InstanceIds=instances)
	print 'ignored instances: ' + str(ignored_instances)
	print 'started your instances: ' + str(instances)