# Azure Container Instances Deployment Script for Streamlit Frontend
param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$ContainerName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "Central India"
)

Write-Host "Starting Azure Container Instances Deployment for Streamlit Frontend" -ForegroundColor Green

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "Azure CLI is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# Login check
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$loginStatus = az account show 2>$null
if (-not $loginStatus) {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Get current subscription info
$currentSub = az account show --output json | ConvertFrom-Json
Write-Host "Using subscription: $($currentSub.name)" -ForegroundColor Cyan

# Create or get resource group
Write-Host "Checking resource group: $ResourceGroupName" -ForegroundColor Yellow
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "false") {
    Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
    az group create --name $ResourceGroupName --location $Location
    Write-Host "Resource group created successfully" -ForegroundColor Green
} else {
    Write-Host "Resource group already exists" -ForegroundColor Green
}

# Build and push Docker image
Write-Host "Building Docker image for Streamlit frontend..." -ForegroundColor Yellow

$ContainerRegistryName = "acrfastapi22645"
$ImageName = "$ContainerRegistryName.azurecr.io/welfare-frontend:latest"

# Build the Docker image
Write-Host "Building image: $ImageName" -ForegroundColor Cyan
docker build -t $ImageName .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Docker image built successfully" -ForegroundColor Green

# Login to ACR
Write-Host "Logging into Azure Container Registry..." -ForegroundColor Yellow
az acr login --name $ContainerRegistryName

# Push the image
Write-Host "Pushing image to registry..." -ForegroundColor Yellow
docker push $ImageName

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker push failed" -ForegroundColor Red
    exit 1
}

Write-Host "Image pushed successfully" -ForegroundColor Green

# Deploy to Azure Container Instances
Write-Host "Deploying to Azure Container Instances..." -ForegroundColor Yellow

# Get ACR credentials
$acrCredentials = az acr credential show --name $ContainerRegistryName --output json | ConvertFrom-Json
$acrUsername = $acrCredentials.username
$acrPassword = $acrCredentials.passwords[0].value

# Deploy container
$deployResult = az container create --resource-group $ResourceGroupName --name $ContainerName --image $ImageName --registry-login-server "$ContainerRegistryName.azurecr.io" --registry-username $acrUsername --registry-password $acrPassword --dns-name-label $ContainerName --ports 8501 --cpu 1 --memory 2 --location $Location --output json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Container deployment failed" -ForegroundColor Red
    exit 1
}

$deployment = $deployResult | ConvertFrom-Json
$fqdn = $deployment.ipAddress.fqdn

Write-Host ""
Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "Your Streamlit Frontend is now live!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend URL: http://$fqdn:8501" -ForegroundColor Cyan
Write-Host "Backend URL: https://welfare-app-anech0dsctemhwbq.centralindia-01.azurewebsites.net/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready to use!" -ForegroundColor Green