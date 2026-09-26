# AI GitOps Portfolio Package

## Deliverable 1: Professional README.md

```
# AI GitOps: Self-Hosted LLM Deployment on Kubernetes with Argo CD

![Kubernetes](https://img.shields.io/badge/Kubernetes-K3s-blue?logo=kubernetes&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-Argo_CD-orange?logo=argo&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-green?logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Ollama%20%7C%20Qwen3%3A4b-black?logo=ollama&logoColor=white)
![Cloud](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)

An end-to-end GitOps continuous delivery pipeline that deploys a containerized Flask AI web client and a persistent Ollama LLM service running the **Qwen3:4b** model onto a K3s Kubernetes cluster hosted on AWS EC2, automated seamlessly with Argo CD.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Repository Structure](#-repository-structure)
- [Kubernetes Components](#-kubernetes-components)
- [GitOps Workflow](#-gitops-workflow)
- [Deployment Steps](#-deployment-steps)
- [Verification & Testing](#-verification--testing)
- [Troubleshooting](#-troubleshooting)
- [Project Results & Impact](#-project-results--impact)
- [Future Improvements](#-future-improvements)
- [Skills Demonstrated](#-skills-demonstrated)

---

## 💡 Overview

This project demonstrates a production-style declarative GitOps architecture for hosting localized AI workloads. By combining **Argo CD**, **K3s**, and **Ollama**, infrastructure state is entirely defined as code (IaC) inside Git. Any operational change pushed to the `main` branch is automatically synchronized into the Kubernetes cluster.

### Key Objectives
* **Declarative Infrastructure:** Keep all Kubernetes manifests (`/k8s`) synchronized via Git.
* **Persistent AI Inference:** Retain downloaded LLM model weights across pod restarts using a dedicated Persistent Volume Claim (`6Gi PVC`).
* **Microservices Communication:** Decouple the frontend client application (`ai-client`) from the LLM engine (`ollama`) using internal Kubernetes ClusterIP services.

---

## 🏗 Architecture


```

