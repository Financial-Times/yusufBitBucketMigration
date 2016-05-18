# Lambda API service

The test verifies differrent lambda API services

 - config service API test verifies configuration file retrieval from S3 on AWS.
 - versioning API simplifies assigning version to applications either major, minor or patch

Setting up the environment

  - virtualenv -p <pythonBinary> <virtualEnvName>
        
        e.g virtualenv -p /usr/bin/python lambdatest
  - Activate he virtualenv - source lambdatest/bin/activate
  - Install he packages - lambdatest/bin/pip install -r requirements.txt
  
Test Parameters:
 - All tests parameters are stored in parameters.ini including the API key needed
 
#  Running Tests locally:
 - config service test - lettuce features/Config
 - versioning test - lettuce features/Versioning
 
       Additional options: lettuce --with-xunit --xunit-file=testresult.xml features/Config





