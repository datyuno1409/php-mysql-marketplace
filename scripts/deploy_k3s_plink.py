#!/usr/bin/env python3
import subprocess
import shlex
import time
import os

HOST = "root@103.9.205.28"
PORT = "2012"
PASSWORD = "Next-Step@2310"

def run_remote(cmd: str, timeout: int = 120) -> str:
    full = f"plink -ssh -P {PORT} -pw {PASSWORD} {HOST} \"{cmd}\""
    proc = subprocess.run(shlex.split(full), capture_output=True, text=True, timeout=timeout)
    return (proc.stdout or "") + (proc.stderr or "")

def main():
    print("Installing/Validating k3s (Kubernetes) on remote server...")
    print("=" * 60)

    # 1) Check kubectl/k3s
    print("\n[1/5] Checking current kubectl/k3s availability...")
    print(run_remote("which kubectl || echo 'kubectl not found'"))
    print(run_remote("k3s --version || echo 'k3s not found'"))

    # 2) Install k3s if missing
    print("\n[2/5] Installing k3s if not present...")
    out = run_remote("k3s --version 2>/dev/null || echo MISSING")
    if "MISSING" in out or "not found" in out.lower():
        print("k3s not found. Installing...")
        install_cmd = (
            "curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644"
        )
        print(run_remote(install_cmd, timeout=600))
    else:
        print("k3s already installed.")

    # 3) Ensure kubectl works and kubeconfig is set
    print("\n[3/5] Configuring kubeconfig and verifying kubectl...")
    print(run_remote("mkdir -p ~/.kube && cp /etc/rancher/k3s/k3s.yaml ~/.kube/config && chmod 600 ~/.kube/config && (which kubectl || ln -sf /usr/local/bin/kubectl /usr/bin/kubectl || true)"))

    # 4) Wait for node to be Ready
    print("\n[4/5] Waiting for node to become Ready (timeout ~120s)...")
    ready = False
    for i in range(40):
        nodes = run_remote("kubectl get nodes --no-headers 2>/dev/null | cat")
        if nodes.strip() and " Ready " in (" " + nodes + " "):
            ready = True
            print("Node is Ready:")
            print(nodes)
            break
        time.sleep(3)
    if not ready:
        print("Node not Ready yet. Current state:")
        print(run_remote("kubectl get nodes -o wide | cat"))

    # 5) Report cluster info
    print("\n[5/5] Cluster information:")
    print("\n- kubectl version:")
    print(run_remote("kubectl version --output=yaml | cat"))
    print("\n- cluster-info:")
    print(run_remote("kubectl cluster-info | cat"))
    print("\n- nodes:")
    print(run_remote("kubectl get nodes -o wide | cat"))
    print("\n- namespaces:")
    print(run_remote("kubectl get ns | cat"))

    # 6) Copy k8s files to remote server
    print("\n[6/6] Copying k8s files to remote server...")
    k8s_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k8s")
    remote_dir = "/tmp/marketplace/k8s"
    
    # Create remote directory
    run_remote(f"mkdir -p {remote_dir}")
    
    # Copy each file in k8s directory to remote server
    for filename in os.listdir(k8s_dir):
        local_file = os.path.join(k8s_dir, filename)
        if os.path.isfile(local_file):
            with open(local_file, 'r') as f:
                content = f.read()
            # Escape quotes in content
            content = content.replace('"', '\\"')
            # Write content to remote file
            run_remote(f"cat > {remote_dir}/{filename} << 'EOL'\n{content}\nEOL")
    
    # 7) Apply manifests in k8s/
    print("\n[7/7] Apply manifests in k8s/ ...")
    # Apply namespace first
    print(run_remote(f"kubectl apply -f {remote_dir}/namespace.yaml | cat"))
    # Apply config and PVCs
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/configmap.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/mysql-init-configmap.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/mysql-pvc.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/app-pvc.yaml | cat"))
    # Apply deployments and nginx config
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/mysql-deployment.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/php-deployment.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/nginx-configmap.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/nginx-deployment.yaml | cat"))
    print(run_remote(f"kubectl -n marketplace apply -f {remote_dir}/ingress.yaml | cat"))

    # Wait for pods Ready
    print("\nWaiting for marketplace pods to become Ready (timeout ~300s)...")
    ready_printed = False
    for i in range(100):
        pods = run_remote("kubectl -n marketplace get pods -o wide | cat")
        if pods.strip():
            lines = [l for l in pods.splitlines() if l and not l.lower().startswith("name")] 
            statuses = [l.split() for l in lines]
            # crude check: look for READY like 1/1 and STATUS Running
            all_ready = any(lines) and all((
                ("/" in cols[1] and cols[1].split("/")[0] == cols[1].split("/")[1]) and ("Running" in cols[2])
                ) for cols in statuses if len(cols) >= 3)
            if all_ready:
                print("Pods Ready:")
                print(pods)
                ready_printed = True
                break
        time.sleep(3)
    if not ready_printed:
        print("Pods not fully Ready yet. Current status:")
        print(run_remote("kubectl -n marketplace get pods -o wide | cat"))

if __name__ == "__main__":
    main()