#!/usr/bin/env python3
"""
Demo Seed Data - Creates Maria and Robert for the demo
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Client, Provider, Appointment

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/first_contact")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_demo_data():
    session = SessionLocal()
    try:
        print("🌱 Seeding demo data...\n")
        
        # Provider: Dr. Smith
        dr_smith = Provider(
            provider_id="dr_smith_001",
            name="Dr. Sarah Smith",
            provider_type="medical",
            contact_email="dr.smith@longbeachhealth.org",
            contact_phone="+1-562-555-0100"
        )
        session.add(dr_smith)
        print("✅ Created provider: Dr. Smith")
        
        # Client A: Maria (tomorrow 2pm appointment)
        tomorrow_2pm = datetime.now() + timedelta(days=1)
        tomorrow_2pm = tomorrow_2pm.replace(hour=14, minute=0, second=0)
        
        maria = Client(
            client_id="maria_demo_001",
            first_name="Maria",
            last_name="Rodriguez",
            medical_urgency=5,
            documents_status={"verified": True}
        )
        session.add(maria)
        
        maria_apt = Appointment(
            client_id="maria_demo_001",
            provider_id="dr_smith_001",
            scheduled_time=tomorrow_2pm,
            status="scheduled"
        )
        session.add(maria_apt)
        print(f"✅ Maria: Tomorrow {tomorrow_2pm.strftime('%I:%M %p')}")
        
        # Client B: Robert (next week 2pm, HIGH urgency)
        next_week = datetime.now() + timedelta(days=7)
        next_week = next_week.replace(hour=14, minute=0, second=0)
        
        robert = Client(
            client_id="robert_demo_001",
            first_name="Robert",
            last_name="Johnson",
            medical_urgency=8,  # HIGH
            documents_status={"verified": True}
        )
        session.add(robert)
        
        robert_apt = Appointment(
            client_id="robert_demo_001",
            provider_id="dr_smith_001",
            scheduled_time=next_week,
            status="scheduled"
        )
        session.add(robert_apt)
        print(f"✅ Robert: Next week {next_week.strftime('%I:%M %p')} (urgency=8)")
        
        session.commit()
        print("\n🎉 Demo data ready!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_demo_data()
