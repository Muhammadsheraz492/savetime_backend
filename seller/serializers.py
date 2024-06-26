from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import serializers
from .models import Device, User,Otp
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import boto3
from django.conf import settings
from datetime import datetime
from botocore.exceptions import ClientError
from user_agents import parse
from rest_framework.exceptions import ValidationError
from .custom_exceptions import CustomValidationError  # Import the custom exception
import random


def send_verification_email(recipient_email, otp):
    # Create the HTML content with dynamic values
    html_content = '''
    <tr>
        <td>
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tbody>
                    <tr>
                        <td align="center" style="padding:40px 40px 0px 40px">
                            <a href="https://github.com/Muhammadsheraz492" target="_blank" style="text-decoration:none;">
                                <span style="
                                    color: #333; 
                                    padding: 10px 20px; 
                                    border-radius: 5px; 
                                    font-weight: bold; 
                                    font-family: Arial, sans-serif;
                                    text-align: center; 
                                    display: inline-block; 
                                ">Save Time</span>
                            </a>
                        </td>
                    </tr>
                    <tr>
                        <td align="center" style="font-size:24px;color:#0e0e0f;font-weight:700;font-family:Helvetica Neue, Arial, sans-serif;line-height:28px;vertical-align:top;text-align:center;padding:35px 40px 0px 40px">
                            <strong>Welcome to SaveTime</strong>
                        </td>
                    </tr>
                    <tr>
                        <td style="font-size:16px;line-height:22px;font-family:Helvetica Neue, Arial, sans-serif;text-align:left;color:#555555;padding:40px 40px 0 40px">
                            <img src="https://www.google-analytics.com/collect?v=1&tid=UA-12078752-14&cid=8212e561-1ec6-4296-800d-ea35cc4f4627&uid=0&t=event&ec=email_open&ea=earnings_csv_created" alt="Tracking Image" style="display:none;">
                            <div>
                                Dear SaveTime User,
                            </div>
                            <br>
                            <div>
                               We received a request to access your Google Account <a href="mailto:{0}" target="_blank">{0}</a> through your email address. Your Save Time verification code is:
                                <br><br>
                                <strong style="text-align:center;font-size:24px;font-weight:bold">{1}</strong>
                            </div>
                            <br>
                            Thanks,<br>The Save Time Team
                        </td>
                    </tr>
                </tbody>
            </table>
        </td>
    </tr>
    '''.format(recipient_email, otp)

    # Create the email message
    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Save Time Verification Code"
    # message["From"] = sender_email
    # message["To"] = recipient_email

    # Attach the HTML content to the email
    # part = MIMEText(html_content, "html")
    # message.attach(part)

    # Send the email
    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Save Time Verification Code"
    # message["From"] = sender_email
    # message["To"] = recipient_email

    # # Attach the HTML content to the email
    # part = MIMEText(html_content, "html")
    # message.attach(part)

    try:
        import smtplib

        # sender_email = "qasim5ali99@gmail.com"
        # rec_email = "tocybernatesolution@gmail.com"
        # password = "zhzu irtp oqja zfkx"
        # message = "Hey, this was sent using python"
        sender_email = "tocybernatesolution@gmail.com"
        password = "rukb ikjx zqbp fvjh"
        # smtp_server = 'smtp.gmail.com'
        # smtp_port = 587
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, password)  # Login to the email server
        print("Login Success")

        server.sendmail(sender_email, recipient_email, otp)
        print("Email has been sent to", recipient_email)

        # Close the connection to the SMTP server
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
# send_verification_email("tocybernatesolution@gmail.com","1223123")
def get_random_five_digit_number():
    return random.randint(10000, 99999)
# def upload_to(instance, filename):
    # print('images/{filename}'.format(filename=filename))
    # return 'images/{filename}'.format(filename=filename)
class DeviceSerializer(serializers.ModelSerializer):
    random_access_point=serializers.CharField(required=True)
    device_name=serializers.CharField(required=True)
    ip=serializers.CharField(required=True)
    class Meta:
        model = Device
        fields = ['random_access_point', 'device_name', 'ip']

class SellerSerializer(serializers.ModelSerializer):
    devices=[]
    email=serializers.EmailField(required=True)
    username=serializers.CharField(required=True)
    firstname=serializers.CharField(required=True)
    lastname=serializers.CharField(required=True)
     
    # devices = DeviceSerializer(many=True, read_only=True)  # Assuming you want to display related devices

    
    profile_image = serializers.ImageField(max_length=None, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password', 'profile_image']
    
    def create(self, validated_data):
        # devices_data = validated_data.pop('devices', [])
        password = validated_data.pop('password')
        validated_data['password']=make_password(password=password)
        profile_image = validated_data.get('profile_image')
        if profile_image:
            
            profile_image = validated_data.pop('profile_image')
            try:
                print(settings.AWS_STORAGE_BUCKET_NAME)
                s3 = boto3.client(
                    's3',
                    aws_access_key_id='AKIA2UC27FQCXBZKOAUO',
                    aws_secret_access_key='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',
                    region_name='eu-north-1'
                )
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_key = f"profile_images/{timestamp}_{profile_image.name}".replace(" ","")
                s3.upload_fileobj(profile_image, 'wishtun', image_key)
                s3_url = f"https://wishtun.s3.amazonaws.com/{image_key}"
                validated_data['profile_image'] = s3_url

            except ClientError as e:
                print(f"Error uploading profile image to S3: {e}")
                raise serializers.ValidationError("Failed to upload profile image")
        try:
            with transaction.atomic():  # Ensure atomicity
                user = User.objects.create(**validated_data)
                test_otp=get_random_five_digit_number()
                data={
                    "otp":test_otp
                }
                
                Otp.objects.create(user=user,**data)
                send_verification_email(validated_data['email'],str(test_otp))
                # server.sendmail(sender_email, , test_otp)
                
                for device_data in self.devices:
                    Device.objects.create(user=user, **device_data)
                
                return user
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                raise serializers.ValidationError("Email address already exists.")
            else:
                raise serializers.ValidationError("An unexpected error occurred.")
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email already exists")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("Username already exists")
        return value
    def validate_firstname(self,value):
        if value is None:
            raise serializers.ValidationError("fistname are required")
        return value
    def validate_lastname(self,value):
        if value is None:
            raise serializers.ValidationError("lastname are required")
        return value
    def validate(self, attrs):
        request = self.context.get('request')
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        
        device_info = {
            'random_access_point': user_agent_str,
            'device_name': user_agent.device.family,
            'action':'register',
            'ip': request.META.get('REMOTE_ADDR', '')
        }
        self.devices.append(device_info)
        
        return super().validate(attrs)
    def to_representation(self, instance):
        data=super().to_representation(instance=instance)
        if instance.profile_image:
            data['profile_image']=instance.profile_image
        return data
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User  # Specify your custom user model here
        fields = ["email", "password"]

    def validate_email(self, value):
        print("This is mine")
        if not value:
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Email field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            error_data = {
                'success': False,
                "message":"This email does not exist."
            }
            raise CustomValidationError(detail=error_data)
    def run_validation(self, data):
        if 'email' in data and not data['email'].strip():
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Email field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        if 'password' in data and not data['password'].strip():
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Password field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        return super().run_validation(data)
    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     try:
    #         user = User.objects.get(email=email)
    #         return user
    #     except User.DoesNotExist:
    #         error_data = {
    #             'success': False,
    #             'error_message': {
    #                   "type": "ValidationError",
    #                   "message":"This email does not exist."
                
    #             },
    #         }
    #         print(error_data)
    #         raise CustomValidationError(detail=error_data)
    #     return attrs
    