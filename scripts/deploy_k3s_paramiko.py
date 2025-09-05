#!/usr/bin/env python3
import paramiko
import time

HOST = "103.9.205.28"
PORT = 2012
USERNAME = "root"
PASSWORD = "Next-Step@2310"

REMOTE_REPO_DIR = "/tmp/marketplace"

CMDS = [
    ("check kubectl", "which kubectl || echo 'kubectl not found'"),
    ("check k3s", "k3s --version || echo 'k3s not found'"),
    ("install k3s", "curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644"),
    ("kubeconfig", "mkdir -p ~/.kube && cp /etc/rancher/k3s/k3s.yaml ~/.kube/config && chmod 600 ~/.kube/config && (which kubectl || ln -sf /usr/local/bin/kubectl /usr/bin/kubectl || true)"),
    ("kubectl version", "kubectl version --output=yaml | cat"),
    ("cluster-info", "kubectl cluster-info | cat"),
]

APPLY = [
    ("namespace", f"kubectl apply -f {REMOTE_REPO_DIR}/k8s/namespace.yaml | cat"),
    ("configmap", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/configmap.yaml | cat"),
    ("mysql-init-cm", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/mysql-init-configmap.yaml | cat"),
    ("mysql-pvc", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/mysql-pvc.yaml | cat"),
    ("app-pvc", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/app-pvc.yaml | cat"),
    ("mysql-deploy", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/mysql-deployment.yaml | cat"),
    ("php-deploy", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/php-deployment.yaml | cat"),
    ("nginx-configmap", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/nginx-configmap.yaml | cat"),
    ("nginx-deploy", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/nginx-deployment.yaml | cat"),
    ("ingress", f"kubectl -n marketplace apply -f {REMOTE_REPO_DIR}/k8s/ingress.yaml | cat"),
]

def run(ssh: paramiko.SSHClient, cmd: str, timeout: int = 600) -> str:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="ignore")
    err = stderr.read().decode("utf-8", errors="ignore")
    return (out + err).strip()

def main():
    print("Connecting via SSH and preparing Kubernetes...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD, look_for_keys=False, allow_agent=False)

    try:
        print("\n[1/4] Pre-flight checks and k3s install (if needed)")
        print(run(ssh, CMDS[0][1]))
        print(run(ssh, CMDS[1][1]))

        k3s_check = run(ssh, "k3s --version || echo MISSING")
        if "MISSING" in k3s_check or "not found" in k3s_check.lower():
            print("Installing k3s...")
            print(run(ssh, CMDS[2][1]))
        else:
            print("k3s already installed.")

        print("\n[2/4] Configure kubeconfig & kubectl")
        print(run(ssh, CMDS[3][1]))

        print("\n[3/4] Cluster sanity checks")
        print(run(ssh, CMDS[4][1]))
        print(run(ssh, CMDS[5][1]))

        print("\n[4/4] Apply manifests (namespace, configmaps, PVCs, deployments, ingress)")
        for name, cmd in APPLY:
            print(f"\n-- Applying {name} --")
            print(run(ssh, cmd))

        # Wait for pods to be Ready
        print("\nWaiting for marketplace pods to become Ready (timeout ~300s)...")
        deadline = time.time() + 300
        while time.time() < deadline:
            pods = run(ssh, "kubectl -n marketplace get pods -o wide | cat")
            if pods.strip():
                lines = [l for l in pods.splitlines() if l and not l.lower().startswith("name")] 
                statuses = [l.split() for l in lines]
                all_ready = bool(lines) and all((
                    ("/" in cols[1] and cols[1].split("/")[0] == cols[1].split("/")[1]) and ("Running" in cols[2])
                ) for cols in statuses if len(cols) >= 3)
                if all_ready:
                    print("Pods Ready:")
                    print(pods)
                    break
                else:
                    print(pods)
            time.sleep(5)

        print("\nFinal status:")
        print(run(ssh, "kubectl get nodes -o wide | cat"))
        print(run(ssh, "kubectl -n marketplace get all | cat"))

    finally:
        ssh.close()

if __name__ == "__main__":
    main()


