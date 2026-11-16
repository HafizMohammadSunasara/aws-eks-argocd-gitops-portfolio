# 11 — Engineering lessons, not a generic technology list

## 1. Correct ownership makes debugging easier

When a CI build passed but the browser hadn't changed yet, the right question was not 'Did GitHub Actions fail?' but 'Where is the new desired image in the chain?' The image can be in ECR while Git still points at the previous SHA. Argo CD can also be waiting on Git and Kubernetes can be waiting on Pod readiness.

## 2. A PR is useful release metadata

The automated promotion PR records what image is requested and who merged it. The [final PR #3](https://github.com/HafizMohammadSunasara/aws-eks-argocd-gitops/pull/3) is as important as the green runner screenshot because it connects an image to a release decision.

## 3. A skipped job can mean policy worked

The ECR publishing job was intentionally gated on a \`push\`. A successful pull-request workflow that skips publish is not a failed pipeline. Understanding event conditions avoided a false diagnosis.

## 4. 'Authenticated' is not 'authorized'

The AWS CLI returned an identity, but one Kubernetes Service request was forbidden. EKS access and Kubernetes RBAC are separate systems. The lesson is to inspect the precise verb/resource/namespace before broadening any role.

## 5. The workstation can fail while EKS is fine

The Windows 8080 binding error was local. Switching to 18080 allowed Argo CD access. Nothing in that specific error proved the cluster was unhealthy.

## 6. Healthy is not production-ready

Two Ready nodes and healthy Pods validate a lab. They do not establish guaranteed spread, disaster recovery, public HTTPS, performance under load or tested rollback. Engineering maturity includes accurate labels for those missing pieces.

## 7. Security mistakes belong in lessons learned

An earlier terminal screenshot exposed credentials. Publication hygiene means excluding that evidence and rotating secrets; a portfolio should not normalize leaked keys just because a terminal screenshot looks impressive.

## The strongest demonstration

A visible Version 2 heading, attached to the source change, an image-promotion PR, Argo CD status and a new Pod, provides a coherent story that can be independently questioned and verified.
