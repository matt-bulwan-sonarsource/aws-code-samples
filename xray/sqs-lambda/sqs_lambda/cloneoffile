from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as _sqs,
    aws_lambda as _lambda,
    aws_sns as _sns,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda_event_sources as _lambda_sources,
)
from constructs import Construct
from os import path


class SqsLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_name = "poc-mb-719"

        queue = _sqs.Queue(scope=self, id=f"sqs-{my_name}", queue_name=f"sqs-{my_name}")
        topic = _sns.Topic(scope=self, id=f"sns-{my_name}", topic_name=f"sns-{my_name}")
        lambda_role = _iam.Role(
            self,
            f"temprole-{my_name}",
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            description="All Permissions For My lambdas",
        )
        lambda_role.add_to_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["sqs:*", "sns:*", "events:*", "xray:*"],
                resources=["*"],
            )
        )
        lambda_role.add_managed_policy(
            policy=_iam.ManagedPolicy.from_managed_policy_arn(
                scope=self,
                id="write-cloudwatch-logs",
                managed_policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
            )
        )

        lambda_01 = _lambda.Function(
            scope=self,
            id=f"lambda1-{my_name}",
            code=_lambda.Code.from_asset("src"),
            handler="func_from_crontab_to_sns_sqs.handler",
            function_name="Service01",
            timeout=Duration.seconds(10),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            tracing=_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "DEBUG",
                "EVENT_TARGET": "sqs",
                "SQS_QUEUE": queue.queue_url,
                "SNS_TOPIC": topic.topic_arn,
            },
        )
        lambda_02 = _lambda.Function(
            scope=self,
            id=f"lambda2-{my_name}",
            code=_lambda.Code.from_asset("src"),
            handler="func_from_crontab_to_sns_sqs.handler",
            function_name="Service02",
            timeout=Duration.seconds(10),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            tracing=_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "DEBUG",
                "EVENT_TARGET": "sns",
                "SQS_QUEUE": queue.queue_url,
                "SNS_TOPIC": topic.topic_arn,
            },
        )
        queue_source = _lambda_sources.SqsEventSource(queue)
        lambda_02.add_event_source(queue_source)

        lambda_03 = _lambda.Function(
            scope=self,
            id=f"lambda3-{my_name}",
            code=_lambda.Code.from_asset("src"),
            handler="func_from_crontab_to_sns_sqs.handler",
            function_name="Service03",
            timeout=Duration.seconds(10),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            tracing=_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "DEBUG",
                "EVENT_TARGET": "bridge",
                "SQS_QUEUE": queue.queue_url,
                "SNS_TOPIC": topic.topic_arn,
            },
        )
        sns_source = _lambda_sources.SnsEventSource(topic)
        lambda_03.add_event_source(sns_source)

        lambda_04 = _lambda.Function(
            scope=self,
            id=f"lambda4-{my_name}",
            code=_lambda.Code.from_asset("src"),
            handler="func_from_crontab_to_sns_sqs.handler",
            function_name="Service04",
            timeout=Duration.seconds(10),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            role=lambda_role,
            tracing=_lambda.Tracing.ACTIVE,
            environment={
                "LOG_LEVEL": "DEBUG",
                "EVENT_TARGET": "end",
                "SQS_QUEUE": queue.queue_url,
                "SNS_TOPIC": topic.topic_arn,
            },
        )

        rule = _events.Rule(
            self,
            "rule-eventbridge3",
            event_pattern=_events.EventPattern(
                source=["publish_to_bridge"],
                detail_type=["publish_to_bridge"],
            ),
        )
        rule.add_target(_targets.LambdaFunction(lambda_04, retry_attempts=3))
