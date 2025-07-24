"""
Retrieval-Augmented Generation (RAG) System for WonderBot
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

# Try to import RAG dependencies, with fallback
try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from openai import OpenAI
    RAG_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ RAG dependencies not available: {e}")
    print("🔧 Falling back to basic response generation")
    RAG_AVAILABLE = False

class RAGSystem:
    def __init__(self):
        """Initialize the RAG system with vector database and embedding model."""
        if not RAG_AVAILABLE:
            print("⚠️ RAG system disabled - dependencies not available")
            self.client = None
            self.embedding_model = None
            self.chroma_client = None
            self.collection = None
            return
            
        try:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Initialize embedding model for child-friendly content
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB for vector storage
            self.chroma_client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="wonderbot_knowledge",
                metadata={"description": "Educational content for WonderBot RAG system"}
            )
            
            # Initialize with educational content
            self._initialize_knowledge_base()
            
        except Exception as e:
            print(f"❌ Error initializing RAG system: {e}")
            RAG_AVAILABLE = False
            self.client = None
            self.embedding_model = None
            self.chroma_client = None
            self.collection = None
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with educational content."""
        if self.collection.count() == 0:
            print("🔍 Initializing RAG knowledge base...")
            self._load_educational_content()
    
    def _load_educational_content(self):
        """Load educational content into the vector database."""
        educational_content = [
            # Science
            {
                "content": "The solar system consists of the Sun and the objects that orbit it, including eight planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. The Sun is a star that provides light and heat to Earth.",
                "metadata": {"category": "science", "topic": "solar_system", "age_group": "6-12"}
            },
            {
                "content": "Photosynthesis is the process by which plants make their own food using sunlight, water, and carbon dioxide. This process produces oxygen that humans and animals need to breathe.",
                "metadata": {"category": "science", "topic": "photosynthesis", "age_group": "6-12"}
            },
            {
                "content": "The water cycle describes how water moves through the environment. It includes evaporation (water turning to vapor), condensation (vapor forming clouds), and precipitation (rain, snow, or hail falling).",
                "metadata": {"category": "science", "topic": "water_cycle", "age_group": "6-12"}
            },
            {
                "content": "Animals can be classified into different groups: mammals (have fur, give birth to live young), birds (have feathers, lay eggs), reptiles (have scales, lay eggs), amphibians (live in water and land), and fish (live in water, have gills).",
                "metadata": {"category": "science", "topic": "animal_classification", "age_group": "6-12"}
            },
            
            # Geography
            {
                "content": "The Earth has seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia. Each continent has unique features like mountains, rivers, and different types of plants and animals.",
                "metadata": {"category": "geography", "topic": "continents", "age_group": "6-12"}
            },
            {
                "content": "Mountains are formed when Earth's tectonic plates move and push against each other. The highest mountain in the world is Mount Everest, which is 29,029 feet tall.",
                "metadata": {"category": "geography", "topic": "mountains", "age_group": "6-12"}
            },
            {
                "content": "Oceans cover about 71% of Earth's surface. The five main oceans are the Pacific, Atlantic, Indian, Southern, and Arctic oceans. The Pacific Ocean is the largest and deepest.",
                "metadata": {"category": "geography", "topic": "oceans", "age_group": "6-12"}
            },
            
            # History
            {
                "content": "Ancient Egypt was one of the first civilizations, known for building pyramids, creating hieroglyphics (picture writing), and having pharaohs as rulers. The Great Pyramid of Giza is one of the Seven Wonders of the Ancient World.",
                "metadata": {"category": "history", "topic": "ancient_egypt", "age_group": "6-12"}
            },
            {
                "content": "The Roman Empire was one of the largest empires in history. Romans built roads, aqueducts (water systems), and famous buildings like the Colosseum. They also created the calendar we use today.",
                "metadata": {"category": "history", "topic": "roman_empire", "age_group": "6-12"}
            },
            
            # Math
            {
                "content": "Addition is combining numbers to find the total. For example, 2 + 3 = 5. Subtraction is taking away numbers to find the difference. For example, 5 - 2 = 3.",
                "metadata": {"category": "math", "topic": "basic_operations", "age_group": "6-12"}
            },
            {
                "content": "Multiplication is repeated addition. For example, 3 x 4 means adding 3 four times: 3 + 3 + 3 + 3 = 12. Division is sharing equally. For example, 12 ÷ 3 = 4 means sharing 12 items among 3 groups.",
                "metadata": {"category": "math", "topic": "multiplication_division", "age_group": "6-12"}
            },
            
            # Technology
            {
                "content": "Computers are machines that can process information quickly. They have parts like a CPU (brain), memory (storage), and input devices like keyboards and mice. The internet connects computers around the world.",
                "metadata": {"category": "technology", "topic": "computers", "age_group": "6-12"}
            },
            {
                "content": "Robots are machines that can perform tasks automatically. Some robots help in factories, others explore space, and some help with household chores. They are programmed with instructions to follow.",
                "metadata": {"category": "technology", "topic": "robots", "age_group": "6-12"}
            }
        ]
        
        # Add content to vector database
        for i, item in enumerate(educational_content):
            self.collection.add(
                documents=[item["content"]],
                metadatas=[item["metadata"]],
                ids=[f"doc_{i}"]
            )
        
        print(f"✅ Loaded {len(educational_content)} educational documents into RAG system")
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a given query."""
        if not RAG_AVAILABLE or not self.collection:
            print("⚠️ RAG system not available, returning empty context")
            return []
            
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            contexts = []
            for i in range(len(results["documents"][0])):
                contexts.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity_score": 1 - results["distances"][0][i]  # Convert distance to similarity
                })
            
            return contexts
            
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return []
    
    def generate_rag_response(self, query: str, age: Optional[int] = None, interests: Optional[str] = None) -> Dict[str, Any]:
        """Generate a response using RAG with retrieved context."""
        if not RAG_AVAILABLE or not self.client:
            print("⚠️ RAG system not available, using fallback response")
            return {
                "response": "I'm here to help you learn! What would you like to know about?",
                "sources": [],
                "confidence": 0.5
            }
            
        try:
            # Retrieve relevant context
            contexts = self.retrieve_relevant_context(query)
            
            if not contexts:
                return {
                    "response": "I don't have specific information about that, but I'd be happy to help you learn more!",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Build context string
            context_text = "\n\n".join([ctx["content"] for ctx in contexts])
            
            # Create age-appropriate prompt
            age_group = "6-8" if age and age <= 8 else "9-12" if age and age <= 12 else "6-12"
            
            prompt = f"""You are WonderBot, a friendly and educational AI assistant for children aged {age_group}.

