output "instance_id" {
  description = "ID da EC2."
  value       = aws_instance.homeequity.id
}

output "public_ip" {
  description = "Elastic IP fixo associado à VM."
  value       = aws_eip.homeequity.public_ip
}

output "public_dns" {
  description = "DNS público da EC2 (muda se o EIP for trocado)."
  value       = aws_instance.homeequity.public_dns
}

output "ssh_user" {
  value = var.ssh_user
}

output "ssh_command" {
  description = "Comando para conectar via SSH."
  value       = "ssh -i ${var.ssh_public_key_path == "~/.ssh/homeequity-ops-ed25519.pub" ? "~/.ssh/homeequity-ops-ed25519" : replace(var.ssh_public_key_path, ".pub", "")} ${var.ssh_user}@${aws_eip.homeequity.public_ip}"
}

output "app_url" {
  description = "URL pública da aplicação (Caddy + Basic-Auth)."
  value       = "http://${aws_eip.homeequity.public_ip}/"
}
