# Auto Log Sender via AWS Lambda

This project contains AWS CloudFormation templates to deploy an AWS Lambda function that runs a specified CloudWatch Logs Insights query and sends the results via email periodically.

## Author

- Gunay Geyik

## License

- MIT License

## Templates

There are two versions of the CloudFormation template:

1. **Inline Lambda Function (`auto_log_sender_inline.yml`)**: Contains the Lambda function code directly within the template.
2. **Lambda Function from a ZIP File (`auto_log_sender_zip.yml`)**: References a ZIP file in an S3 bucket for the Lambda function code. (Note: This version is not tested.)

## Usage

### Mandatory Parameters

- `EmailAddress`: The email address to which the query results will be sent. Make sure that email address is verified in Amazon SES!
- `LogGroupNames`: Comma-separated names of the log groups to query.

### Optional Parameters

- `QueryString`: The CloudWatch Logs Insights query to run. Default is a query for errors.
- `DaysInterval`: The interval in days to query and how often the function runs. Default is 7 days.
- `TimeToWaitForQueryCompletion`: Time in seconds to wait for the query to complete. Default is 60 seconds. Note that the timeout is set to 180 seconds so anything higher or closer will cause issues unless you update it as well.

## Deployment

To deploy the template, use the AWS CLI. For example, to deploy the inline version, first upload the inline yml file and run:

```sh
aws cloudformation create-stack --stack-name ErrorSender --template-body file://auto_log_sender_deployer_inline.yml --capabilities CAPABILITY_IAM --parameters '[{"ParameterKey":"EmailAddress","ParameterValue":"example@eaxmple.com"},{"ParameterKey":"LogGroupNames","ParameterValue":"/aws/lambda/log1,/aws/lambda/log2"}]'
```
## Final Notes

- Replace placeholders like `<YOUR_S3_BUCKET_NAME>`, `<YOUR_ZIP_FILE_NAME>` with your actual information.
- For the ZIP file version, ensure the ZIP file is uploaded to an S3 bucket and the template is updated accordingly before deployment.

## TODO:

- Improve the IAM permissions and make them more granular.
- Support for multiple email addresses.


