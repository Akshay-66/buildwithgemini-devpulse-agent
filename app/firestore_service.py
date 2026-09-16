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

import logging
from typing import Dict, List, Optional
from google.cloud import firestore

# IMPORTANT: Hardcoded GCP Project ID for DevPulse agent
# Do NOT read from google.auth.default() or GOOGLE_CLOUD_PROJECT environment variable,
# as those return project numbers on Google Agent Platform.
PROJECT_ID = "qwiklabs-gcp-03-6800ece3e043"
COLLECTION_NAME = "support_tickets"

logger = logging.getLogger(__name__)

# Fallback memory store in case Firestore database is unavailable or not yet created
_LOCAL_TICKETS_STORE: Dict[str, dict] = {
    "TICK-101": {
        "ticket_id": "TICK-101",
        "title": "API Gateway 504 Timeout Error",
        "description": "Intermittent 504 timeouts on /v1/auth endpoint during high traffic spikes.",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "assignee": "infra-team",
        "category": "Infrastructure",
        "created_at": "2026-09-16T10:00:00Z"
    },
    "TICK-102": {
        "ticket_id": "TICK-102",
        "title": "VPN & Developer Proxy Setup",
        "description": "New developer onboarding: request for internal proxy access and certificate installation.",
        "status": "OPEN",
        "priority": "MEDIUM",
        "assignee": "it-helpdesk",
        "category": "Authentication",
        "created_at": "2026-09-16T11:30:00Z"
    },
    "TICK-103": {
        "ticket_id": "TICK-103",
        "title": "CI/CD Build Failure after dependency upgrade",
        "description": "Pytest failure on main branch after upgrading protobuf package.",
        "status": "RESOLVED",
        "priority": "HIGH",
        "assignee": "dev-lead",
        "category": "Build Pipeline",
        "created_at": "2026-09-15T14:20:00Z"
    }
}


def get_firestore_client() -> Optional[firestore.Client]:
    """Initializes and returns the Firestore client with hardcoded project ID."""
    try:
        return firestore.Client(project=PROJECT_ID)
    except Exception as e:
        logger.warning(f"Failed to initialize Firestore client for project '{PROJECT_ID}': {e}")
        return None


def read_support_tickets_db(ticket_id: Optional[str] = None, status: Optional[str] = None) -> List[dict]:
    """Reads support tickets from Firestore collection 'support_tickets' with local fallback."""
    client = get_firestore_client()
    if client:
        try:
            col_ref = client.collection(COLLECTION_NAME)
            if ticket_id:
                doc = col_ref.document(ticket_id).get()
                if doc.exists:
                    return [doc.to_dict()]
                return []
            
            docs = col_ref.stream()
            results = [d.to_dict() for d in docs]
            if status:
                results = [t for t in results if t.get("status", "").upper() == status.upper()]
            if results:
                return results
        except Exception as e:
            logger.warning(f"Firestore query error: {e}. Falling back to in-memory ticket store.")

    # Fallback return from memory store
    tickets = list(_LOCAL_TICKETS_STORE.values())
    if ticket_id:
        return [t for t in tickets if t.get("ticket_id") == ticket_id]
    if status:
        return [t for t in tickets if t.get("status", "").upper() == status.upper()]
    return tickets


def save_support_ticket_db(
    ticket_id: str,
    title: str,
    description: str,
    status: str = "OPEN",
    priority: str = "MEDIUM",
    assignee: str = "it-helpdesk",
    category: str = "General"
) -> dict:
    """Creates or updates a support ticket document in Firestore collection 'support_tickets'."""
    ticket_data = {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "status": status.upper(),
        "priority": priority.upper(),
        "assignee": assignee,
        "category": category,
        "created_at": "2026-09-16T16:22:00Z"
    }
    
    client = get_firestore_client()
    if client:
        try:
            doc_ref = client.collection(COLLECTION_NAME).document(ticket_id)
            doc_ref.set(ticket_data)
            logger.info(f"Saved ticket {ticket_id} to Firestore collection '{COLLECTION_NAME}'")
        except Exception as e:
            logger.warning(f"Firestore set error: {e}. Updating in-memory ticket store.")
            _LOCAL_TICKETS_STORE[ticket_id] = ticket_data
    else:
        _LOCAL_TICKETS_STORE[ticket_id] = ticket_data

    return ticket_data


def seed_firestore_tickets() -> List[dict]:
    """Seeds initial IT & developer support tickets into Firestore collection 'support_tickets'."""
    client = get_firestore_client()
    seeded = []
    
    initial_tickets = [
        {
            "ticket_id": "TICK-101",
            "title": "API Gateway 504 Timeout Error",
            "description": "Intermittent 504 timeouts on /v1/auth endpoint during high traffic spikes.",
            "status": "IN_PROGRESS",
            "priority": "HIGH",
            "assignee": "infra-team",
            "category": "Infrastructure",
            "created_at": "2026-09-16T10:00:00Z"
        },
        {
            "ticket_id": "TICK-102",
            "title": "VPN & Developer Proxy Setup",
            "description": "New developer onboarding: request for internal proxy access and certificate installation.",
            "status": "OPEN",
            "priority": "MEDIUM",
            "assignee": "it-helpdesk",
            "category": "Authentication",
            "created_at": "2026-09-16T11:30:00Z"
        },
        {
            "ticket_id": "TICK-103",
            "title": "CI/CD Build Failure after dependency upgrade",
            "description": "Pytest failure on main branch after upgrading protobuf package.",
            "status": "RESOLVED",
            "priority": "HIGH",
            "assignee": "dev-lead",
            "category": "Build Pipeline",
            "created_at": "2026-09-15T14:20:00Z"
        }
    ]

    for item in initial_tickets:
        _LOCAL_TICKETS_STORE[item["ticket_id"]] = item
        if client:
            try:
                client.collection(COLLECTION_NAME).document(item["ticket_id"]).set(item)
                logger.info(f"Seeded ticket {item['ticket_id']} into Firestore")
            except Exception as e:
                logger.warning(f"Could not write {item['ticket_id']} to Firestore: {e}")
        seeded.append(item)

    return seeded
