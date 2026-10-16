# Terraform: AWS VPC + EKS for TaskBoard

Infrastructure as Code for the production-style home of the application: a VPC (two public, two private subnets, one NAT gateway) and an EKS cluster with one managed node group. Kubernetes manages the workloads; Terraform manages what Kubernetes runs on.

> Cost warning: EKS (control plane), the NAT gateway and the worker nodes bill by the hour. Run `terraform destroy` when you are finished.

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # optional overrides
terraform init
terraform fmt -recursive
terraform validate
terraform plan                                  # needs AWS credentials (aws configure / env vars)
terraform apply
aws eks update-kubeconfig --region ap-south-1 --name taskboard-eks
kubectl get nodes
terraform destroy
```

Files: `versions.tf` (Terraform and provider versions, default tags), `variables.tf`, `main.tf` (VPC and EKS modules), `outputs.tf`, `terraform.tfvars.example`.
