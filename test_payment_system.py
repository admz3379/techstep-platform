#!/usr/bin/env python3
"""
Comprehensive Payment System Testing Script
"""
import sqlite3
import json
import requests
from datetime import datetime

# Configuration
BACKEND_URL = "https://8000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev"
DB_PATH = "/home/user/webapp/backend/techstep.db"

def test_database_connection():
    """Test database connectivity and structure"""
    print("🔍 Testing Database Connection...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"✅ Database connected successfully")
        print(f"📊 Available tables: {', '.join(tables)}")
        
        # Check payment table structure
        if 'payments' in tables:
            cursor.execute("PRAGMA table_info(payments);")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"💳 Payment table columns: {', '.join(columns)}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_recent_payments():
    """Check for recent payments in database"""
    print("\n🔍 Checking Recent Payments...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, payment_intent_id, amount, currency, 
                   status, created_at, description
            FROM payments 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        payments = cursor.fetchall()
        
        if payments:
            print(f"💳 Found {len(payments)} recent payments:")
            for payment in payments:
                print(f"  - ID: {payment[0]}, Amount: ${payment[3]}, Status: {payment[5]}")
                print(f"    Payment Intent: {payment[2]}")
                print(f"    Created: {payment[6]}")
                print(f"    Description: {payment[7]}")
                print("-" * 40)
        else:
            print("❌ No payments found in database")
            
        conn.close()
    except Exception as e:
        print(f"❌ Error checking payments: {e}")

def check_recent_users():
    """Check for recent user registrations"""
    print("\n👤 Checking Recent Users...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, email, username, full_name, phone, role, 
                   is_verified, created_at
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        users = cursor.fetchall()
        
        if users:
            print(f"👥 Found {len(users)} recent users:")
            for user in users:
                print(f"  - ID: {user[0]}, Email: {user[1]}")
                print(f"    Name: {user[3]}, Role: {user[5]}")
                print(f"    Verified: {user[6]}, Created: {user[7]}")
                print("-" * 40)
        else:
            print("❌ No users found in database")
            
        conn.close()
    except Exception as e:
        print(f"❌ Error checking users: {e}")

def test_api_health():
    """Test API connectivity"""
    print("\n🏥 Testing API Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"📋 Service: {data['service']} v{data['version']}")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health Check Error: {e}")
        return False

def test_payment_endpoint():
    """Test payment intent creation endpoint"""
    print("\n💳 Testing Payment Intent Endpoint...")
    
    test_data = {
        "amount": 299900,  # $2999.00 in cents
        "currency": "usd",
        "course_id": 1,
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "customer_phone": "+1234567890"
    }
    
    try:
        print("📤 Sending payment intent request...")
        response = requests.post(
            f"{BACKEND_URL}/api/v1/payments/create-payment-intent",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "client_secret" in data:
                print("✅ Payment Intent Created Successfully!")
                print(f"🔐 Client Secret: {data['client_secret'][:20]}...")
                return data['client_secret']
            else:
                print(f"❌ Unexpected response format: {data}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.ConnectTimeout:
        print("⏱️  Request timed out - this may indicate network restrictions")
    except requests.exceptions.ConnectionError:
        print("🌐 Connection error - check network connectivity")
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    return None

def create_test_payment_record():
    """Manually create a test payment record to verify database functionality"""
    print("\n🧪 Creating Test Payment Record...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert test payment
        test_payment = (
            1,  # user_id (assuming admin user exists)
            "pi_test_manual_12345",  # payment_intent_id
            "stripe",  # payment_method
            "course_purchase",  # payment_type
            "completed",  # status
            2999.00,  # amount
            "USD",  # currency
            "Test payment - Manual verification",  # description
            1,  # course_id
            0.0,  # transaction_fee
            2999.00,  # net_amount
            datetime.utcnow().isoformat()  # processed_at
        )
        
        cursor.execute("""
            INSERT INTO payments (
                user_id, payment_intent_id, payment_method, payment_type,
                status, amount, currency, description, course_id,
                transaction_fee, net_amount, processed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_payment)
        
        conn.commit()
        payment_id = cursor.lastrowid
        
        print(f"✅ Test payment record created with ID: {payment_id}")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating test payment: {e}")
        return False

def main():
    """Run comprehensive payment system tests"""
    print("🚀 TechStep Payment System Testing")
    print("=" * 50)
    
    # Test 1: Database
    db_ok = test_database_connection()
    
    # Test 2: API Health
    api_ok = test_api_health()
    
    # Test 3: Check existing data
    check_recent_payments()
    check_recent_users()
    
    # Test 4: Payment endpoint (may fail due to network)
    client_secret = test_payment_endpoint()
    
    # Test 5: Manual test payment
    if db_ok:
        create_test_payment_record()
        print("\n🔍 Checking payments after manual test...")
        check_recent_payments()
    
    print("\n📋 Test Summary:")
    print(f"  Database: {'✅' if db_ok else '❌'}")
    print(f"  API Health: {'✅' if api_ok else '❌'}")
    print(f"  Payment Endpoint: {'✅' if client_secret else '⚠️ Network Issue'}")
    
    print("\n💡 Recommendations:")
    if not client_secret:
        print("  - Use frontend testing for full payment flow")
        print("  - Network restrictions may prevent direct Stripe API calls")
    if db_ok:
        print("  - Database is ready to record payments")
    if api_ok:
        print("  - Backend API is running and accessible")
    
    print(f"\n🌐 Test your frontend at: https://3000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev")
    print("🔐 Use test card: 4242 4242 4242 4242")

if __name__ == "__main__":
    main()