variable "prefix" {
  description = "The prefix used for all resources in this environment"
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}
variable "oauth_client_id" {
  description = "OAUTH CLIENT ID"
}
variable "oauth_client_secret" {
  description = "OAUTH CLIENT SECRET"
}
variable "secret_key" {
  description = "SECRET KEY"
}

variable "oauth_authenticate_url"{
  description = "OAUTH AUTHENTICATE URL"
}    

variable "oauth_access_token_url"{
  description = "OAUTH ACCESS TOKEN URL"
} 

variable "oauth_user_url"{
  description = "OAUTH USER URL"
} 

variable "role_writer_users"{
  description = "ROLE WRITER USERS"
} 

