import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('E_temp_esp32')
def lambda_handler(event, context):
    try:
        path = event.get('path', '/')

        # إزالة Stage name إذا موجود
        if path.startswith("/E_stage_API"):
            path = path[len("/E_stage_API"):]

        method = event.get('httpMethod', 'GET')
        query_params = event.get('queryStringParameters') or {}

        print(f"Path: {path}, Method: {method}, Params: {query_params}")

        if path == '/latest' and method == 'GET':
            return get_latest_reading(query_params)
        elif path == '/history' and method == 'GET':
            return get_historical_data(query_params)
        elif path == '/status' and method == 'GET':  # ← تأكد إذا تريد stats أم status
            return get_statistics(query_params)
        else:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({'error': 'Not found'})
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }


def get_cors_headers():
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }

# -------------------------------------------------------
# GET /latest
# -------------------------------------------------------
def get_latest_reading(params):
    device_id = params.get('deviceId', '1')

    response = table.query(
        KeyConditionExpression=Key('deviceId').eq(device_id),
        ScanIndexForward=False,
        Limit=1
    )

    items = response.get('Items', [])
    if not items:
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'No data found'})
        }

    item = items[0]

    temperature = float(item.get('temp', 0))
    humidity = float(item.get('humidity', 0))

    # timestamp is already milliseconds
    timestamp_ms = int(item['timestamp'])

    # Convert ms → ISO string
    timestamp_iso = datetime.utcfromtimestamp(timestamp_ms / 1000).isoformat() + "Z"

    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'deviceId': device_id,
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp_iso,
            'timestamp_ms': timestamp_ms
        }, cls=DecimalEncoder)
    }

# -------------------------------------------------------
# GET /history?hours=24
# -------------------------------------------------------
def get_historical_data(params):
    device_id = params.get('deviceId', '1')
    hours = int(params.get('hours', '24'))

    now_ms = int(datetime.utcnow().timestamp() * 1000)
    start_ms = now_ms - (hours * 3600 * 1000)

    response = table.query(
        KeyConditionExpression=Key('deviceId').eq(device_id) &
                              Key('timestamp').between(str(start_ms), str(now_ms)),
        ScanIndexForward=True
    )

    items = response.get('Items', [])
    formatted_data = []

    for item in items:
        timestamp_ms = int(item['timestamp'])

        formatted_data.append({
            'timestamp': timestamp_ms,
            'temperature': float(item.get('temp', 0)),
            'humidity': float(item.get('humidity', 0))
        })

    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'deviceId': device_id,
            'count': len(formatted_data),
            'data': formatted_data,
            'start_ms': start_ms,
            'end_ms': now_ms
        }, cls=DecimalEncoder)
    }

# -------------------------------------------------------
# GET /stats?hours=24
# -------------------------------------------------------
def get_statistics(params):
    device_id = params.get('deviceId', '1')
    hours = int(params.get('hours', '24'))

    now_ms = int(datetime.utcnow().timestamp() * 1000)
    start_ms = now_ms - (hours * 3600 * 1000)

    response = table.query(
        KeyConditionExpression=Key('deviceId').eq(device_id) &
                              Key('timestamp').between(str(start_ms), str(now_ms))
    )

    items = response.get('Items', [])

    if not items:
        return {
            'statusCode': 404,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'No data found'})
        }

    temperatures = [float(i.get('temp', 0)) for i in items]
    humidities = [float(i.get('humidity', 0)) for i in items]

    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'deviceId': device_id,
            'period_hours': hours,
            'temperature': {
                'min': min(temperatures),
                'max': max(temperatures),
                'avg': sum(temperatures) / len(temperatures),
                'current': temperatures[-1]
            },
            'humidity': {
                'min': min(humidities),
                'max': max(humidities),
                'avg': sum(humidities) / len(humidities),
                'current': humidities[-1]
            },
            'dataPoints': len(items)
        }, cls=DecimalEncoder)
    }
