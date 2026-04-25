###############################################################################
#  CashMe — VM única (EC2 + EIP + SG + KeyPair)
#
#  AMI: Ubuntu 24.04 LTS (Noble) ARM64, resolvida via SSM Parameter Store
#       para sempre pegar a mais recente publicada pela Canonical.
###############################################################################

# ── AMI Ubuntu 24.04 ARM ──────────────────────────────────────────────────────
data "aws_ssm_parameter" "ubuntu_2404_arm64" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/arm64/hvm/ebs-gp3/ami-id"
}

# ── Default VPC / Subnet (suficiente para 1 VM) ──────────────────────────────
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ── KeyPair ───────────────────────────────────────────────────────────────────
resource "aws_key_pair" "cashme" {
  key_name   = "${var.project_name}-ops"
  public_key = file(pathexpand(var.ssh_public_key_path))
}

# ── Security Group ───────────────────────────────────────────────────────────
locals {
  panel_ports = var.open_panel_ports ? [
    8000, # app direto
    3000, # langfuse
    3001, # grafana
    9090, # prometheus
    3100, # loki
    3200, # tempo
    8001, # chromadb
    5540, # redisinsight
    3500, # chroma-admin
    6006, # phoenix
    5500, # mlflow
    8888, # jupyter
  ] : []
}

resource "aws_security_group" "cashme" {
  name        = "${var.project_name}-sg"
  description = "Security group da VM CashMe"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
  }

  ingress {
    description = "HTTP via Caddy (Basic-Auth)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  dynamic "ingress" {
    for_each = local.panel_ports
    content {
      description = "Painel direto :${ingress.value}"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# ── EC2 Instance ─────────────────────────────────────────────────────────────
resource "aws_instance" "cashme" {
  ami                         = data.aws_ssm_parameter.ubuntu_2404_arm64.value
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.cashme.id]
  key_name                    = aws_key_pair.cashme.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_disk_gb
    delete_on_termination = true
    encrypted             = true
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required" # IMDSv2
  }

  user_data = <<-EOT
    #!/bin/bash
    set -euo pipefail
    apt-get update -y
    apt-get install -y python3 sudo

    if ! id -u ${var.ssh_user} >/dev/null 2>&1; then
      useradd -m -s /bin/bash ${var.ssh_user}
      usermod -aG sudo ${var.ssh_user}
      echo "${var.ssh_user} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-${var.ssh_user}
      chmod 0440 /etc/sudoers.d/90-${var.ssh_user}
      mkdir -p /home/${var.ssh_user}/.ssh
      chmod 700 /home/${var.ssh_user}/.ssh
      cp /home/ubuntu/.ssh/authorized_keys /home/${var.ssh_user}/.ssh/authorized_keys
      chown -R ${var.ssh_user}:${var.ssh_user} /home/${var.ssh_user}/.ssh
      chmod 600 /home/${var.ssh_user}/.ssh/authorized_keys
    fi

    mkdir -p /srv/${var.project_name}/{repo,volumes}
    chown -R ${var.ssh_user}:${var.ssh_user} /srv/${var.project_name}
  EOT

  tags = {
    Name = "${var.project_name}-vm"
  }

  lifecycle {
    ignore_changes = [ami] # não recria a VM quando a Canonical publica nova AMI
  }
}

# ── Elastic IP ────────────────────────────────────────────────────────────────
resource "aws_eip" "cashme" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

resource "aws_eip_association" "cashme" {
  instance_id   = aws_instance.cashme.id
  allocation_id = aws_eip.cashme.id
}
