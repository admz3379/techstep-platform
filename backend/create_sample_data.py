#!/usr/bin/env python3
"""
Create sample data for TechStep platform
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.user import User
from app.models.course import Course
from app.core.security import get_password_hash
import json

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample admin user
        admin_user = db.query(User).filter(User.email == "admin@techstep.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@techstep.com",
                username="admin",
                full_name="TechStep Administrator",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_verified=True
            )
            db.add(admin_user)
            print("✅ Created admin user: admin@techstep.com / admin123")

        # Create sample student user
        student_user = db.query(User).filter(User.email == "student@techstep.com").first()
        if not student_user:
            student_user = User(
                email="student@techstep.com",
                username="student",
                full_name="John Doe",
                hashed_password=get_password_hash("student123"),
                role="student",
                is_verified=True
            )
            db.add(student_user)
            print("✅ Created student user: student@techstep.com / student123")

        # Create sample courses
        courses_data = [
            {
                "title": "Complete Ethical Hacking Bootcamp",
                "slug": "ethical-hacking-bootcamp",
                "description": "Master the art of ethical hacking with our comprehensive bootcamp. Learn penetration testing, vulnerability assessment, and advanced security techniques used by professionals.",
                "short_description": "Learn ethical hacking and penetration testing from scratch",
                "level": "intermediate",
                "price": 299.99,
                "duration_hours": 40,
                "instructor_name": "Sarah Chen",
                "instructor_bio": "Certified Ethical Hacker (CEH) with 8+ years in cybersecurity",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Master penetration testing techniques", "Understand vulnerability assessment", "Learn network security fundamentals"],
                "prerequisites": ["Basic networking knowledge", "Command line familiarity"],
                "tags": ["ethical hacking", "penetration testing", "security"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=250&fit=crop"
            },
            {
                "title": "Network Security Fundamentals",
                "slug": "network-security-fundamentals",
                "description": "Build a strong foundation in network security. Cover firewalls, intrusion detection systems, VPNs, and network monitoring techniques.",
                "short_description": "Essential network security concepts and implementations",
                "level": "beginner",
                "price": 199.99,
                "duration_hours": 25,
                "instructor_name": "Michael Rodriguez",
                "instructor_bio": "Network Security Specialist with CISSP certification",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Understand network protocols", "Configure firewalls", "Implement network monitoring"],
                "prerequisites": ["Basic IT knowledge"],
                "tags": ["networking", "firewalls", "security fundamentals"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=250&fit=crop"
            },
            {
                "title": "Incident Response & Digital Forensics",
                "slug": "incident-response-forensics",
                "description": "Learn how to respond to security incidents and conduct digital forensics investigations. Master tools and techniques used by incident response teams.",
                "short_description": "Professional incident response and forensics training",
                "level": "advanced",
                "price": 399.99,
                "duration_hours": 35,
                "instructor_name": "Dr. Emily Watson",
                "instructor_bio": "Digital Forensics Expert and Former FBI Cybercrime Investigator",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Master incident response procedures", "Learn forensics tools", "Understand legal aspects"],
                "prerequisites": ["Advanced networking knowledge", "Security fundamentals"],
                "tags": ["incident response", "digital forensics", "investigation"],
                "status": "published",
                "is_featured": False,
                "thumbnail_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=250&fit=crop"
            },
            {
                "title": "Cloud Security Architecture",
                "slug": "cloud-security-architecture",
                "description": "Secure cloud environments with best practices for AWS, Azure, and GCP. Learn cloud-specific security controls and compliance requirements.",
                "short_description": "Comprehensive cloud security for modern environments",
                "level": "intermediate",
                "price": 349.99,
                "duration_hours": 30,
                "instructor_name": "David Kim",
                "instructor_bio": "Cloud Security Architect with AWS and Azure certifications",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Design secure cloud architectures", "Implement compliance controls", "Manage cloud security tools"],
                "prerequisites": ["Cloud platform experience", "Security fundamentals"],
                "tags": ["cloud security", "AWS", "Azure", "compliance"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=250&fit=crop"
            }
        ]

        for course_data in courses_data:
            existing_course = db.query(Course).filter(Course.slug == course_data["slug"]).first()
            if not existing_course:
                # Convert lists to JSON strings
                course_data["learning_objectives"] = json.dumps(course_data["learning_objectives"])
                course_data["prerequisites"] = json.dumps(course_data["prerequisites"])
                course_data["tags"] = json.dumps(course_data["tags"])
                
                course = Course(**course_data)
                db.add(course)
                print(f"✅ Created course: {course_data['title']}")

        db.commit()
        print(f"\n🎉 Sample data created successfully!")
        print(f"Backend API URL: https://8000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev")
        print(f"API Docs: https://8000-iijrwv71livvm5m4tkmpb-6532622b.e2b.dev/docs")

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()