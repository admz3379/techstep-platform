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
                "title": "SOC Analyst Foundations",
                "slug": "soc-analyst-foundations",
                "description": "Master security operations center fundamentals, threat detection, and incident response procedures.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "beginner",
                "price": 1200.00,
                "duration_hours": 180,
                "instructor_name": "Sarah Chen",
                "instructor_bio": "SOC Manager with 10+ years in cybersecurity operations",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Master SOC fundamentals", "Understand threat detection", "Learn incident response procedures"],
                "prerequisites": ["Basic IT knowledge"],
                "tags": ["SOC", "threat detection", "incident response"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=250&fit=crop"
            },
            {
                "title": "Cyber Threat Analyst & Incident Response",
                "slug": "cyber-threat-analyst-incident-response",
                "description": "Advanced threat hunting, malware analysis, and comprehensive incident response strategies.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "intermediate",
                "price": 1400.00,
                "duration_hours": 180,
                "instructor_name": "Michael Rodriguez",
                "instructor_bio": "Senior Threat Analyst with expertise in malware analysis",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Advanced threat hunting", "Malware analysis techniques", "Incident response strategies"],
                "prerequisites": ["SOC fundamentals", "Basic networking"],
                "tags": ["threat hunting", "malware analysis", "incident response"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&h=250&fit=crop"
            },
            {
                "title": "SIEM Engineering - Splunk Specialization",
                "slug": "siem-engineering-splunk",
                "description": "Master Splunk administration, SIEM deployment, and security monitoring infrastructure.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "intermediate",
                "price": 1100.00,
                "duration_hours": 180,
                "instructor_name": "Dr. Emily Watson",
                "instructor_bio": "SIEM Architect and Splunk Expert with 12+ years experience",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Master Splunk administration", "SIEM deployment", "Security monitoring infrastructure"],
                "prerequisites": ["Basic security knowledge", "Command line familiarity"],
                "tags": ["SIEM", "Splunk", "security monitoring"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=250&fit=crop"
            },
            {
                "title": "Cloud Security Analyst (AWS, Azure, GCP)",
                "slug": "cloud-security-analyst",
                "description": "AWS, Azure, and GCP security architecture, compliance, and best practices.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "intermediate",
                "price": 1300.00,
                "duration_hours": 180,
                "instructor_name": "David Kim",
                "instructor_bio": "Cloud Security Architect with AWS and Azure certifications",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["AWS security architecture", "Azure compliance", "GCP best practices"],
                "prerequisites": ["Cloud platform experience", "Basic security fundamentals"],
                "tags": ["cloud security", "AWS", "Azure", "GCP"],
                "status": "published",
                "is_featured": True,
                "thumbnail_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&h=250&fit=crop"
            },
            {
                "title": "Malware Analyst & Network Defense",
                "slug": "malware-analyst-network-defense",
                "description": "Reverse engineering, dynamic analysis, and advanced network security techniques.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "advanced",
                "price": 1500.00,
                "duration_hours": 180,
                "instructor_name": "Alex Rivera",
                "instructor_bio": "Malware Research Specialist with reverse engineering expertise",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Reverse engineering techniques", "Dynamic malware analysis", "Network defense strategies"],
                "prerequisites": ["Advanced security knowledge", "Programming basics"],
                "tags": ["malware analysis", "reverse engineering", "network defense"],
                "status": "published",
                "is_featured": False,
                "thumbnail_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=250&fit=crop"
            },
            {
                "title": "Risk & Compliance Analyst - GRC Fundamentals",
                "slug": "risk-compliance-analyst-grc",
                "description": "Governance frameworks, risk management, and regulatory compliance strategies.",
                "short_description": "Self-paced learning decks, labs, virtual internship & certificate",
                "level": "intermediate",
                "price": 1400.00,
                "duration_hours": 180,
                "instructor_name": "Michelle Zhang",
                "instructor_bio": "GRC Consultant with expertise in compliance frameworks",
                "instructor_avatar_url": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
                "learning_objectives": ["Governance frameworks", "Risk management", "Regulatory compliance"],
                "prerequisites": ["Basic business knowledge", "Security awareness"],
                "tags": ["GRC", "compliance", "risk management"],
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