def get_namespace(k8sCore, namespace):
    """
    return if namespace is found in the clusters namespaces
    """
    namespaces = [
        namespace.metadata.name for namespace in k8sCore.list_namespace().items
    ]
    if namespace in namespaces:
        return True
    else:
        return False


def get_deployment(k8sApp, namespace, deployment):
    """
    return true if deployment is found in the namespace
    """
    deployments = [
        deployment.metadata.name
        for deployment in k8sApp.list_namespaced_deployment(namespace).items
    ]
    if deployment in deployments:
        return True
    else:
        return False


def get_daemonset(k8sApp, namespace, daemonset):
    """
    return true if daemonset is found in the namespace and has the same number of desired and running pods
    """

    daemonsets = [
        daemonset.metadata.name
        for daemonset in k8sApp.list_namespaced_daemon_set(namespace).items
    ]
    print(daemonsets)
    for daemon in daemonsets:
        if daemon == daemonset:
            print(f"Found daemonset {daemonset} in namespace {namespace}")
            d = k8sApp.read_namespaced_daemon_set(daemon, namespace)
            desired = d.status.desired_number_scheduled
            running = d.status.number_ready
            if desired == running:
                return True
            else:
                return False


def get_secrets(k8sCore, namespace, secrets):
    """
    Return true if all secrets are found in the namespace
    """
    DEPLOYED_SECRETS = []
    ns_secrets = k8sCore.list_namespaced_secret(namespace)
    for secret in ns_secrets.items:
        DEPLOYED_SECRETS.append(secret.metadata.name)

    if compare_arrays(secrets, DEPLOYED_SECRETS):
        return True
    else:
        return False


def get_service_accounts(k8sCore, namespace, service_accounts):
    """
    Return true if all service accounts are found in namespace
    """
    DEPLOYED_SERVICE_ACCOUNTS = []
    ns_service_accounts = k8sCore.list_namespaced_service_account(namespace)
    for service_account in ns_service_accounts.items:
        DEPLOYED_SERVICE_ACCOUNTS.append(service_account.metadata.name)
    if compare_arrays(service_accounts, DEPLOYED_SERVICE_ACCOUNTS):
        return True
    else:
        return False


def get_configmaps(k8sCore, namespace, configmaps):
    """
    Return true if all configmaps are found in namespace
    """
    DEPLOYED_CONFIGMAPS = []
    ns_configmaps = k8sCore.list_namespaced_config_map(namespace)
    for configmap in ns_configmaps.items:
        DEPLOYED_CONFIGMAPS.append(configmap.metadata.name)
    if compare_arrays(configmaps, DEPLOYED_CONFIGMAPS):
        return True
    else:
        return False


def get_services(k8sCore, namespace, services):
    """
    Return true if service is found in namespace
    """
    DEPLOYED_SERVICES = []
    ns_services = k8sCore.list_namespaced_service(namespace)
    for live_service in ns_services.items:
        DEPLOYED_SERVICES.append(live_service.metadata.name)
    if compare_arrays(services, DEPLOYED_SERVICES):
        return True
    else:
        return False


def get_roles(k8sRbac, namespace, roles):
    """
    Return true if role is found in namespace
    """
    DEPLOYED_ROLES = []
    ns_roles = k8sRbac.list_namespaced_role(namespace)
    for live_roles in ns_roles.items:
        DEPLOYED_ROLES.append(live_roles.metadata.name)
    if compare_arrays(roles, DEPLOYED_ROLES):
        return True
    else:
        return False


########### sub functions ############


def compare_arrays(array1, array2):
    """
    Compares two arrays and looks to see if the values in array1 are in array2.
    used for secret / configmap / service account testing

    Args:
      array1: A list of values.
      array2: A list of values.

    Returns:
      True if all of the values in array1 are in array2, False otherwise.
    """

    # Create a set of the values in array2.
    array2_set = set(array2)

    # Iterate over the values in array1 and check if they are in array2_set.
    for value in array1:
        if value not in array2_set:
            return False

    # If all of the values in array1 are in array2_set, return True.
    return True
