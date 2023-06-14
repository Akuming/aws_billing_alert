import boto3
import os
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ce = boto3.client('ce')

    end = datetime.today().date().strftime('%Y-%m-%d')
    start_month = datetime.today().date().replace(day=1).strftime('%Y-%m-%d')
    start_day = (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
    
    print("The start date is ", start_month)
    print("The end date is ", end)

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_month,
            'End': end
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    print(response)

    daily_cost = sum(float(res['Metrics']['UnblendedCost']['Amount']) for res in response['ResultsByTime'][-1]['Groups'])
    print("The daily cost is ", daily_cost)
    monthly_cost = sum(float(res['Metrics']['UnblendedCost']['Amount']) for day in response['ResultsByTime'] for res in day['Groups'])
    print("The monthly cost is ", monthly_cost)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'daily_cost': daily_cost,
            'monthly_cost': monthly_cost
        })
    }