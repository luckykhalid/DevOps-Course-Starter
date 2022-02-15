output "webapp_url" {
  value = "https://${azurerm_app_service.main.default_site_hostname}"
}

output "webhook_url" {
  value = "https://${azurerm_app_service.main.site_credential[0].username}:${azurerm_app_service.main.site_credential[0].password}@${azurerm_app_service.main.name}.scm.azurewebsites.net/docker/hook"
  sensitive   = true
}
