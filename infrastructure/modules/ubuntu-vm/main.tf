terraform {
  required_version = ">= 1.6.0"
}

# Mock provider for Phase 1 — no real cloud resources are created.
# This resource simulates a VM for local development and testing.

resource "null_resource" "vm" {
  triggers = {
    name      = var.vm_name
    hostname  = var.hostname
    plan      = var.plan
    region    = var.region
    image     = var.image
    cpu_cores = var.cpu_cores
    memory_mb = var.memory_mb
    disk_gb   = var.disk_gb
  }

  provisioner "local-exec" {
    command = "echo '[MOCK] Provisioning ${var.vm_name} (${var.plan}) in ${var.region} with ${var.image}'"
  }
}
