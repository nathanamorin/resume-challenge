import os
from attr import Attribute
from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_certificatemanager as certificatemanager
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as aws_lambda
from aws_cdk import aws_apigatewayv2 as apigateway
from aws_cdk import aws_apigatewayv2_integrations as apigateway_integration


class InfraStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        table = dynamodb.Table(self, "table", 
            partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.STRING)
        )

        function = aws_lambda.Function(self, "function",
            code=aws_lambda.Code.from_asset(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lambda-handler')),
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="index.main",
            environment={
                "TABLE": table.table_name
            }
        )

        table.grant_read_write_data(function)

        api_gateway = apigateway.HttpApi(self, "gateway")

        integration = apigateway_integration.LambdaProxyIntegration(handler=function)

        api_gateway.add_routes(
            path="/count", 
            methods=[apigateway.HttpMethod.GET],
            integration=integration
        )



        bucket = s3.Bucket(self, "resume-static-site", 
                                versioned=True,
                                bucket_name="nathan-morin-static-resume-site"
                        )

        cert = certificatemanager.Certificate.from_certificate_arn(self, "cert",
            f"arn:aws:acm:us-east-1:{self.account}:certificate/9cd00288-9a0f-47e1-96ce-59e45a9d89e0"
        )

        oia = cloudfront.OriginAccessIdentity(self, "access")
        bucket.grant_read(oia)

        cloudfront_dist = cloudfront.Distribution(self, "cloudfront",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket=bucket, origin_access_identity=oia),
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=["resume.nathanmorin.com"],
            certificate=cert,
            default_root_object="index.html",
            additional_behaviors={
                "/count": cloudfront.BehaviorOptions(
                    origin=origins.HttpOrigin(domain_name=api_gateway.url.replace("https://", "").strip("/")),
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    cache_policy=cloudfront.CachePolicy.CACHING_DISABLED
                )
            }
        )

        core.CfnOutput(self, "resume-cloudfront", 
                        export_name="resume-cloudfront", 
                        value=cloudfront_dist.distribution_id
                    )





