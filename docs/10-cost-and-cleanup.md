# 10 — AWS cost model and cleanup checklist

AWS charges can continue when a laptop or CloudShell session is closed. This lab used resources that may incur continuous hourly charges.

## Review these cost centers

| Resource | Why it may cost money |
|---|---|
| EKS control plane | Managed cluster charge |
| EC2 worker instances | Running node-group capacity |
| EBS volumes | Persistent instance storage |
| NAT gateways | Hourly plus data processing charges |
| Elastic Load Balancers | If any are left provisioned |
| ECR | Stored image bytes and some transfer activity |
| Public IPv4 addresses | Current applicable charges |
| CloudWatch/logging | Log ingestion/storage if enabled |

Prices and policies vary by region/date. Check the AWS Billing Console and current pricing pages for your account; no exact monthly spend is asserted here.

## Before teardown

1. Record final Git and screenshot evidence.
2. Check namespaces, Deployments, Services, Ingresses and PVCs.
3. Check whether any external load balancers or volumes were created by Kubernetes controllers.
4. Inspect ECR images, cluster node groups and NAT gateways.
5. Identify resources shared with other labs; **do not delete a shared VPC or IAM role blindly**.
6. Take any needed backup or export before removing material state.
7. Delete only positively identified task resources, in an order appropriate to controller dependencies.
8. Recheck the AWS Console and billing view afterward.

The earlier user screenshots did not establish final resource deletion, so the portfolio makes **no claim that costs have stopped**.

## Security/cost overlap

An unrestricted public API endpoint or lingering IAM credentials increases risk even when the cluster is only a lab. Shut down unneeded compute and secure credentials independently.
