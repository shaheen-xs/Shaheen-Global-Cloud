variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
}

variable "hostname" {
  description = "Hostname for the VM"
  type        = string
}

variable "plan" {
  description = "Server plan (micro, small, medium, large, xlarge)"
  type        = string
  default     = "small"
}

variable "region" {
  description = "Deployment region"
  type        = string
  default     = "us-east-1"
}

variable "image" {
  description = "OS image"
  type        = string
  default     = "ubuntu-24.04"
}

variable "cpu_cores" {
  description = "Number of vCPU cores"
  type        = number
  default     = 2
}

variable "memory_mb" {
  description = "Memory in MB"
  type        = number
  default     = 2048
}

variable "disk_gb" {
  description = "Disk size in GB"
  type        = number
  default     = 40
}

variable "tags" {
  description = "Tags to apply to the VM"
  type        = map(string)
  default     = {}
}
