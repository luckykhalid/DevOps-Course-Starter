terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
  backend "azurerm" {
    resource_group_name  = "OpenCohort1_KhalidAshraf_ProjectExercise"
    storage_account_name = "tfstate28504"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "OpenCohort1_KhalidAshraf_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-todo-app-v2"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|khalidashraf/todo_app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "SECRET_KEY"                 = "${var.secret_key}"
    "MONGODB_CONNECTION_STRING"  = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "OAUTH_CLIENT_ID"            = "${var.oauth_client_id}"
    "OAUTH_CLIENT_SECRET"        = "${var.oauth_client_secret}"
    "OAUTH_AUTHENTICATE_URL"     = "${var.oauth_authenticate_url}"
    "OAUTH_ACCESS_TOKEN_URL"     = "${var.oauth_access_token_url}"
    "OAUTH_USER_URL"             = "${var.oauth_user_url}"
    "ROLE_WRITER_USERS"          = "${var.role_writer_users}"
  }
}

data "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-devops"
  resource_group_name = data.azurerm_resource_group.main.name
  #capabilities { name = "EnableServerless" }
  #capabilities { name = "EnableMongo" }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "devops"
  resource_group_name = data.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.main.name
  lifecycle { prevent_destroy = true }
}
