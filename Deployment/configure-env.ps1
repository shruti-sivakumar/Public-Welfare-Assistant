# Environment Configuration Script for Azure Deployment
# This script helps you set up environment variables for your Azure App Service

Write-Host " Environment Configuration for Public Welfare Assistant" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

$APP_NAME = Read-Host "Enter your App Service name (e.g., welfare-assistant-api-123)"
$RESOURCE_GROUP = Read-Host "Enter your Resource Group name (default: welfare-assistant-rg)" 
if ([string]::IsNullOrEmpty($RESOURCE_GROUP)) { $RESOURCE_GROUP = "welfare-assistant-rg" }

Write-Host ""
Write-Host " Setting up environment variables for: $APP_NAME" -ForegroundColor Yellow
Write-Host ""

# Database Configuration
Write-Host " Database Configuration:" -ForegroundColor Cyan
$DB_SERVER = Read-Host "Azure SQL Server name (e.g., myserver.database.windows.net)"
$DB_NAME = Read-Host "Database name (default: WelfareDB)"
if ([string]::IsNullOrEmpty($DB_NAME)) { $DB_NAME = "WelfareDB" }
$DB_USERNAME = Read-Host "Database username"
$DB_PASSWORD = Read-Host "Database password" -AsSecureString
$DB_PASSWORD_TEXT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($DB_PASSWORD))

Write-Host ""

# Azure OpenAI Configuration
Write-Host " Azure OpenAI Configuration:" -ForegroundColor Cyan
$OPENAI_ENDPOINT = Read-Host "Azure OpenAI endpoint (e.g., https://myopenai.openai.azure.com/)"
$OPENAI_KEY = Read-Host "Azure OpenAI API key" -AsSecureString
$OPENAI_KEY_TEXT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($OPENAI_KEY))
$OPENAI_DEPLOYMENT = Read-Host "OpenAI deployment name (default: gpt-4)"
if ([string]::IsNullOrEmpty($OPENAI_DEPLOYMENT)) { $OPENAI_DEPLOYMENT = "gpt-4" }

Write-Host ""

# Azure Speech Configuration
Write-Host " Azure Speech Configuration:" -ForegroundColor Cyan
$SPEECH_KEY = Read-Host "Azure Speech API key" -AsSecureString
$SPEECH_KEY_TEXT = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($SPEECH_KEY))
$SPEECH_REGION = Read-Host "Azure Speech region (e.g., eastus)"

Write-Host ""

# Application Settings
Write-Host " Application Settings:" -ForegroundColor Cyan
$SECRET_KEY = Read-Host "Application secret key (or press Enter for auto-generated)"
if ([string]::IsNullOrEmpty($SECRET_KEY)) { 
    $SECRET_KEY = [System.Web.Security.Membership]::GeneratePassword(32, 8)
    Write-Host "Generated secret key: $SECRET_KEY" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Applying configuration to Azure App Service..." -ForegroundColor Yellow

try {
    # Set all environment variables at once
    az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings `
        "DATABASE_SERVER=$DB_SERVER" `
        "DATABASE_NAME=$DB_NAME" `
        "DATABASE_USERNAME=$DB_USERNAME" `
        "DATABASE_PASSWORD=$DB_PASSWORD_TEXT" `
        "AZURE_OPENAI_ENDPOINT=$OPENAI_ENDPOINT" `
        "AZURE_OPENAI_API_KEY=$OPENAI_KEY_TEXT" `
        "AZURE_OPENAI_API_VERSION=2024-02-15-preview" `
        "AZURE_OPENAI_DEPLOYMENT_NAME=$OPENAI_DEPLOYMENT" `
        "AZURE_SPEECH_KEY=$SPEECH_KEY_TEXT" `
        "AZURE_SPEECH_REGION=$SPEECH_REGION" `
        "SECRET_KEY=$SECRET_KEY" `
        "DEBUG=false" `
        "ENVIRONMENT=production" `
        --output none

    Write-Host " Environment variables configured successfully!" -ForegroundColor Green
    
    # Restart the app to apply changes
    Write-Host " Restarting app to apply changes..." -ForegroundColor Yellow
    az webapp restart --name $APP_NAME --resource-group $RESOURCE_GROUP --output none
    Write-Host " App restarted successfully!" -ForegroundColor Green
    
    # Get app URL
    $appUrl = az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query "defaultHostName" --output tsv
    $fullUrl = "https://$appUrl"
    
    Write-Host ""
    Write-Host " Configuration completed!" -ForegroundColor Green
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host " Your app: $fullUrl" -ForegroundColor Green
    Write-Host " API Docs: $fullUrl/docs" -ForegroundColor Green
    Write-Host " Health: $fullUrl/health" -ForegroundColor Green
    Write-Host ""
    Write-Host " Please wait 2-3 minutes for the app to fully restart" -ForegroundColor Yellow
    Write-Host ""
    
    # Save configuration to local file for reference
    $configContent = @"
# Azure App Service Configuration
# Generated on $(Get-Date)

App Name: $APP_NAME
Resource Group: $RESOURCE_GROUP
App URL: $fullUrl

Environment Variables Configured:
✅ DATABASE_SERVER=$DB_SERVER
✅ DATABASE_NAME=$DB_NAME  
✅ DATABASE_USERNAME=$DB_USERNAME
✅ DATABASE_PASSWORD=[CONFIGURED]
✅ AZURE_OPENAI_ENDPOINT=$OPENAI_ENDPOINT
✅ AZURE_OPENAI_API_KEY=[CONFIGURED]
✅ AZURE_SPEECH_KEY=[CONFIGURED]
✅ AZURE_SPEECH_REGION=$SPEECH_REGION
✅ SECRET_KEY=[CONFIGURED]

To view logs:
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP

To update container image:
az webapp config container set --name $APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name my-fastapi-app:latest
"@
    
    $configContent | Out-File -FilePath "azure-deployment-config.txt" -Encoding UTF8
    Write-Host " Configuration saved to: azure-deployment-config.txt" -ForegroundColor Cyan
    
    $openApp = Read-Host "Would you like to open the app now? (y/n)"
    if ($openApp -eq "y" -or $openApp -eq "Y") {
        Start-Process $fullUrl
    }

} catch {
    Write-Host ""
    Write-Host " Configuration failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host " You can configure these manually in Azure Portal:" -ForegroundColor Yellow
    Write-Host "1. Go to portal.azure.com" -ForegroundColor White
    Write-Host "2. Navigate to App Services → $APP_NAME" -ForegroundColor White
    Write-Host "3. Go to Configuration → Application Settings" -ForegroundColor White
    Write-Host "4. Add each environment variable manually" -ForegroundColor White
}