#!/bin/bash

# Test script for RTD API Server
# Usage: ./test_api.sh [API_KEY]

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_KEY=${1:-"demo-key-change-in-production"}
BASE_URL="http://localhost:5000"

echo "=================================="
echo "🧪 Testing RTD API Server"
echo "=================================="
echo ""
echo "API Key: $API_KEY"
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Health check (no auth required)
echo "Test 1: Health Check (no auth)"
echo "GET $BASE_URL/api/health"
response=$(curl -s "$BASE_URL/api/health")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ FAIL${NC}"
fi
echo ""

# Test 2: Get vehicles without auth (should fail)
echo "Test 2: Get Vehicles (no auth - should fail with 401)"
echo "GET $BASE_URL/api/vehicles"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BASE_URL/api/vehicles")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d: -f2)
if [ "$http_code" = "401" ]; then
    echo -e "${GREEN}✅ PASS - Correctly rejected${NC}"
else
    echo -e "${RED}❌ FAIL - Should return 401${NC}"
fi
echo ""

# Test 3: Get vehicles with auth
echo "Test 3: Get Vehicles (with auth)"
echo "GET $BASE_URL/api/vehicles"
echo "Header: X-API-Key: $API_KEY"
response=$(curl -s -H "X-API-Key: $API_KEY" "$BASE_URL/api/vehicles")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool | head -20
    echo "..."
else
    echo -e "${RED}❌ FAIL${NC}"
fi
echo ""

# Test 4: Get vehicles for specific route
echo "Test 4: Get Vehicles for Route 'A'"
echo "GET $BASE_URL/api/vehicles/A"
response=$(curl -s -H "X-API-Key: $API_KEY" "$BASE_URL/api/vehicles/A")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ FAIL${NC}"
fi
echo ""

# Test 5: Get directions
echo "Test 5: Get Transit Directions"
echo "GET $BASE_URL/api/directions?origin=Union%20Station&destination=Denver%20Airport"
response=$(curl -s -H "X-API-Key: $API_KEY" "$BASE_URL/api/directions?origin=Union%20Station&destination=Denver%20Airport")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}"
    echo "$response" | python3 -m json.tool | head -30
    echo "..."
else
    echo -e "${RED}❌ FAIL${NC}"
fi
echo ""

echo "=================================="
echo "Testing Complete!"
echo "=================================="
echo ""
echo "💡 For Zapier Integration:"
echo "   Webhook URL: $BASE_URL/api/vehicles"
echo "   Header: X-API-Key: $API_KEY"
echo ""

