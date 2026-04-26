variable "project_name" {
  description = "Prefixo aplicado a todos os recursos."
  type        = string
  default     = "cashme"
}

variable "region" {
  description = "Região AWS de deploy."
  type        = string
  default     = "sa-east-1"
}

variable "aws_profile" {
  description = "Perfil do AWS CLI a usar (configurado via `aws configure --profile ...`)."
  type        = string
  default     = "cashme-ops"
}

variable "instance_type" {
  description = "Tipo da EC2 (ARM por padrão para usar a AMI t4g)."
  type        = string
  default     = "t4g.large"
}

variable "root_disk_gb" {
  description = "Tamanho do volume root EBS (gp3) em GB."
  type        = number
  default     = 60
}

variable "ssh_public_key_path" {
  description = "Caminho do arquivo da chave SSH pública a importar."
  type        = string
  default     = "~/.ssh/cashme-ops-ed25519.pub"
}

variable "allowed_ssh_cidrs" {
  description = "CIDRs autorizados a SSH. Default = mundo (somente chave permite login). Restrinja para o seu IP em prod real."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "open_panel_ports" {
  description = "Se true, abre portas diretas dos painéis (8000, 3000, 3001, 9090, etc.) sem passar pelo Caddy. Recomendado: false."
  type        = bool
  default     = false
}

variable "ssh_user" {
  description = "Usuário Linux criado na VM (recebe a chave SSH)."
  type        = string
  default     = "cashme"
}
