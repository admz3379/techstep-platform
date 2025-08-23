#!/usr/bin/env python3
"""
Script to check payment records in the TechStep database
"""
import sqlite3
import json
from datetime import datetime

def check_payments():
    """Check all payment records in the database"""
    db_path = "/home/user/webapp/backend/techstep.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if payments table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("📊 Available tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "="*60)
        
        # Check payments table
        try:
            cursor.execute("SELECT * FROM payments ORDER BY created_at DESC LIMIT 10;")
            payments = cursor.fetchall()
            
            if payments:
                # Get column names
                cursor.execute("PRAGMA table_info(payments);")
                columns = [col[1] for col in cursor.fetchall()]
                
                print(f"💳 Recent Payments (Last 10):")
                print("-" * 60)
                
                for payment in payments:
                    payment_dict = dict(zip(columns, payment))
                    print(f"Payment ID: {payment_dict.get('id', 'N/A')}")
                    print(f"Stripe Payment Intent: {payment_dict.get('stripe_payment_intent_id', 'N/A')}")
                    print(f"User ID: {payment_dict.get('user_id', 'N/A')}")
                    print(f"Course ID: {payment_dict.get('course_id', 'N/A')}")
                    print(f"Amount: ${payment_dict.get('amount', 0) / 100:.2f}")
                    print(f"Status: {payment_dict.get('status', 'N/A')}")
                    print(f"Payment Type: {payment_dict.get('payment_type', 'N/A')}")
                    print(f"Created: {payment_dict.get('created_at', 'N/A')}")
                    print("-" * 40)
            else:
                print("❌ No payments found in database")
                
        except sqlite3.OperationalError as e:
            print(f"❌ Error accessing payments table: {e}")
            
        print("\n" + "="*60)
        
        # Check users table
        try:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"👤 Total users in database: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, email, created_at FROM users ORDER BY created_at DESC LIMIT 5;")
                recent_users = cursor.fetchall()
                print("📝 Recent users:")
                for user in recent_users:
                    print(f"  ID: {user[0]}, Email: {user[1]}, Created: {user[2]}")
                    
        except sqlite3.OperationalError as e:
            print(f"❌ Error accessing users table: {e}")
        
        print("\n" + "="*60)
        
        # Check course_enrollments table
        try:
            cursor.execute("SELECT COUNT(*) FROM course_enrollments;")
            enrollment_count = cursor.fetchone()[0]
            print(f"📚 Total course enrollments in database: {enrollment_count}")
            
            if enrollment_count > 0:
                cursor.execute("""
                    SELECT e.id, e.user_id, e.course_id, e.created_at, c.title 
                    FROM course_enrollments e 
                    LEFT JOIN courses c ON e.course_id = c.id 
                    ORDER BY e.created_at DESC LIMIT 5;
                """)
                recent_enrollments = cursor.fetchall()
                print("📖 Recent enrollments:")
                for enrollment in recent_enrollments:
                    print(f"  ID: {enrollment[0]}, User: {enrollment[1]}, Course: {enrollment[4] or enrollment[2]}, Created: {enrollment[3]}")
                    
        except sqlite3.OperationalError as e:
            print(f"❌ Error accessing course_enrollments table: {e}")
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔍 Checking TechStep Payment Records...")
    print("="*60)
    check_payments()
    print("\n✅ Payment check completed!")