# 🔧 Manual Load Balancer Implementation Guide

## Current App Architecture
- **Frontend**: Container App `welfare-frontend-app`
- **Backend**: Container App `welfare-backend-app` 
- **Database**: Azure SQL Database
- **Container Registry**: `acrfastapi22645.azurecr.io`

## Option 1: Azure Front Door (Best for Global Load Balancing)

### Step 1: Create Azure Front Door
1. Go to Azure Portal → Search "Front Door"
2. Click "Create" → "Front Door and CDN profiles"
3. Choose "Azure Front Door (classic)" for simplicity
4. Basic Configuration:
   - **Resource Group**: `welfare-prod-rg`
   - **Name**: `welfare-front-door`
   - **Region**: Global

### Step 2: Configure Frontend Host
- **Frontend hosts**: Add custom domain
  - **Host name**: `welfare-app.yourdomain.com` (or use azurefd.net subdomain)

### Step 3: Configure Backend Pool
- **Backend pools** → Add backend pool:
  - **Name**: `welfare-backend-pool`
  - **Load balancing**: Weighted round robin
  - **Backends**:
    - **Backend 1**: Your frontend container app URL
    - **Backend 2**: Your backend container app URL (if you want to load balance between multiple instances)

### Step 4: Configure Routing Rules
- **Routing rules**:
  - **Rule 1**: `/api/*` → Route to backend
  - **Rule 2**: `/*` → Route to frontend

## Option 2: Application Gateway (Web Application Firewall)

### Azure CLI Commands (Run these in order):

```bash
# 1. Create Virtual Network
az network vnet create \
  --resource-group welfare-prod-rg \
  --name welfare-vnet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name gateway-subnet \
  --subnet-prefix 10.0.1.0/24

# 2. Create Public IP
az network public-ip create \
  --resource-group welfare-prod-rg \
  --name welfare-gateway-ip \
  --allocation-method Static \
  --sku Standard

# 3. Create Application Gateway
az network application-gateway create \
  --resource-group welfare-prod-rg \
  --name welfare-app-gateway \
  --location eastus \
  --vnet-name welfare-vnet \
  --subnet gateway-subnet \
  --capacity 2 \
  --sku Standard_v2 \
  --http-settings-cookie-based-affinity Disabled \
  --public-ip-address welfare-gateway-ip \
  --servers welfare-frontend-app.azurewebsites.net
```

## Option 3: Simple Traffic Manager (DNS-based)

### Step 1: Create Traffic Manager Profile
1. Go to Azure Portal → Search "Traffic Manager"
2. Click "Create"
3. Basic Configuration:
   - **Name**: `welfare-traffic-manager`
   - **Routing method**: Performance (or Weighted)
   - **Resource Group**: `welfare-prod-rg`

### Step 2: Add Endpoints
- **Endpoints** → Add endpoint:
  - **Type**: Azure endpoint
  - **Name**: `welfare-frontend`
  - **Target resource**: Select your container app
  - **Weight**: 100 (if using weighted routing)

## Option 4: Azure Container Apps Built-in Load Balancing

### Enable Multiple Replicas (Simplest Option)
1. Go to your Container App → **Scale and replicas**
2. Enable **Scale** options:
   - **Min replicas**: 2
   - **Max replicas**: 10
   - **Scale rules**: Add HTTP scale rule
     - **Rule name**: `http-requests`
     - **Metadata**: `concurrentRequests=10`

This automatically provides load balancing between replicas!

## Recommended Implementation Order:

### Quick Start (5 minutes):
1. **Container Apps Scale** → Enable 2+ replicas
2. This gives you instant load balancing

### Production Ready (30 minutes):
1. **Azure Front Door** → Global load balancing + CDN
2. **Application Gateway** → Web Application Firewall
3. **Traffic Manager** → DNS-based routing

## Testing Your Load Balancer:

```bash
# Test multiple requests to see load distribution
for i in {1..10}; do
  curl -I https://your-load-balancer-url.com
  echo "Request $i completed"
done
```

## Monitoring Load Balancer:
1. Go to Azure Monitor
2. Create alerts for:
   - Response time > 2 seconds
   - Error rate > 5%
   - Healthy backend instances < 1

Would you like me to help implement any of these options?