#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Seed script to populate initial support ticket items into Google Cloud Firestore backend."""

import os
import sys

# Ensure project root is on sys.path
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from app.firestore_service import PROJECT_ID, seed_firestore_tickets, read_support_tickets_db

def main():
    print(f"🚀 Seeding Firestore backend collection 'support_tickets' for project: '{PROJECT_ID}'...")
    seeded_items = seed_firestore_tickets()
    print(f"✅ Successfully seeded {len(seeded_items)} support tickets!")
    for item in seeded_items:
        print(f"  - [{item['ticket_id']}] ({item['priority']}) {item['title']} -> {item['status']}")

    print("\n🔍 Verifying tickets reading tool output...")
    current_tickets = read_support_tickets_db()
    print(f"Total tickets in backend: {len(current_tickets)}")

if __name__ == "__main__":
    main()
