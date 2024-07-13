import uuid

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict
from pydantic.v1 import BaseModel, Field, validator

if TYPE_CHECKING:
    from langchain_core.documents import Document as LangChainDocument


class BaseDocument(ABC, BaseModel):
    """A generic interface for documents."""

    doc_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the document.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields.")

    @validator("metadata", pre=True)
    def _validate_metadata(cls, v) -> Dict:
        if v is None:
            return {}
        return v

    @abstractmethod
    def get_content(self) -> str:
        """Get document content."""

    @abstractmethod
    def get_metadata(self) -> str:
        """Get metadata."""


class Document(BaseDocument):
    text: str = Field(default="", description="Text content of the document.")

    @classmethod
    def class_name(cls) -> str:
        return "Document"

    def get_content(self) -> str:
        """Get the text content of the document."""
        return self.text

    def get_metadata(self) -> dict:
        """Get the metadata of the document."""
        return self.metadata

    @classmethod
    def from_langchain_format(cls, doc: "LangChainDocument") -> "Document":
        """
        Convert a document from LangChain  format.

        Args:
            doc (LangChainDocument): Document in LangChain format.
        """
        return cls(text=doc.page_content, metadata=doc.metadata)
