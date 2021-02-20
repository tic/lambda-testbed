# Each file in this folder should contain (at least) a function formatted exactly as the
# lambda handler function is in AWS. Consider the following function as an example:

def lambda_function(event, context):
    import requests
    try:
        day = event['params']['query']['day']
    except KeyError:
        day = '2021-01-01'
    return requests.get('https://api.devhub.virginia.edu/v1/facilities/sensors/Rice Hall/Electric Demand/' + day).text
