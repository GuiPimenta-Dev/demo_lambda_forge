from functions.another_hello_world.config import AnotherHelloWorldConfig
from functions.authorizers.auth.config import AuthConfig
from functions.hello_world.config import HelloWorldConfig
from functions.docs.config import DocsConfig
from functions.authorizers.docs_authorizer.config import DocsAuthorizerConfig
from aws_cdk import Stack
from constructs import Construct
from infra.services import Services
from lambda_forge import release

@release
class LambdaStack(Stack):
    def __init__(
        self,
        scope: Construct,
        stage,
        arns,
        **kwargs,
    ) -> None:

        name = scope.node.try_get_context("name")
        super().__init__(scope, f"{name}-CDK", **kwargs)

        self.services = Services(self, stage, arns)

        # Authorizers
        AuthConfig(self.services)
        DocsAuthorizerConfig(self.services)

        # Docs
        DocsConfig(scope, self.services)

        # HelloWorld
        HelloWorldConfig(self.services)

        # AnotherHelloWorld
        AnotherHelloWorldConfig(self.services)
