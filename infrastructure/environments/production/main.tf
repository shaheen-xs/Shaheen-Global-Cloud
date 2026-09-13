terraform {
  required_version = ">= 1.6.0"
}

module "ubuntu_vm" {
  source = "../../modules/ubuntu-vm"

  vm_name   = var.vm_name
  hostname  = var.hostname
  plan      = var.plan
  region    = var.region
  image     = var.image

  cpu_cores = var.plan == "micro" ? 1 : var.plan == "small" ? 2 : var.plan == "medium" ? 4 : var.plan == "large" ? 8 : 16
  memory_mb = var.plan == "micro" ? 1024 : var.plan == "small" ? 2048 : var.plan == "medium" ? 4096 : var.plan == "large" ? 8192 : 16384
  disk_gb   = var.plan == "micro" ? 20 : var.plan == "small" ? 40 : var.plan == "medium" ? 80 : var.plan == "large" ? 160 : 320

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "shaheen-global-cloud"
  }
}
