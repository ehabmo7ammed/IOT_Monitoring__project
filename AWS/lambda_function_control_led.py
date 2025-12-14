import json
import boto3

# IoT Data client
iot_client = boto3.client(
    'iot-data',
    region_name='us-east-2',
    endpoint_url='https://a16yla8r2d4dg4-ats.iot.us-east-2.amazonaws.com'
)

# SNS client
sns_client = boto3.client('sns', region_name='us-east-2')

# ARN لتوبك الـ SNS
SNS_ARN = "arn:aws:sns:us-east-2:635753876167:E_to_email"

def lambda_handler(event, context):

    print("Received event:", event)

    # قراءة البيانات من IoT Rule
    device_id = event.get("deviceId")
    temp = float(event.get("temp", 0))

    # تحديد حالة LED
    led_state = "on" if temp > 30 else "off"

    # نشر الرسالة إلى MQTT للتحكم بالـ LED
    topic = f"control_led/{device_id}"
    payload = {
        "deviceId": device_id,
        "led": led_state,
        "timestamp": event.get("timestamp")
    }

    iot_client.publish(
        topic=topic,
        qos=0,
        payload=json.dumps(payload)
    )

    # إذا كانت درجة الحرارة أعلى من 30 أرسل رسالة بريد إلكتروني عبر SNS
    if temp > 30:
        message = f"Warning: The temperature from.{device_id}  too high: {temp}°C"
        sns_client.publish(
            TopicArn=SNS_ARN,
            Message=message,
            Subject="Warning temperature"
        )

    return {
        "status": "OK",
        "led_state_sent": payload,
        "sns_sent": temp > 30
    }
