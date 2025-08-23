#!/bin/bash
echo "🚀 TechStep Payment System - Quick Test"
echo "========================================"

echo "🏥 1. Testing API Health..."
curl -s https://8000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev/health | python3 -m json.tool

echo -e "\n💳 2. Testing Payment Intent Creation..."
curl -X POST "https://8000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev/api/v1/payments/create-payment-intent" \
-H "Content-Type: application/json" \
-d '{
  "amount": 299900,
  "currency": "usd",
  "course_id": 1,
  "customer_name": "Quick Test User",
  "customer_email": "quicktest@example.com",
  "customer_phone": "+1555000123"
}' | python3 -m json.tool

echo -e "\n🔍 3. Checking Database Records..."
cd /home/user/webapp && python3 check_payments.py | head -20

echo -e "\n✅ Quick test completed!"
echo -e "\n🌐 Frontend Test: https://3000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev"
echo "🔐 Test Card: 4242 4242 4242 4242"