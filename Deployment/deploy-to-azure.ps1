# Azure App Service Deployment Script for Public Welfare Assistant
# This script deploys the FastAPI backend to Azure App Service using Docker containers

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$AppServiceName,
    
    [Parameter(Mandatory=$true)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$false)]
    [string]$ContainerRegistryName,
    
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId
)

Write-Host "🚀 Starting Azure App Service Deployment for Public Welfare Assistant" -ForegroundColor Green

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Login to Azure (if not already logged in)
Write-Host "🔐 Checking Azure login status..." -ForegroundColor Yellow
$loginStatus = az account show 2>$null
if (-not $loginStatus) {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Set subscription if provided
if ($SubscriptionId) {
    Write-Host "📋 Setting subscription to: $SubscriptionId" -ForegroundColor Yellow
    az account set --subscription $SubscriptionId
}

# Get current subscription info
$currentSub = az account show --output json | ConvertFrom-Json
Write-Host "📋 Using subscription: $($currentSub.name) ($($currentSub.id))" -ForegroundColor Cyan

# Step 1: Create Resource Group
Write-Host "📦 Creating Resource Group: $ResourceGroupName" -ForegroundColor Yellow
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "false") {
    az group create --name $ResourceGroupName --location $Location
    Write-Host "✅ Resource Group created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Resource Group already exists" -ForegroundColor Green
}

# Step 2: Create Container Registry (if name provided)
if ($ContainerRegistryName) {
    Write-Host "🐳 Creating Azure Container Registry: $ContainerRegistryName" -ForegroundColor Yellow
    $acrExists = az acr show --name $ContainerRegistryName --resource-group $ResourceGroupName 2>$null
    if (-not $acrExists) {
        az acr create --name $ContainerRegistryName --resource-group $ResourceGroupName --sku Basic --admin-enabled true
        Write-Host "✅ Container Registry created successfully" -ForegroundColor Green
    } else {
        Write-Host "✅ Container Registry already exists" -ForegroundColor Green
    }
    
    # Get ACR credentials
    $acrServer = az acr show --name $ContainerRegistryName --resource-group $ResourceGroupName --query "loginServer" --output tsv
    $acrUsername = az acr credential show --name $ContainerRegistryName --resource-group $ResourceGroupName --query "username" --output tsv
    $acrPassword = az acr credential show --name $ContainerRegistryName --resource-group $ResourceGroupName --query "passwords[0].value" --output tsv
    
    Write-Host "🔑 ACR Details:" -ForegroundColor Cyan
    Write-Host "  Server: $acrServer" -ForegroundColor White
    Write-Host "  Username: $acrUsername" -ForegroundColor White
    Write-Host "  Password: [HIDDEN]" -ForegroundColor White
}

# Step 3: Create App Service Plan
$appServicePlanName = "$AppServiceName-plan"
Write-Host "🏗️ Creating App Service Plan: $appServicePlanName" -ForegroundColor Yellow
$planExists = az appservice plan show --name $appServicePlanName --resource-group $ResourceGroupName 2>$null
if (-not $planExists) {
    az appservice plan create --name $appServicePlanName --resource-group $ResourceGroupName --is-linux --sku B1
    Write-Host "✅ App Service Plan created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ App Service Plan already exists" -ForegroundColor Green
}

# Step 4: Create Web App
Write-Host "🌐 Creating Web App: $AppServiceName" -ForegroundColor Yellow
$webAppExists = az webapp show --name $AppServiceName --resource-group $ResourceGroupName 2>$null
if (-not $webAppExists) {
    if ($ContainerRegistryName) {
        # Deploy with custom container
        az webapp create --name $AppServiceName --resource-group $ResourceGroupName --plan $appServicePlanName --deployment-container-image-name "$acrServer/public-welfare-assistant:latest"
    } else {
        # Deploy with Docker Hub image (using our local image name)
        az webapp create --name $AppServiceName --resource-group $ResourceGroupName --plan $appServicePlanName --deployment-container-image-name "my-fastapi-app:latest"
    }
    Write-Host "✅ Web App created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Web App already exists" -ForegroundColor Green
}

# Step 5: Configure Container Registry credentials (if using ACR)
if ($ContainerRegistryName) {
    Write-Host "🔐 Configuring container registry credentials..." -ForegroundColor Yellow
    az webapp config container set --name $AppServiceName --resource-group $ResourceGroupName --docker-custom-image-name "$acrServer/public-welfare-assistant:latest" --docker-registry-server-url "https://$acrServer" --docker-registry-server-user $acrUsername --docker-registry-server-password $acrPassword
}

# Step 6: Configure App Settings (Environment Variables)
Write-Host "⚙️ Configuring application settings..." -ForegroundColor Yellow

# Read environment variables from .env file if it exists
$envFile = ".env"
if (Test-Path $envFile) {
    Write-Host "📄 Reading environment variables from $envFile" -ForegroundColor Cyan
    $envVars = @()
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $envVars += "$key=$value"
        }
    }
    
    if ($envVars.Count -gt 0) {
        az webapp config appsettings set --name $AppServiceName --resource-group $ResourceGroupName --settings $envVars
        Write-Host "✅ Environment variables configured" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️ No .env file found. You'll need to configure environment variables manually in the Azure portal." -ForegroundColor Yellow
    Write-Host "Required variables:" -ForegroundColor White
    Write-Host "  - DATABASE_SERVER" -ForegroundColor White
    Write-Host "  - DATABASE_NAME" -ForegroundColor White
    Write-Host "  - DATABASE_USERNAME" -ForegroundColor White
    Write-Host "  - DATABASE_PASSWORD" -ForegroundColor White
    Write-Host "  - AZURE_OPENAI_ENDPOINT" -ForegroundColor White
    Write-Host "  - AZURE_OPENAI_API_KEY" -ForegroundColor White
    Write-Host "  - AZURE_SPEECH_KEY" -ForegroundColor White
    Write-Host "  - AZURE_SPEECH_REGION" -ForegroundColor White
}

# Step 7: Configure startup settings
Write-Host "🔧 Configuring startup settings..." -ForegroundColor Yellow
az webapp config set --name $AppServiceName --resource-group $ResourceGroupName --startup-file "uvicorn main:app --host 0.0.0.0 --port 8000"

# Step 8: Enable logging
Write-Host "📊 Enabling application logging..." -ForegroundColor Yellow
az webapp log config --name $AppServiceName --resource-group $ResourceGroupName --application-logging filesystem --level information

# Step 9: Get deployment information
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
$webAppInfo = az webapp show --name $AppServiceName --resource-group $ResourceGroupName --output json | ConvertFrom-Json
$webAppUrl = "https://$($webAppInfo.defaultHostName)"

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your app is available at: $webAppUrl" -ForegroundColor Green
Write-Host "📚 API Documentation: $webAppUrl/docs" -ForegroundColor Green
Write-Host "❤️ Health Check: $webAppUrl/health" -ForegroundColor Green
Write-Host ""
Write-Host "🔍 To monitor your app:" -ForegroundColor Yellow
Write-Host "  az webapp log tail --name $AppServiceName --resource-group $ResourceGroupName" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Configure custom domain (optional)" -ForegroundColor White
Write-Host "  2. Enable SSL certificate" -ForegroundColor White
Write-Host "  3. Set up monitoring and alerts" -ForegroundColor White
Write-Host "  4. Configure CI/CD pipeline" -ForegroundColor White

# Optional: Open the app in browser
$openInBrowser = Read-Host "Would you like to open the app in your browser? (y/n)"
if ($openInBrowser -eq "y" -or $openInBrowser -eq "Y") {
    Start-Process $webAppUrl
}
