###############################################################################
#  Equity — VM única (EC2 + EIP + SG + KeyPair)
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
resource "aws_key_pair" "homeequity" {
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

resource "aws_security_group" "homeequity" {
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
    description = "HTTP via Caddy (redirect to HTTPS / Basic-Auth)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS via Caddy (TLS Lets Encrypt DNS-01)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP/3 (QUIC) via Caddy"
    from_port   = 443
    to_port     = 443
    protocol    = "udp"
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

  lifecycle {
    # 'name' é ForceNew: sem isto o destroy do SG antigo falha por ainda estar
    # anexado à ENI da instância (DependencyViolation).
    create_before_destroy = true
  }
}

# ── EC2 Instance ─────────────────────────────────────────────────────────────
resource "aws_instance" "homeequity" {
  ami                         = data.aws_ssm_parameter.ubuntu_2404_arm64.value
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.homeequity.id]
  key_name                    = aws_key_pair.homeequity.key_name
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
    # Atributos ForceNew (ou que disparam stop/start) cujo valor mudou quando o
    # projeto foi renomeado de 'cashme' para 'homeequity'. Sem isto, um apply
    # DESTRÓI a instância e o disco de 60 GB junto:
    #   ami       — Canonical publica AMI nova periodicamente
    #   user_data — interpola project_name e ssh_user; já foi aplicado no boot original
    #   key_name  — a key pair passou a se chamar homeequity-ops
    #   subnet_id — vem de data.aws_subnets.default.ids[0], cuja ordem a API não garante
    ignore_changes = [ami, user_data, key_name, subnet_id]
  }
}

# ── Elastic IP ────────────────────────────────────────────────────────────────
resource "aws_eip" "homeequity" {
  domain = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}

resource "aws_eip_association" "homeequity" {
  instance_id   = aws_instance.homeequity.id
  allocation_id = aws_eip.homeequity.id
}
