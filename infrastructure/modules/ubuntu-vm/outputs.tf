output "vm_id" {
  description = "ID of the provisioned VM"
  value       = null_resource.vm.id
}

output "vm_name" {
  description = "Name of the VM"
  value       = var.vm_name
}

output "hostname" {
  description = "Hostname of the VM"
  value       = var.hostname
}

output "plan" {
  description = "Server plan"
  value       = var.plan
}

output "region" {
  description = "Deployment region"
  value       = var.region
}

output "image" {
  description = "OS image"
  value       = var.image
}

output "cpu_cores" {
  description = "Allocated vCPU cores"
  value       = var.cpu_cores
}

output "memory_mb" {
  description = "Allocated memory in MB"
  value       = var.memory_mb
}

output "disk_gb" {
  description = "Allocated disk in GB"
  value       = var.disk_gb
}
