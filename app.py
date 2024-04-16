#!/usr/bin/env python3
from aws_cdk import App, Aspects
from cdk_nag import AwsSolutionsChecks

from src.amplify_add_on_stack import CustomAmplifyDistributionStack
from src.web_acl_stack import CustomWebAclStack

app = App()

CustomWebAclStack(
    app,
    "CustomWebAclStackDev", # change it to a different name in case you want to deploy to a different environment
    description="This stack creates WebACL to be attached to a CloudFront distribution \
        for a Web App hosted with Amplify",
    env={"region": "us-east-1"},
)
CustomAmplifyDistributionStack(
    app,
    "CustomAmplifyDistributionStackDev", # change it to a different name in case you want to deploy to a different environment
    description="This stack creates a custom CloudFront distribution pointing to \
        Amplify app's default CloudFront distribution. \
        It also enables Basic Auth protection on specified branch. \
        Creates event based setup for invalidating custom CloudFront distribution when \
        a new version of Amplify App is deployed.",
    web_acl_arn=app.node.try_get_context("web_acl_arn"),
    app_id=app.node.try_get_context("app_id"),
    branch_name=app.node.try_get_context("branch_name"),
)

Aspects.of(app).add(AwsSolutionsChecks())
app.synth()
