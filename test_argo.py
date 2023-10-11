import pytest
from kubernetes import client, config
from kubernetes.client.rest import ApiException


# get the current context from the configuration
current_context = config.list_kube_config_contexts()[1]
full_cluster_cluster = current_context["context"]["cluster"].split("/")
cluster_name = full_cluster_cluster[-1]
# print(cluster_name)

APPLICATIONS = [
    "cert-manager",
    "prometheus-helm",
    "external-dns",
    "kubecost",
    "acm-updater",
    "falco",
    "falco-exporter",
    "fluent-bit",
    "goldilocks",
    "letsencrypt-oc-io",
]

TEST_APPLICATIONS = []
for application in APPLICATIONS:
    TEST_APPLICATIONS.append(f"{application}-{cluster_name}")


@pytest.mark.argo
@pytest.mark.parametrize("object", TEST_APPLICATIONS)
def test_argo_application_health(object):
    # Load the kubeconfig file
    config.load_kube_config(context="mgmt")

    # Create an instance of the CustomObjectsApi class
    api_instance = client.CustomObjectsApi()

    # Get the Argo application object
    try:
        api_response = api_instance.get_namespaced_custom_object(
            group="argoproj.io",
            version="v1alpha1",
            namespace="argocd",
            plural="applications",
            name=object,
        )
    except ApiException as e:
        pytest.fail(f"Failed to get Argo application: {e}")

    # Check the status of the Argo application
    application_status = api_response["status"]
    assert application_status["health"]["status"] == "Healthy"
