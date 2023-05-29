# project-23-dont-remember

# Deployment
begin deploy
```
terraform apply -var-file="secret.tfvars" -auto-approve
terraform apply -var-file="secret.tfvars" -auto-approve -parallelism=20
```

