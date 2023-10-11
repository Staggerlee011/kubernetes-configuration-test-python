import pytest
from kubernetes import client, config
from utils import (
    get_daemonset,
    get_deployment,
    get_services,
    get_namespace,
    get_secrets,
    get_service_accounts,
    get_configmaps,
    get_roles,
)

#################### FIXTURES ####################


@pytest.fixture(scope="class")
def k8sApp():
    """A fixture that provides a Kubernetes connection."""
    # Load active kube config (kubectx friendly)
    config.load_kube_config()
    k8sApp = client.AppsV1Api()
    return k8sApp


@pytest.fixture(scope="class")
def k8sCore():
    """A fixture that provides a Kubernetes connection."""

    # Load active kube config (kubectx friendly)
    config.load_kube_config()
    # Create CoreV1Api and AppsV1Api instances
    k8sCore = client.CoreV1Api()
    if k8sCore:
        return k8sCore
    else:
        error("Could not create k8sCore object")


@pytest.fixture(scope="class")
def k8sRbac():
    """A fixture that provides a Kubernetes connection."""

    # Load active kube config (kubectx friendly)
    config.load_kube_config()
    # Create CoreV1Api and AppsV1Api instances
    k8sRbac = client.RbacAuthorizationV1Api()
    if k8sRbac:
        return k8sRbac
    else:
        error("Could not create k8sRbac object")


#################### amazon cloudwatch metrics ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_aws_cloudwatch_metrics:
    def test_aws_cloudwatch_metrics_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "amazon-cloudwatch") is True

    def test_aws_cloudwatch_metrics_daemonset(self, k8sApp):
        assert (
            get_daemonset(
                k8sApp,
                namespace="amazon-cloudwatch",
                daemonset="aws-cloudwatch-metrics",
            )
            is True
        )

    def test_aws_cloudwatch_metricsh_secrets(self, k8sCore):
        assert (
            get_secrets(
                k8sCore,
                namespace="amazon-cloudwatch",
                secrets=["sh.helm.release.v1.aws-cloudwatch-metrics.v1"],
            )
            is True
        )

    def test_aws_cloudwatch_metrics_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="amazon-cloudwatch",
                service_accounts=["aws-cloudwatch-metrics"],
            )
            is True
        )

    def test_aws_cloudwatch_metrics_configmaps(self, k8sCore):
        assert (
            get_configmaps(
                k8sCore,
                namespace="amazon-cloudwatch",
                configmaps=[
                    "aws-cloudwatch-metrics",
                    "cwagent-clusterleader",
                    "kube-root-ca.crt",
                ],
            )
            is True
        )


#################### efs-csi-node ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_efs_csi_node:
    def test_efs_csi_node_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_efs_csi_node_daemonset(self, k8sApp):
        assert (
            get_daemonset(k8sApp, namespace="kube-system", daemonset="efs-csi-node")
            is True
        )

    def test_efs_csi_node_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="kube-system",
                service_accounts=["efs-csi-controller-sa"],
            )
            is True
        )


#################### ebs-csi-node ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_ebs_csi_node:
    def test_ebs_csi_node_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_ebs_csi_node_daemonset(self, k8sApp):
        assert (
            get_daemonset(k8sApp, namespace="kube-system", daemonset="ebs-csi-node")
            is True
        )

    def test_ebs_csi_node_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore, namespace="kube-system", service_accounts=["ebs-csi-node-sa"]
            )
            is True
        )

    def test_ebs_csi_node_roles(self, k8sRbac):
        assert (
            get_roles(k8sRbac, namespace="kube-system", roles=["ebs-csi-leases-role"])
            is True
        )


#################### metrics server ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_metrics_server:
    def test_metrics_server_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_metrics_server_deployment(self, k8sApp):
        assert (
            get_deployment(k8sApp, namespace="kube-system", deployment="metrics-server")
            is True
        )

    def test_metrics_server_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore, namespace="kube-system", service_accounts=["metrics-server"]
            )
            is True
        )

    def test_metrics_server_services(self, k8sCore):
        assert (
            get_services(k8sCore, namespace="kube-system", services=["metrics-server"])
            is True
        )


#################### coredns ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_core_dns:
    def test_core_dns_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_core_dns_deployment(self, k8sApp):
        assert (
            get_deployment(k8sApp, namespace="kube-system", deployment="coredns")
            is True
        )

    def test_core_dns_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore, namespace="kube-system", service_accounts=["coredns"]
            )
            is True
        )

    def test_core_dns_services(self, k8sCore):
        assert (
            get_services(k8sCore, namespace="kube-system", services=["kube-dns"])
            is True
        )


#################### aws_load_balancer_controller ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_aws_load_balancer_controller:
    def test_aws_load_balancer_controller_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_aws_load_balancer_controller_deployment(self, k8sApp):
        assert (
            get_deployment(
                k8sApp,
                namespace="kube-system",
                deployment="aws-load-balancer-controller",
            )
            is True
        )

    def test_aws_load_balancer_controller_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="kube-system",
                service_accounts=["aws-load-balancer-controller-sa"],
            )
            is True
        )

    def test_aws_load_balancer_controller_services(self, k8sCore):
        assert (
            get_services(
                k8sCore,
                namespace="kube-system",
                services=["aws-load-balancer-webhook-service"],
            )
            is True
        )

    def test_aws_load_balancer_controller_secrets(self, k8sCore):
        assert (
            get_secrets(
                k8sCore, namespace="kube-system", secrets=["aws-load-balancer-tls"]
            )
            is True
        )

    def test_aws_load_balancer_controller_roles(self, k8sRbac):
        assert (
            get_roles(
                k8sRbac,
                namespace="kube-system",
                roles=["aws-load-balancer-controller-leader-election-role"],
            )
            is True
        )


