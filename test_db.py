#!/usr/bin/env python3
import sys
import os
sys.path.append('backend')

from backend.app.db.database import SessionLocal
from backend.app.models.course import Course

def test_db():
    db = SessionLocal()
    try:
        courses = db.query(Course).all()
        print(f'Found {len(courses)} courses:')
        for c in courses:
            print(f'- {c.title}: ${c.price}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        db.close()

if __name__ == "__main__":
    test_db()