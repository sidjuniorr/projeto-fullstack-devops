provider "docker" {}

resource "null_resource" "kind_cluster" {
  provisioner "local-exec" {
    command = <<EOT
      if ! kind get clusters | grep -q "^fullstack-cluster$"; then
        kind create cluster --name fullstack-cluster --config=../kind-config.yaml
      else
        echo "Cluster 'fullstack-cluster' já existe. Ignorando criação."
      fi
    EOT
  }

  triggers = {
    always_run = timestamp()
  }
}
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}
