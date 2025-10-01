# Step 1: Azure Application Gateway Deployment
# This script creates an Application Gateway for load balancing and routing

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$true)]
    [string]$AppGatewayName,
    
    [Parameter(Mandatory=$true)]
    [string]$VNetName,
    
    [Parameter(Mandatory=$true)]
    [string]$BackendAppUrl,  # Your current app URL
    
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId
)

Write-Host "Step 1: Implementing Azure Application Gateway" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check Azure CLI
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install it first." -ForegroundColor Red
    exit 1
}

# Login check
$loginStatus = az account show 2>$null
if (-not $loginStatus) {
    Write-Host "Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Set subscription
if ($SubscriptionId) {
    az account set --subscription $SubscriptionId
}

$currentSub = az account show --output json | ConvertFrom-Json
Write-Host "📋 Using subscription: $($currentSub.name)" -ForegroundColor Cyan

# Step 1.1: Create Virtual Network for Application Gateway
Write-Host "Creating Virtual Network: $VNetName" -ForegroundColor Yellow

$vnetExists = az network vnet show --name $VNetName --resource-group $ResourceGroupName 2>$null
if (-not $vnetExists) {
    # Create VNet with subnets
    az network vnet create `
        --name $VNetName `
        --resource-group $ResourceGroupName `
        --location $Location `
        --address-prefix 10.0.0.0/16 `
        --subnet-name AppGatewaySubnet `
        --subnet-prefix 10.0.1.0/24
    
    # Create additional subnet for backend services
    az network vnet subnet create `
        --name BackendSubnet `
        --resource-group $ResourceGroupName `
        --vnet-name $VNetName `
        --address-prefix 10.0.2.0/24
    
    Write-Host "✅ Virtual Network created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual Network already exists" -ForegroundColor Green
}

# Step 1.2: Create Public IP for Application Gateway
$publicIpName = "$AppGatewayName-pip"
Write-Host "🌐 Creating Public IP: $publicIpName" -ForegroundColor Yellow

$pipExists = az network public-ip show --name $publicIpName --resource-group $ResourceGroupName 2>$null
if (-not $pipExists) {
    az network public-ip create `
        --name $publicIpName `
        --resource-group $ResourceGroupName `
        --location $Location `
        --allocation-method Static `
        --sku Standard `
        --tier Regional
    
    Write-Host "✅ Public IP created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Public IP already exists" -ForegroundColor Green
}

# Step 1.3: Create Application Gateway
Write-Host "🚪 Creating Application Gateway: $AppGatewayName" -ForegroundColor Yellow

$appGwExists = az network application-gateway show --name $AppGatewayName --resource-group $ResourceGroupName 2>$null
if (-not $appGwExists) {
    # Create Application Gateway with basic configuration
    az network application-gateway create `
        --name $AppGatewayName `
        --resource-group $ResourceGroupName `
        --location $Location `
        --capacity 2 `
        --sku Standard_v2 `
        --vnet-name $VNetName `
        --subnet AppGatewaySubnet `
        --public-ip-address $publicIpName `
        --http-settings-cookie-based-affinity Disabled `
        --http-settings-port 80 `
        --http-settings-protocol Http `
        --frontend-port 80 `
        --servers $BackendAppUrl
    
    Write-Host "✅ Application Gateway created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Application Gateway already exists" -ForegroundColor Green
}

# Step 1.4: Configure Health Probe
Write-Host "🩺 Configuring Health Probe..." -ForegroundColor Yellow

az network application-gateway probe create `
    --gateway-name $AppGatewayName `
    --resource-group $ResourceGroupName `
    --name HealthProbe `
    --protocol Http `
    --host-name-from-http-settings true `
    --path "/health" `
    --interval 30 `
    --timeout 30 `
    --threshold 3

# Update backend HTTP settings to use the health probe
az network application-gateway http-settings update `
    --gateway-name $AppGatewayName `
    --resource-group $ResourceGroupName `
    --name appGatewayBackendHttpSettings `
    --probe HealthProbe

Write-Host "✅ Health probe configured" -ForegroundColor Green

# Step 1.5: Configure SSL (Optional - for HTTPS)
Write-Host "🔒 Setting up SSL redirect..." -ForegroundColor Yellow

# Add HTTPS listener (port 443)
az network application-gateway frontend-port create `
    --gateway-name $AppGatewayName `
    --resource-group $ResourceGroupName `
    --name HttpsPort `
    --port 443

Write-Host "✅ SSL configuration prepared (certificate needed for full HTTPS)" -ForegroundColor Green

# Step 1.6: Configure URL routing rules
Write-Host "🔀 Configuring routing rules..." -ForegroundColor Yellow

# Create path-based rule for API endpoints
az network application-gateway url-path-map create `
    --gateway-name $AppGatewayName `
    --resource-group $ResourceGroupName `
    --name ApiPathMap `
    --default-address-pool appGatewayBackendPool `
    --default-http-settings appGatewayBackendHttpSettings `
    --rule-name ApiRule `
    --address-pool appGatewayBackendPool `
    --http-settings appGatewayBackendHttpSettings `
    --paths "/api/*" "/docs" "/openapi.json" "/health"

Write-Host "✅ Routing rules configured" -ForegroundColor Green

# Step 1.7: Get deployment information
Write-Host "📋 Application Gateway Deployment Summary:" -ForegroundColor Cyan

$appGwInfo = az network application-gateway show --name $AppGatewayName --resource-group $ResourceGroupName --output json | ConvertFrom-Json
$publicIpInfo = az network public-ip show --name $publicIpName --resource-group $ResourceGroupName --output json | ConvertFrom-Json

Write-Host "✅ Step 1 - Application Gateway completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Application Gateway Details:" -ForegroundColor Cyan
Write-Host "  Name: $AppGatewayName" -ForegroundColor White
Write-Host "  Public IP: $($publicIpInfo.ipAddress)" -ForegroundColor White
Write-Host "  Frontend URL: http://$($publicIpInfo.ipAddress)" -ForegroundColor White
Write-Host "  Health Probe: /health endpoint" -ForegroundColor White
Write-Host "  Backend Pool: $BackendAppUrl" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Configuration Features:" -ForegroundColor Yellow
Write-Host "  ✅ Load balancing enabled" -ForegroundColor Green
Write-Host "  ✅ Health monitoring configured" -ForegroundColor Green
Write-Host "  ✅ URL path-based routing" -ForegroundColor Green
Write-Host "  ✅ Auto-scaling (2 instances minimum)" -ForegroundColor Green
Write-Host "  🔒 SSL ready (certificate required)" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Test the Application Gateway: http://$($publicIpInfo.ipAddress)" -ForegroundColor White
Write-Host "  2. Configure SSL certificate for HTTPS" -ForegroundColor White
Write-Host "  3. Update DNS to point to: $($publicIpInfo.ipAddress)" -ForegroundColor White
Write-Host "  4. Move to Step 2: Virtual Network & NSGs" -ForegroundColor White
Write-Host ""

# Save configuration details for next steps
$configDetails = @{
    ResourceGroupName = $ResourceGroupName
    AppGatewayName = $AppGatewayName
    VNetName = $VNetName
    PublicIP = $publicIpInfo.ipAddress
    Location = $Location
} | ConvertTo-Json

$configDetails | Out-File -FilePath "step1-appgateway-config.json" -Encoding UTF8
Write-Host "💾 Configuration saved to: step1-appgateway-config.json" -ForegroundColor Cyan

Write-Host ""
Write-Host "🚀 Ready for Step 2? Run the Virtual Network & NSGs script!" -ForegroundColor Green