#################### cluster_autoscaler ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_cluster_autoscaler:
    def test_cluster_autoscaler_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_cluster_autoscaler_deployment(self, k8sApp):
        assert (
            get_deployment(
                k8sApp,
                namespace="kube-system",
                deployment="cluster-autoscaler-aws-cluster-autoscaler",
            )
            is True
        )

    def test_cluster_autoscaler_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="kube-system",
                service_accounts=["cluster-autoscaler-sa"],
            )
            is True
        )

    def test_cluster_autoscaler_services(self, k8sCore):
        assert (
            get_services(
                k8sCore,
                namespace="kube-system",
                services=["cluster-autoscaler-aws-cluster-autoscaler"],
            )
            is True
        )

    def test_cluster_autoscaler_roles(self, k8sRbac):
        assert (
            get_roles(
                k8sRbac,
                namespace="kube-system",
                roles=["cluster-autoscaler-aws-cluster-autoscaler"],
            )
            is True
        )


#################### vpa ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_vpa:
    def test_vpa_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "vpa") is True

    def test_vpa_deployment(self, k8sApp):
        assert (
            get_deployment(
                k8sApp, namespace="vpa", deployment="vpa-admission-controller"
            )
            is True
        )
        assert (
            get_deployment(k8sApp, namespace="vpa", deployment="vpa-recommender")
            is True
        )
        assert get_deployment(k8sApp, namespace="vpa", deployment="vpa-updater") is True

    def test_vpa_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="vpa",
                service_accounts=[
                    "vpa-admission-controller",
                    "vpa-recommender",
                    "vpa-updater",
                ],
            )
            is True
        )

    def test_vpa_services(self, k8sCore):
        assert get_services(k8sCore, namespace="vpa", services=["vpa-webhook"]) is True

    def test_vpa_configmaps(self, k8sCore):
        assert (
            get_configmaps(k8sCore, namespace="vpa", configmaps=["kube-root-ca.crt"])
            is True
        )

    def test_vpc_secrets(self, k8sCore):
        assert get_secrets(k8sCore, namespace="vpa", secrets=["vpa-tls-certs"]) is True


#################### external_secrets ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_external_secrets:
    def test_external_secrets_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "external-secrets") is True

    def test_external_secrets_deployments(self, k8sApp):
        assert (
            get_deployment(
                k8sApp, namespace="external-secrets", deployment="external-secrets"
            )
            is True
        )
        assert (
            get_deployment(
                k8sApp,
                namespace="external-secrets",
                deployment="external-secrets-cert-controller",
            )
            is True
        )
        assert (
            get_deployment(
                k8sApp,
                namespace="external-secrets",
                deployment="external-secrets-webhook",
            )
            is True
        )

    def test_external_secrets_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore,
                namespace="external-secrets",
                service_accounts=[
                    "external-secrets-sa",
                    "external-secrets-cert-controller",
                    "external-secrets-webhook",
                ],
            )
            is True
        )

    def test_external_secrets_service(self, k8sCore):
        assert (
            get_services(
                k8sCore,
                namespace="external-secrets",
                services=["external-secrets-webhook"],
            )
            is True
        )

    def test_external_secrets_configmaps(self, k8sCore):
        assert (
            get_configmaps(
                k8sCore, namespace="external-secrets", configmaps=["kube-root-ca.crt"]
            )
            is True
        )

    def test_external_secrets_secrets(self, k8sCore):
        assert (
            get_secrets(
                k8sCore,
                namespace="external-secrets",
                secrets=[
                    "external-secrets-webhook",
                    "sh.helm.release.v1.external-secrets.v1",
                ],
            )
            is True
        )

    def test_external_secrets_roles(self, k8sRbac):
        assert (
            get_roles(
                k8sRbac,
                namespace="external-secrets",
                roles=["external-secrets-leaderelection"],
            )
            is True
        )


#################### vpc_cni ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_vpc_cni:
    def test_vpc_cni_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_vpc_cni_daemonset(self, k8sApp):
        assert (
            get_daemonset(k8sApp, namespace="kube-system", daemonset="aws-node") is True
        )

    def test_vpc_cni_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore, namespace="kube-system", service_accounts=["aws-node"]
            )
            is True
        )


#################### kube_proxy ####################


@pytest.mark.blueprint
@pytest.mark.usefixtures("k8sCore")
@pytest.mark.usefixtures("k8sApp")
class Test_kube_proxy:
    def test_kube_proxy_namespace(self, k8sCore):
        assert get_namespace(k8sCore, "kube-system") is True

    def test_kube_proxy_daemonset(self, k8sApp):
        assert (
            get_daemonset(k8sApp, namespace="kube-system", daemonset="kube-proxy")
            is True
        )

    def test_kube_proxy_service_accounts(self, k8sCore):
        assert (
            get_service_accounts(
                k8sCore, namespace="kube-system", service_accounts=["kube-proxy"]
            )
            is True
        )

    def test_kube_proxy_configmaps(self, k8sCore):
        assert (
            get_configmaps(
                k8sCore,
                namespace="kube-system",
                configmaps=["kube-proxy", "kube-proxy-config"],
            )
            is True
        )


#################### load ####################

if __name__ == "__main__":
    pytest.main()
