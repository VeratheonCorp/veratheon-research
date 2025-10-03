"""RAG operations for embeddings and research_docs integration."""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from src.lib.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseRAG:
    """RAG operations for research documents with vector embeddings."""

    def __init__(self):
        """Initialize Supabase RAG client."""
        self._client = None

    @property
    def client(self):
        """Get Supabase client connection."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    def add_document(
        self,
        content: str,
        title: str,
        symbol: str,
        report_type: str,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        token_count: Optional[int] = None
    ) -> bool:
        """
        Add a document to the research_docs table with optional embedding.

        Args:
            content: Document content (markdown/text)
            title: Document title
            symbol: Stock symbol
            report_type: Type of report (e.g., 'comprehensive_report')
            embedding: Optional vector embedding (if None, will be generated later)
            metadata: Optional metadata
            token_count: Optional token count

        Returns:
            True if successful, False otherwise
        """
        try:
            doc_metadata = metadata or {}
            doc_metadata["symbol"] = symbol.upper()
            doc_metadata["report_type"] = report_type

            doc_entry = {
                "content": content,
                "title": title,
                "embedding": embedding,  # Can be None initially
                "metadata": doc_metadata,
                "token_count": token_count
            }

            self.client.table("research_docs").insert(doc_entry).execute()
            logger.info(f"Added document to research_docs: {title} ({symbol})")
            return True

        except Exception as e:
            logger.error(f"Failed to add document for {symbol}: {str(e)}")
            return False

    def update_embedding(
        self,
        doc_id: int,
        embedding: List[float]
    ) -> bool:
        """
        Update the embedding for an existing document.

        Args:
            doc_id: Document ID
            embedding: Vector embedding

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table("research_docs")\
                .update({"embedding": embedding})\
                .eq("id", doc_id)\
                .execute()

            logger.info(f"Updated embedding for document {doc_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update embedding for document {doc_id}: {str(e)}")
            return False

    def search_documents(
        self,
        query_embedding: List[float],
        limit: int = 10,
        symbol_filter: Optional[str] = None,
        report_type_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.

        Note: This requires pgvector extension and similarity functions in Supabase.

        Args:
            query_embedding: Query vector embedding
            limit: Maximum number of results
            symbol_filter: Optional symbol to filter by
            report_type_filter: Optional report type to filter by

        Returns:
            List of matching documents with similarity scores
        """
        try:
            # Note: Vector similarity search requires RPC function in Supabase
            # This is a placeholder - needs to be implemented with Supabase RPC
            # For now, just return recent documents
            query = self.client.table("research_docs")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)

            if symbol_filter:
                query = query.filter("metadata->>symbol", "eq", symbol_filter.upper())

            if report_type_filter:
                query = query.filter("metadata->>report_type", "eq", report_type_filter)

            response = query.execute()
            return response.data if response.data else []

        except Exception as e:
            logger.error(f"Failed to search documents: {str(e)}")
            return []

    def get_documents_by_symbol(
        self,
        symbol: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get all research documents for a symbol.

        Args:
            symbol: Stock symbol
            limit: Maximum number of results

        Returns:
            List of documents
        """
        try:
            response = self.client.table("research_docs")\
                .select("*")\
                .filter("metadata->>symbol", "eq", symbol.upper())\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()

            return response.data if response.data else []

        except Exception as e:
            logger.error(f"Failed to get documents for {symbol}: {str(e)}")
            return []

    def delete_old_documents(self, days: int = 90) -> int:
        """
        Delete documents older than specified days.

        Args:
            days: Number of days to keep

        Returns:
            Number of documents deleted
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            response = self.client.table("research_docs")\
                .delete()\
                .lt("created_at", cutoff_date.isoformat())\
                .execute()

            deleted_count = len(response.data) if response.data else 0
            logger.info(f"Deleted {deleted_count} documents older than {days} days")
            return deleted_count

        except Exception as e:
            logger.error(f"Failed to delete old documents: {str(e)}")
            return 0

# Global RAG instance
_rag_instance = None

def get_supabase_rag() -> SupabaseRAG:
    """Get or create global Supabase RAG instance."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = SupabaseRAG()
    return _rag_instance
