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

import os
import sys

# Ensure project root is in sys.path so app module imports resolve properly
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools.load_memory_tool import LoadMemoryTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager

from app.a2ui_utils import a2ui_callback
from app.tools import (
    fetch_pypi_package_info,
    inspect_local_git_status,
    git_repository_inspector,
    search_knowledge_base,
    read_support_tickets,
    create_or_update_support_ticket,
    manage_support_ticket,
    run_diagnostic_code,
    get_system_topology,
    consult_gutenberg_corpus,
    generate_system_asset_image,
    generate_system_asset_video,
)


async def generate_memories_callback(callback_context: CallbackContext):
    """Callback after agent execution to persist session events to Vertex AI Memory Bank."""
    await callback_context.add_session_to_memory()
    return None


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

SYSTEM_INSTRUCTION = schema_manager.generate_system_prompt(
    role_description=(
        "You are DevPulse, an expert AI Developer & IT Support Assistant built on Google Agent Platform.\n"
        "You remember facts, preferences, developer role context, and explicitly ALL user allergies "
        "(e.g. food, environmental, or medical allergies) stated in previous conversations, using them "
        "to personalize every response and maintain safety across sessions.\n"
        "If the user asks a question about catering, food, team lunches, or health precautions, ALWAYS "
        "check user memory or call `load_memory(query='allergies')` to ensure all stored allergies are "
        "retrieved and respected."
    ),
    workflow_description=(
        "Analyze the request and return structured UI when appropriate.\n"
        "Your primary tools and capabilities include:\n"
        "1. Generating IT asset & architecture diagram images using gemini-3.1-flash-lite-image (generate_system_asset_image).\n"
        "2. Generating short IT system asset videos or status animations using gemini-omni-flash-preview (generate_system_asset_video).\n"
        "3. Fetching package release metadata and dependencies from PyPI public API (fetch_pypi_package_info).\n"
        "4. Inspecting real local Git repository history, working tree changes, and branch status (inspect_local_git_status).\n"
        "5. Inspecting simulated or target Git repository commits and diffs (git_repository_inspector).\n"
        "6. Searching internal IT & Developer knowledge base corpora via RAG (search_knowledge_base).\n"
        "7. Grounded knowledge retrieval from Project Gutenberg document corpus pg49513 (consult_gutenberg_corpus).\n"
        "8. Reading support tickets from Google Cloud Firestore backend (read_support_tickets).\n"
        "9. Creating or updating support tickets in Google Cloud Firestore (create_or_update_support_ticket / manage_support_ticket).\n"
        "10. Running diagnostic computations in a sandboxed execution tool (run_diagnostic_code).\n"
        "11. Providing system architecture topology summaries (get_system_topology).\n"
        "12. Executing Python code in a secure Agent Engine Sandbox (AgentEngineSandboxCodeExecutor)."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

# Configure AgentEngineSandboxCodeExecutor with the agent engine resource
code_executor = AgentEngineSandboxCodeExecutor(
    agent_engine_resource_name="projects/qwiklabs-gcp-03-6800ece3e043/locations/us-central1/reasoningEngines/3030005006766964736"
)

root_agent = Agent(
    name="devpulse_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    code_executor=code_executor,
    tools=[
        PreloadMemoryTool(),
        LoadMemoryTool(),
        generate_system_asset_image,
        generate_system_asset_video,
        fetch_pypi_package_info,
        inspect_local_git_status,
        git_repository_inspector,
        search_knowledge_base,
        consult_gutenberg_corpus,
        read_support_tickets,
        create_or_update_support_ticket,
        manage_support_ticket,
        run_diagnostic_code,
        get_system_topology,
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