Context information:
{context_text}

Child's question: {query}

Please provide a clear, engaging, and educational response that:
1. Uses simple, age-appropriate language
2. Includes interesting facts from the context
3. Encourages curiosity and learning
4. Is fun and interactive
5. Relates to the child's interests if mentioned: {interests or 'general curiosity'}

Keep your response under 200 words and make it engaging for a child."""

            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are WonderBot, a friendly educational assistant for children."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            generated_response = response.choices[0].message.content.strip()
            
            # Calculate confidence based on context similarity
            avg_similarity = sum(ctx["similarity_score"] for ctx in contexts) / len(contexts)
            confidence = min(avg_similarity * 1.2, 1.0)  # Boost confidence slightly
            
            return {
                "response": generated_response,
                "sources": [ctx["metadata"] for ctx in contexts],
                "confidence": confidence,
                "context_used": contexts
            }
            
        except Exception as e:
            print(f"❌ Error generating RAG response: {e}")
            return {
                "response": "I'm having trouble finding information about that right now. Let's explore something else together!",
                "sources": [],
                "confidence": 0.0
            }
    
    def add_knowledge(self, content: str, category: str, topic: str, age_group: str = "6-12") -> bool:
        """Add new knowledge to the RAG system."""
        try:
            doc_id = f"doc_{uuid.uuid4().hex[:8]}"
            
            self.collection.add(
                documents=[content],
                metadatas=[{
                    "category": category,
                    "topic": topic,
                    "age_group": age_group,
                    "added_date": datetime.now().isoformat()
                }],
                ids=[doc_id]
            )
            
            print(f"✅ Added new knowledge: {topic} ({category})")
            return True
            
        except Exception as e:
            print(f"❌ Error adding knowledge: {e}")
            return False
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        if not RAG_AVAILABLE or not self.collection:
            return {
                "status": "disabled",
                "message": "RAG system not available - dependencies missing",
                "total_documents": 0,
                "categories": {}
            }
            
        try:
            total_docs = self.collection.count()
            
            # Get sample of documents to analyze categories
            sample_results = self.collection.get(limit=total_docs)
            categories = {}
            
            for metadata in sample_results["metadatas"]:
                category = metadata.get("category", "unknown")
                categories[category] = categories.get(category, 0) + 1
            
            return {
                "status": "active",
                "total_documents": total_docs,
                "categories": categories,
                "collection_name": self.collection.name
            }
            
        except Exception as e:
            print(f"❌ Error getting knowledge stats: {e}")
            return {"error": str(e)}

# Global RAG system instance
rag_system = RAGSystem() 