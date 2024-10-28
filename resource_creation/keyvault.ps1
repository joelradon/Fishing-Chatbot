# Step 1: Deploy OpenAI Model (Azure OpenAI Setup)
# If you are using Azure OpenAI, you do not need to "deploy" the model in the traditional sense like custom ML models. However, you need to create an Azure OpenAI resource.
# After creating the Azure OpenAI resource, you will have access to API keys and endpoints to use in your app.

# Step 2: Create an Azure Key Vault and Store Secrets
# Use Azure CLI to create a Key Vault and store the necessary secrets securely.

# Set up variables for easy reuse
$RESOURCE_GROUP="FishingBot-RG"
$LOCATION="eastus"
$KEY_VAULT_NAME="FishingBot"

# Create a resource group (if not already created)
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create an Azure Key Vault
az keyvault create --name $KEY_VAULT_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# Assign Key Vault Secrets Officer role to the current user
CURRENT_USER=$(az account show --query user.name -o tsv)
az role assignment create --role "Key Vault Secrets Officer" --assignee $CURRENT_USER --scope /subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEY_VAULT_NAME

# Store the secrets in the Key Vault
# Note: Azure Key Vault doesn't support underscores in secret names, so we use dashes instead.

# Storing Telegram Bot API Token
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "TELEGRAM-API-TOKEN" --value "YOUR_TELEGRAM_BOT_API_TOKEN"

# Storing Azure Custom Question Answering Endpoint and API Key
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "CQA-ENDPOINT" --value "YOUR_CQA_ENDPOINT"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "CQA-API-KEY" --value "YOUR_CQA_API_KEY"

# Storing Azure OpenAI Endpoint and API Key
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "OPENAI-ENDPOINT" --value "YOUR_OPENAI_ENDPOINT"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "OPENAI-API-KEY" --value "YOUR_OPENAI_API_KEY"

# Step 3: Access Secrets in Your Python Script
# Update your Python script to retrieve the secrets from Azure Key Vault instead of hardcoding them.
# You can use Azure SDK for Python (`azure-identity` and `azure-keyvault-secrets` libraries) to achieve this.
