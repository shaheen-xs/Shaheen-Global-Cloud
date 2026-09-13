variable "project_name" {
  description = "Project name"
  type        = string
  default     = "shaheen-global-cloud"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "vm_name" {
  description = "Name of the VM to provision"
  type        = string
  default     = "shaheen-vm-01"
}

variable "hostname" {
  description = "Hostname for the VM"
  type        = string
  default     = "vm-01.shaheen.cloud"
}

variable "plan" {
  description = "Server plan"
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
