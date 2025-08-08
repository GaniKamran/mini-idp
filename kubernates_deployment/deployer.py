from kubernetes import client, config


class AppDeployer:
    def __init__(self, config_data, namespace="default"):
        self.config_data = config_data
        self.namespace = namespace
        config.load_kube_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def _build_env_vars(self):
        return [
            client.V1EnvVar(name=key, value=value)
            for key, value in self.config_data.get("env", {}).items()
        ]

    def _build_container(self):
        return client.V1Container(
            name=self.config_data["name"],
            image=self.config_data["image"],
            ports=[client.V1ContainerPort(container_port=self.config_data["port"])],
            env=self._build_env_vars()
        )

    def _build_deployment(self):
        container = self._build_container()

        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": self.config_data["name"]}),
            spec=client.V1PodSpec(containers=[container])
        )

        spec = client.V1DeploymentSpec(
            replicas=self.config_data.get("replicas", 1),
            selector=client.V1LabelSelector(
                match_labels={"app": self.config_data["name"]}
            ),
            template=template
        )

        return client.V1Deployment(
            metadata=client.V1ObjectMeta(name=self.config_data["name"]),
            spec=spec
        )

    def _build_service(self):
        return client.V1Service(
            metadata=client.V1ObjectMeta(name=self.config_data["name"]),
            spec=client.V1ServiceSpec(
                selector={"app": self.config_data["name"]},
                ports=[client.V1ServicePort(
                    protocol="TCP",
                    port=80,
                    target_port=self.config_data["port"]
                )],
                type="ClusterIP"
            )
        )

    def deploy(self):
        deployment = self._build_deployment()
        service = self._build_service()

        self.apps_v1.create_namespaced_deployment(
            namespace=self.namespace,
            body=deployment
        )

        self.core_v1.create_namespaced_service(
            namespace=self.namespace,
            body=service
        )

        print(f"✅ App '{self.config_data['name']}' deployed successfully to namespace '{self.namespace}'")
