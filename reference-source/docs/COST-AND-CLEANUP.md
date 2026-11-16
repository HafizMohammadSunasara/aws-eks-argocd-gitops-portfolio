# AWS cost, security and cleanup checklist

## Before creating any AWS resources

- [ ] Confirm region and account.
- [ ] Estimate hourly costs for the EKS control plane, two EC2 workers, EBS volumes, NAT Gateway/data transfer, public NLB, public IPv4, and ECR storage/scanning.
- [ ] Create AWS Budgets cost alerts. Alerts notify; they do not automatically shut down resources.
- [ ] Decide how long the lab may run, and set a reminder to clean up.
- [ ] Restrict GitHub OIDC trust to the single repository and `main` branch.
- [ ] Keep worker nodes in private subnets; separate IAM roles and prefer the least privilege practical.
- [ ] Do not commit access tokens, passwords, SSH keys, kubeconfig, `.env` files, or real AWS account secrets.

## After the demonstration (manual cleanup, in dependency order)

1. Save non-sensitive screenshots, manifests and test results needed for your portfolio.
2. Remove the Argo CD-managed public NLB Service and **confirm the AWS Load Balancer is deleted**. Watch for stuck Kubernetes Service finalizers rather than forcing deletion immediately.
3. Remove remaining demo workloads and Argo CD Application as appropriate; confirm any dynamically created load balancers and target groups are gone.
4. Delete the managed EKS node group, then the EKS cluster; wait for completion.
5. Delete remaining NAT Gateway, release unused Elastic IP, and remove VPC network resources only after verifying dependencies.
6. Review ECR images/repository, unattached EBS volumes, CloudWatch log groups and other paid resources.
7. Check AWS Billing/Cost Explorer the next day for continuing charges.

**Never use a broad wildcard deletion command.** Confirm exact names, account and region before deleting resources.

## Honest portfolio scope

This starter is not production-ready. Production work would add TLS/HTTPS and DNS, private ingress where appropriate, strict IAM and network policy, vulnerability scanning/policy enforcement, alerting/SLOs, higher availability for outbound NAT, multi-environment approvals, and recovery plans.
