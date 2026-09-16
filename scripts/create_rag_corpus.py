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

"""Script to create a Serverless Vertex AI RAG Corpus and import Project Gutenberg document pg49513.txt."""

from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr
import vertexai

PROJECT_ID = "qwiklabs-gcp-03-6800ece3e043"
LOCATION = "us-central1"
GCS_PATH = "gs://devpulse-assets-qwiklabs-gcp-03-6800ece3e043/rag/pg49513.txt"

def main():
    print(f"Initializing Vertex AI for project '{PROJECT_ID}' in location '{LOCATION}'...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    cfg = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    try:
        rag.update_rag_engine_config(rag_engine_config=rag.RagEngineConfig(
            name=cfg,
            rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
        ))
        print("✅ RAG engine config set to serverless mode.")
    except Exception as e:
        print(f"ℹ️ RAG engine config update note: {e}")

    print("🚀 Creating Vertex AI RAG Corpus (devpulse-gutenberg-corpus)...")
    corpus = rag.create_corpus(
        display_name="devpulse-gutenberg-corpus",
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-005"
        ),
    )
    print("CREATED_CORPUS_NAME:", corpus.name)

    print(f"📥 Importing and indexing '{GCS_PATH}' into corpus...")
    resp = rag.import_files(
        corpus_name=corpus.name,
        paths=[GCS_PATH],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
    )
    print("IMPORTED_FILES_COUNT:", resp.imported_rag_files_count)
    print(f"✅ RAG corpus '{corpus.name}' successfully created and indexed!")

if __name__ == "__main__":
    main()