Developer
│
▼
GitHub Repository (main)
│
▼
Argo CD (Reconciler)
│
▼
K3s / Kubernetes Cluster (AWS EC2 - Ubuntu 26.04 LTS)
│
└── Namespace: ai-gitops
│
├── NodePort Service (:30601) ──► Flask AI Client (:5000)
│                                       │
│ (http://ollama:11434/api/chat)        │
▼                                       ▼
ClusterIP Service (:11434) ────────► Ollama Engine + Qwen3:4b Model
│
▼
PVC (6Gi Storage)

````

---

## ✨ Key Features

* **Automated CD Pipeline:** Argo CD detects changes in Git and reconciles cluster state within minutes without manual `kubectl` intervention.
* **Decoupled Architecture:** Separates the web presentation tier (`Flask`) from heavy ML computation workloads (`Ollama`).
* **Data Persistence:** Dedicated Persistent Volume Claim (`6Gi`) ensures the `Qwen3:4b` model weights survive pod reinstantiations.
* **Automated Internal Routing:** Utilizes Kubernetes DNS resolution (`http://ollama:11434/api/chat`) for efficient service-to-service communication.
* **Lightweight Footprint:** Built on K3s running on AWS EC2, optimizing resource consumption while maintaining full Kubernetes API compatibility.

---

## 🛠 Technology Stack

* **Cloud Platform:** AWS EC2
* **OS:** Ubuntu 26.04 LTS
* **Kubernetes Orchestration:** K3s
* **GitOps Engine:** Argo CD
* **Containerization:** Docker
* **Frontend/Client:** Python, Flask, HTML5/CSS3
* **AI/LLM Engine:** Ollama with `Qwen3:4b` model
* **Version Control:** GitHub (`hasnainbanusi/ai-gitops`)

---

## 📁 Repository Structure

```directory
.
├── k8s/                         # Kubernetes Manifests
│   ├── namespace.yaml           # Namespace definition (ai-gitops)
│   ├── ollama-pvc.yaml          # PersistentVolumeClaim for model storage (6Gi)
│   ├── ollama-deployment.yaml   # Deployment for Ollama engine
│   ├── ollama-service.yaml      # ClusterIP service for internal API traffic
│   ├── ai-client-deployment.yaml# Flask web application deployment
│   └── ai-client-service.yaml   # NodePort service exposing port 30601
├── app/                         # Flask Application Source Code
│   ├── app.py                   # Main Flask application server logic
│   ├── templates/               # HTML UI templates
│   ├── Dockerfile               # Container spec for ai-client
│   └── requirements.txt         # Python dependencies
├── argocd/                      # Argo CD Application Manifest
│   └── application.yaml         # GitOps sync source & destination specs
└── README.md                    # Documentation

````

## ☸️ Kubernetes Components

1. **Namespace (`ai-gitops`):** Encapsulates all application resources for clean isolation.

2. **PersistentVolumeClaim (`ollama-pvc`):** Requests `6Gi` storage utilizing standard local-path storage classes to store model assets under `/root/.ollama`.

3. **Ollama Deployment & ClusterIP Service:**

   * Deployment: Runs the official `ollama/ollama` image mounted to `ollama-pvc`.

   * Service: Exposes internal port `11434` as `http://ollama:11434`.

4. **AI Client Deployment & NodePort Service:**

   * Deployment: Runs the customized Flask container interacting with the internal Ollama service.

   * Service: Maps container port `5000` to external NodePort `30601`.

## 🔄 GitOps Workflow

1. **Code Modification:** Developer commits changes to application logic or Kubernetes manifests on branch `main`.

2. **Push to GitHub:** Commit `feb05dd` pushed updates, including the NodePort service spec (`ai-client-service.yaml`).

3. **Argo CD Reconcile:** Argo CD detects target state divergence between `main/k8s` and the active cluster.

4. **Automated Sync:** Argo CD applies necessary object creations or mutations directly to the `ai-gitops` namespace.

## 🚀 Deployment Steps

### Prerequisites

* An active AWS EC2 Instance (Ubuntu 26.04 LTS) with ports `80`, `443`, `6443`, and `30601` open in the Security Group.

* Installed `k3s` and `kubectl`.

* Argo CD installed in the `argocd` namespace.

### Step-by-Step Guide

1. **Clone the Repository:**

   ```
   git clone https://github.com/hasnainbanusi/ai-gitops.git
   cd ai-gitops
   
   ```

2. **Apply Argo CD Application Manifest:**

   ```
   kubectl apply -f argocd/application.yaml
   
   ```

3. **Verify GitOps Sync:**

   ```
   kubectl get application -n argocd
   
   ```

4. **Verify Resources in `ai-gitops` Namespace:**

   ```
   kubectl get all -n ai-gitops
   kubectl get pvc -n ai-gitops
   
   ```

5. **Initialize LLM Model in Ollama Pod:**

   ```
   # Get Ollama Pod Name
   OLLAMA_POD=$(kubectl get pods -n ai-gitops -l app=ollama -o jsonpath='{.items[0].metadata.name}')
   
   # Pull Qwen3:4b Model into Persistent Storage
   kubectl exec -n ai-gitops -it $OLLAMA_POD -- ollama pull qwen3:4b
   
   ```

## 🧪 Verification & Testing

### 1. Browser Access

Navigate to your AWS EC2 Public IP on NodePort `30601`:

```
http://<AWS_EC2_PUBLIC_IP>:30601

```

### 2. API Endpoint Direct Test

Test the internal communication pipeline using `curl` directly from within the `ai-client` container or host:

```
curl -X POST http://<AWS_EC2_PUBLIC_IP>:30601/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain GitOps in two sentences."}'

```

**Expected Response:**

```
{
  "response": "GitOps is an operational framework that uses Git repositories as the single source of truth for infrastructure and application code. Automated tools like Argo CD continuously synchronize the cluster state with the code defined in Git."
}

```

## 🔍 Troubleshooting

| **Issue** | **Potential Cause** | **Resolution** | 
| **NodePort Unreachable** | AWS Security Group rule missing for port `30601`. | Add custom TCP rule allowing inbound traffic on port `30601`. | 
| **Flask returning 500 / Timeout** | Ollama pod is initializing or model is not pulled. | Run `kubectl exec` to ensure `qwen3:4b` is present via `ollama list`. | 
| **Argo CD `OutOfSync`** | Kubernetes manifest syntax error or path mismatch. | Check logs via `argocd app logs ai-gitops` or `kubectl describe application ai-gitops -n argocd`. | 
| **PVC Pending** | StorageClass unfulfilled or insufficient storage on disk. | Verify node disk space via `df -h` and ensure K3s local-path provisioner is active. | 

## 📈 Project Results & Impact

* **100% Automated Infrastructure Delivery:** Automated configuration sync eliminated drift and eliminated manual deployment steps.

* **Persistent Model Execution:** Zero AI data loss across pod lifecycle events due to configured storage claims.

* **Streamlined Developer Workflow:** Applied changes (such as commit `feb05dd` adding NodePort configurations) sync to the live environment automatically upon push.

## 🔮 Future Improvements

* \[ \] Implement an Ingress Controller with TLS termination using `cert-manager`.

* \[ \] Add HPA (Horizontal Pod Autoscaler) for the Flask frontend.

* \[ \] Integrate Prometheus and Grafana for monitoring inference latency and resource consumption.

* \[ \] Implement automated CI image builds via GitHub Actions with versioned tag updates in Git.

## 🛠 Skills Demonstrated

* **GitOps & Continuous Delivery:** Argo CD, Git Workflow, Continuous Synchronization

* **Container Orchestration:** Kubernetes (K3s), Deployments, Services (NodePort & ClusterIP), Stateful Storage (PVC)

* **Infrastructure & Cloud:** AWS EC2, Networking Security Groups, Linux (Ubuntu 26.04)

* **Application & AI Integration:** Python, Flask, REST APIs, Ollama, Qwen3:4b LLM Integration

````

---

## Deliverable 2: Portfolio Project Case Study Document

```markdown
# CASE STUDY: Enterprise AI Infrastructure Deployment using K3s, GitOps, and Argo CD

**Author:** Hasnain Banusi  
**Repository:** [github.com/hasnainbanusi/ai-gitops](https://github.com/hasnainbanusi/ai-gitops)  
**Target Domain:** Cloud Native / DevOps / AI Operations (AIOps)

---

## 1. Executive Summary

This case study details the design, implementation, and deployment of a self-hosted, cloud-native Artificial Intelligence inference platform using GitOps methodology. By leveraging lightweight Kubernetes (K3s) on AWS EC2, Argo CD, and containerized Python services, the platform provides a scalable, declarative environment hosting the **Qwen3:4b** Large Language Model through Ollama and a Flask client interface.

---

## 2. Project Objective & Challenge

### Objective
The primary objective was to build an automated, stateful Continuous Delivery infrastructure capable of hosting microservice-based AI workloads without manual cluster management interventions.

### Problem Statement
Deploying LLM workloads onto cloud infrastructure introduces specific engineering challenges:
1. **Infrastructure Drift & Manual Friction:** Deploying manifests manually via `kubectl` leads to configuration drift across environments.
2. **Heavy Model Ephemerality:** AI models are large (several gigabytes). Container recreations without persistent volume orchestration cause long recovery times due to model re-downloads.
3. **Service Routing Complexity:** Decoupling user-facing application components from internal inference engines requires robust service discovery and internal cluster routing.

---

## 3. Architecture & System Design

The application utilizes a microservices architecture hosted on an AWS EC2 instance running Ubuntu 26.04 LTS and K3s. 

### Core Architectural Layers:
* **Version Control Tier:** GitHub repository containing both application source code and declarative Kubernetes manifests under `/k8s`.
* **GitOps Control Plane:** Argo CD monitoring the repository's `main` branch to reconcile cluster state.
* **Frontend Tier (`ai-client`):** A Flask web application exposed externally via NodePort `30601`.
* **Inference Engine Tier (`ollama`):** An internal Ollama service running the `Qwen3:4b` model, exposed exclusively within the cluster via ClusterIP on port `11434`.
* **Storage Tier:** A `6Gi` PersistentVolumeClaim ensuring localized caching of model binaries.


````

+-----------------------------------------------------------------------+
|                              AWS EC2 Host                             |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  |                       K3s Kubernetes Cluster                    |  |
|  |                                                                 |  |
|  |  +-----------------------------------------------------------+  |  |
|  |  |                  Namespace: ai-gitops                     |  |  |
|  |  |                                                           |  |  |
|  |  |  +---------------------+        +----------------------+  |  |  |
|  |  |  |  ai-client Pod      |        |  ollama Pod          |  |  |  |
|  |  |  |  (Flask Port 5000)  |        |  (Qwen3:4b Engine)   |  |  |  |
|  |  |  +----------▲----------+        +----------▲-----------+  |  |  |
|  |  |             │                              │              |  |  |
|  |  |  +----------┴----------+        +----------┴-----------+  |  |  |
|  |  |  | NodePort Service    |        | ClusterIP Service    |  |  |  |
|  |  |  | Port 30601          |        | Port 11434           |  |  |  |
|  |  |  +----------▲----------+        +----------▲-----------+  |  |  |
|  |  |             │                              │              |  |  |
|  |  +-------------│------------------------------│--------------+  |  |
|  +----------------│------------------------------│-----------------+  |
|                   │                              │                    |
+-------------------|------------------------------|--------------------+
│                              │
External Access                   6Gi PVC Storage
(Browser / User)

```

---

## 4. Implementation Details

### Declarative Manifest Management
The workload was modularized into standalone manifests under `/k8s`:
- `namespace.yaml`: Segregates resources into `ai-gitops`.
- `ollama-pvc.yaml`: Bound persistent storage for model weight retention.
- `ollama-deployment.yaml` & `ollama-service.yaml`: Managed internal model processing nodes.
- `ai-client-deployment.yaml` & `ai-client-service.yaml`: Deployed the Flask frontend client.

### GitOps Sync Workflow
Argo CD was configured with an automated sync policy pointing to `https://github.com/hasnainbanusi/ai-gitops` targeting path `k8s`. 

During iterative development (e.g., Commit `feb05dd`), external networking requirements called for transitioning service exposure to NodePort. The spec update was committed directly to Git, and Argo CD automatically detected and applied the delta without downtime or manual cluster logins.

---

## 5. Technical Challenges & Solutions

### Challenge 1: Inter-service Communication Failure
* **Symptom:** The Flask web client timed out when attempting to forward user prompts to the AI backend.
* **Root Cause:** Hardcoded host IP addresses in the application layer failed upon pod reschedule events.
* **Solution:** Reconfigured the Flask API client to leverage Kubernetes CoreDNS internal service naming standard (`http://ollama:11434/api/chat`).

### Challenge 2: Model Lifecycle Ephemerality
* **Symptom:** Ollama pod recreations caused loss of downloaded `Qwen3:4b` weights, causing high latency during pod spin-up.
* **Solution:** Introduced a `PersistentVolumeClaim` (`ollama-pvc`) mounted directly to `/root/.ollama` in the container runtime environment.

---

## 6. Testing, Validation & Results

### Functional Testing
- **Browser Validation:** Verified user access to the Flask UI at `http://<EC2-IP>:30601`.
- **Inference Verification:** Executed prompt requests through the web UI and directly via API calls. Successfully received coherent completions generated by `Qwen3:4b`.

### Performance & Reliability Outcomes
- **Zero-Drift Execution:** 100% of cluster configurations match state stored in the Git repository.
- **Improved Recovery Time:** Pod restarts recover instantly without requiring model re-downloading.

---

## 7. Key DevOps Competencies Demonstrated

- **GitOps Infrastructure Management:** Argo CD declarative synchronization.
- **Container Orchestration:** K3s, Kubernetes Services, PVC, Pods, Namespaces.
- **Cloud Engineering:** AWS EC2 setup, Security Group networking configuration.
- **Application Integration:** Python, Flask, REST API orchestration, Local LLM Integration.

```

## Deliverable 3: LinkedIn Post

```
🚀 Excited to share my latest DevOps project: Automated Self-Hosted AI Infrastructure using GitOps & Kubernetes!

I recently completed a project focused on running Large Language Models (LLMs) on cloud-native infrastructure using GitOps practices. 

Instead of manually deploying microservices and AI engines using imperative commands, I built a declarative deployment pipeline that hosts a Flask AI client and an Ollama inference engine running the Qwen3:4b model inside a Kubernetes cluster—managed entirely by Argo CD.

🛠️ What I Built & Key Tech:
• AWS EC2 (Ubuntu 26.04 LTS) hosting a K3s Kubernetes cluster.
• Argo CD continuously monitoring the GitHub repository to automatically reconcile state changes.
• Flask AI Client (ai-client) exposed via NodePort 30601.
• Ollama Engine running Qwen3:4b exposed internally via ClusterIP (port 11434).
• Persistent Volume Claim (6Gi PVC) to ensure model weights survive pod reinstantiations.

🔄 GitOps in Action:
When I updated the service configuration to add NodePort exposure (commit feb05dd), Argo CD automatically picked up the changes from the main branch and synchronized the cluster within seconds—zero manual kubectl apply commands required.

🧪 Testing & Validation:
Successfully verified end-to-end communication from the browser client down to the internal Ollama engine, returning responses generated by Qwen3:4b.

💡 Key Takeaways:
1. GitOps eliminates drift and makes infrastructure management auditable and predictable.
2. Stateful storage claims (PVCs) are critical when managing persistent AI workloads on ephemeral container platforms.

🔮 Next Steps:
I plan to add Ingress with cert-manager for HTTPS termination and set up Prometheus/Grafana monitoring for inference performance.

📂 Explore the full repository and setup guide here:
https://github.com/hasnainbanusi/ai-gitops

#DevOps #Kubernetes #GitOps #ArgoCD #AWS #Docker #Python #Flask #AI #MachineLearning #AIOps #K3s #CloudComputing

```

## Deliverable 4: Architecture Diagrams

### 1. Detailed System Architecture Diagram (GitHub / Portfolio)

```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 700" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0d1117; }
      .box-dev { fill: #161b22; stroke: #30363d; stroke-width: 2; rx: 8px; }
      .box-aws { fill: #161f2c; stroke: #ff9900; stroke-width: 2; rx: 10px; }
      .box-k8s { fill: #0f2537; stroke: #326ce5; stroke-width: 2; rx: 10px; }
      .box-ns { fill: #132a40; stroke: #1f6feb; stroke-width: 2; stroke-dasharray: 4; rx: 8px; }
      .box-pod { fill: #21262d; stroke: #58a6ff; stroke-width: 1.5; rx: 6px; }
      .box-argo { fill: #2b1d1d; stroke: #ef7b4d; stroke-width: 2; rx: 8px; }
      .box-pvc { fill: #272015; stroke: #d29922; stroke-width: 1.5; rx: 6px; }
      .text-title { fill: #f0f6fc; font-family: Arial, sans-serif; font-weight: bold; font-size: 16px; }
      .text-sub { fill: #8b949e; font-family: Arial, sans-serif; font-size: 12px; }
      .text-light { fill: #c9d1d9; font-family: Arial, sans-serif; font-size: 13px; }
      .text-highlight { fill: #58a6ff; font-family: Arial, sans-serif; font-weight: bold; font-size: 13px; }
      .arrow { stroke: #58a6ff; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
      .arrow-orange { stroke: #ef7b4d; stroke-width: 2; fill: none; marker-end: url(#arrowhead-orange); }
      .arrow-green { stroke: #3fb950; stroke-width: 2; fill: none; marker-end: url(#arrowhead-green); }
    </style>
    <marker id="arrowhead" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#58a6ff"/>
    </marker>
    <marker id="arrowhead-orange" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef7b4d"/>
    </marker>
    <marker id="arrowhead-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#3fb950"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1000" height="700" class="bg" />

  <!-- Header -->
  <text x="500" y="35" class="text-title" font-size="20" text-anchor="middle">AI GitOps - System Architecture</text>
  <text x="500" y="55" class="text-sub" text-anchor="middle">Flask + Ollama (Qwen3:4b) on K3s Kubernetes with Argo CD</text>

  <!-- External Entities Tier -->
  <!-- Developer -->
  <rect x="40" y="90" width="160" height="70" class="box-dev" />
  <text x="120" y="120" class="text-title" text-anchor="middle">Developer</text>
  <text x="120" y="140" class="text-sub" text-anchor="middle">Git Push (main)</text>

  <!-- GitHub -->
  <rect x="260" y="90" width="180" height="70" class="box-dev" />
  <text x="350" y="120" class="text-title" text-anchor="middle">GitHub Repository</text>
  <text x="350" y="140" class="text-sub" text-anchor="middle">hasnainbanusi/ai-gitops</text>

  <!-- Browser -->
  <rect x="780" y="90" width="180" height="70" class="box-dev" />
  <text x="870" y="120" class="text-title" text-anchor="middle">User / Browser</text>
  <text x="870" y="140" class="text-sub" text-anchor="middle">HTTP Client Access</text>

  <!-- AWS EC2 Box -->
  <rect x="40" y="210" width="920" height="460" class="box-aws" />
  <text x="60" y="235" class="text-title" fill="#ff9900">AWS Cloud (EC2 Instance: Ubuntu 26.04 LTS)</text>

  <!-- Argo CD -->
  <rect x="70" y="260" width="200" height="100" class="box-argo" />
  <text x="170" y="295" class="text-title" fill="#ef7b4d" text-anchor="middle">Argo CD</text>
  <text x="170" y="315" class="text-sub" text-anchor="middle">GitOps Operator</text>
  <text x="170" y="335" class="text-sub" text-anchor="middle">Auto-Sync / Reconcile</text>

  <!-- K3s Cluster Box -->
  <rect x="300" y="260" width="630" height="380" class="box-k8s" />
  <text x="320" y="285" class="text-title" fill="#326ce5">K3s Kubernetes Cluster</text>

  <!-- Namespace Box -->
  <rect x="320" y="305" width="590" height="315" class="box-ns" />
  <text x="340" y="325" class="text-highlight">Namespace: ai-gitops</text>

  <!-- Flask NodePort Service -->
  <rect x="660" y="340" width="220" height="60" class="box-pod" />
  <text x="770" y="365" class="text-title" text-anchor="middle">ai-client-service</text>
  <text x="770" y="385" class="text-sub" text-anchor="middle">NodePort: 30601</text>

  <!-- Flask Pod -->
  <rect x="660" y="435" width="220" height="80" class="box-pod" />
  <text x="770" y="460" class="text-title" text-anchor="middle">ai-client Pod</text>
  <text x="770" y="480" class="text-sub" text-anchor="middle">Flask App (Port 5000)</text>

  <!-- Ollama ClusterIP Service -->
  <rect x="350" y="435" width="220" height="80" class="box-pod" />
  <text x="460" y="460" class="text-title" text-anchor="middle">ollama Service</text>
  <text x="460" y="480" class="text-sub" text-anchor="middle">ClusterIP (Port 11434)</text>

  <!-- Ollama Pod -->
  <rect x="350" y="540" width="220" height="65" class="box-pod" />
  <text x="460" y="565" class="text-title" text-anchor="middle">Ollama Pod</text>
  <text x="460" y="585" class="text-sub" text-anchor="middle">Qwen3:4b LLM Engine</text>

  <!-- PVC Storage -->
  <rect x="660" y="540" width="220" height="65" class="box-pvc" />
  <text x="770" y="565" class="text-title" fill="#d29922" text-anchor="middle">ollama-pvc</text>
  <text x="770" y="585" class="text-sub" text-anchor="middle">6Gi Persistent Storage</text>

  <!-- Arrows -->
  <!-- Dev to GitHub -->
  <path d="M 200 125 L 260 125" class="arrow" />
  
  <!-- GitHub to ArgoCD -->
  <path d="M 350 160 L 350 190 L 170 190 L 170 260" class="arrow-orange" />
  <text x="240" y="180" class="text-sub">Poll / Watch Sync</text>

  <!-- ArgoCD to Cluster -->
  <path d="M 270 310 L 300 310" class="arrow-orange" />

  <!-- Browser to NodePort -->
  <path d="M 870 160 L 870 340" class="arrow-green" />
  <text x="880" y="200" class="text-sub">EC2 IP:30601</text>

  <!-- NodePort to Flask Pod -->
  <path d="M 770 400 L 770 435" class="arrow-green" />

  <!-- Flask Pod to Ollama Service -->
  <path d="M 660 475 L 570 475" class="arrow" />
  <text x="615" y="465" class="text-sub" text-anchor="middle">HTTP API</text>

  <!-- Ollama Service to Ollama Pod -->
  <path d="M 460 515 L 460 540" class="arrow" />

  <!-- Ollama Pod to PVC -->
  <path d="M 570 572 L 660 572" class="arrow" stroke-dasharray="3" />
  <text x="615" y="565" class="text-sub" text-anchor="middle">Mounts</text>

</svg>

```

### 2. LinkedIn Optimized Architecture Diagram (Simplified)

```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="100%" height="100%">
  <defs>
    <style>
      .bg { fill: #0d1117; }
      .box { fill: #161b22; stroke: #30363d; stroke-width: 2; rx: 8px; }
      .box-k8s { fill: #0f2537; stroke: #326ce5; stroke-width: 2; rx: 10px; }
      .box-argo { fill: #2b1d1d; stroke: #ef7b4d; stroke-width: 2; rx: 8px; }
      .title { fill: #f0f6fc; font-family: Arial, sans-serif; font-weight: bold; font-size: 15px; }
      .sub { fill: #8b949e; font-family: Arial, sans-serif; font-size: 12px; }
      .arrow { stroke: #58a6ff; stroke-width: 2; fill: none; marker-end: url(#arrow); }
      .arrow-orange { stroke: #ef7b4d; stroke-width: 2; fill: none; marker-end: url(#arrow-o); }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#58a6ff"/>
    </marker>
    <marker id="arrow-o" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef7b4d"/>
    </marker>
  </defs>

  <rect width="800" height="450" class="bg" />

  <!-- Main Title -->
  <text x="400" y="30" class="title" font-size="18" text-anchor="middle">GitOps Automated AI Pipeline on Kubernetes</text>

  <!-- Flow Boxes -->
  <!-- 1. Dev & Git -->
  <rect x="40" y="70" width="160" height="80" class="box" />
  <text x="120" y="105" class="title" text-anchor="middle">GitHub Repo</text>
  <text x="120" y="125" class="sub" text-anchor="middle">Manifests (/k8s)</text>

  <!-- 2. Argo CD -->
  <rect x="250" y="70" width="160" height="80" class="box-argo" />
  <text x="330" y="105" class="title" fill="#ef7b4d" text-anchor="middle">Argo CD</text>
  <text x="330" y="125" class="sub" text-anchor="middle">Continuous Delivery</text>

  <!-- 3. Kubernetes Cluster -->
  <rect x="40" y="190" width="720" height="220" class="box-k8s" />
  <text x="60" y="215" class="title" fill="#326ce5">AWS EC2 / K3s Kubernetes Cluster</text>

  <!-- Inside K8s -->
  <!-- Flask App -->
  <rect x="80" y="240" width="260" height="140" class="box" />
  <text x="210" y="270" class="title" text-anchor="middle">Flask AI Client</text>
  <text x="210" y="295" class="sub" text-anchor="middle">NodePort Service (:30601)</text>
  <text x="210" y="320" class="sub" text-anchor="middle">UI &amp; API Gateway</text>

  <!-- Ollama + Qwen -->
  <rect x="460" y="240" width="260" height="140" class="box" />
  <text x="590" y="270" class="title" text-anchor="middle">Ollama + Qwen3:4b</text>
  <text x="590" y="295" class="sub" text-anchor="middle">ClusterIP Service (:11434)</text>
  <text x="590" y="320" class="sub" text-anchor="middle">Mounted 6Gi PVC Storage</text>

  <!-- Connectors -->
  <path d="M 200 110 L 250 110" class="arrow-orange" />
  <path d="M 330 150 L 330 190" class="arrow-orange" />
  <path d="M 340 310 L 460 310" class="arrow" />
  <text x="400" y="300" class="sub" text-anchor="middle">Internal API</text>

  <!-- External User Arrow -->
  <path d="M 600 70 L 600 150 L 210 150 L 210 240" class="arrow" stroke-dasharray="4" />
  <text x="400" y="140" class="sub" text-anchor="middle">User Access (Port 30601)</text>
</svg>

```
