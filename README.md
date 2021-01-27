# Intersight Alarm Monitor Example
AWS Lambda based Python 3.8 script to check Intersight for alarms generated within the past 15 minutes and post to a Webex Teams room.

Instructions:
1. Replace contents of SecretKey.txt with Interight API Private Key
2. Replace contents of .env with Intersight API Key, Webex Room ID, Webex Bot Token
3. Create AWS Lambda package from root of project directory:

        sudo pip3 install --target ./package cryptography requests python-dotenv

        cd package/

        zip -r ../my-deployment-package.zip .

        cd ..

        zip -g my-deployment-package.zip *.py

        zip -g my-deployment-package.zip *.txt

        zip -g my-deployment-package.zip *.env

4. Create AWS Lambda Function using Python 3.8
5. Upload my-deployment-package.zip to Lambda Function
6. Set timeout to 8 seconds on AWS Lambda Function
7. Create AWS Event Bridge to run Lambda Function at a fixed interval every 15 minutes

“Copyright (c) 2020 Cisco Systems, Inc. and/or its affiliates”
