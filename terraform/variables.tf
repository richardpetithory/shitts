variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-east-1"
}

# networking

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1b", "us-east-1c"]
}

# load balancer

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/ping/"
}

# logs

variable "log_retention_in_days" {
  default = 30
}

# ecs

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "production"
}

variable "docker_image_url_shitts" {
  description = "Docker image to run in the ECS cluster"
  default     = "939548766794.dkr.ecr.us-west-1.amazonaws.com/shitts-app:latest"
}

variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 2
}

variable "fargate_cpu" {
  description = "Amount of CPU for Fargate task. E.g., '256' (.25 vCPU)"
  default     = "256"
}

variable "fargate_memory" {
  description = "Amount of memory for Fargate task. E.g., '512' (0.5GB)"
  default     = "512"
}
