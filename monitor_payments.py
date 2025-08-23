#!/usr/bin/env python3
"""
Real-time payment monitoring script
"""
import sqlite3
import time
from datetime import datetime

DB_PATH = "/home/user/webapp/backend/techstep.db"

def monitor_payments():
    """Monitor new payments in real-time"""
    print("🔍 Starting Payment Monitor...")
    print("💡 Make a test payment on your frontend and watch for new records!")
    print("-" * 60)
    
    last_count = 0
    
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Get current payment count
            cursor.execute("SELECT COUNT(*) FROM payments;")
            current_count = cursor.fetchone()[0]
            
            # Check for new payments
            if current_count > last_count:
                new_payments = current_count - last_count
                print(f"🎉 {new_payments} NEW PAYMENT(S) DETECTED!")
                
                # Show latest payment details
                cursor.execute("""
                    SELECT id, user_id, payment_intent_id, amount, 
                           status, description, created_at
                    FROM payments 
                    ORDER BY created_at DESC 
                    LIMIT ?;
                """, (new_payments,))
                
                payments = cursor.fetchall()
                for payment in payments:
                    print(f"  💳 Payment ID: {payment[0]}")
                    print(f"     Amount: ${payment[3]}")
                    print(f"     Status: {payment[4]}")
                    print(f"     Intent ID: {payment[2]}")
                    print(f"     Time: {payment[6]}")
                    print("-" * 40)
                
                last_count = current_count
            
            conn.close()
            
            # Update status
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Monitoring... (Total: {current_count} payments)")
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            print("\n👋 Payment monitoring stopped.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_payments()