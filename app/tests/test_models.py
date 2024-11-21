from datetime import datetime
from bson import ObjectId
from pydantic import ValidationError
import pytest
from app.models import Content

class TestContentModel:
    def test_content_creation(self):
        content = Content(
            title="Test Content",
            description="Test Description",
            content_type="article",
            tags=["test"]
        )
        assert content.title == "Test Content"
        assert content.content_type == "article"
        assert isinstance(content.created_at, datetime)

    def test_invalid_title_length(self):
        with pytest.raises(ValidationError):
            Content(
                title="",  # Empty title should fail
                description="Test",
                content_type="article"
            )

    def test_tags_validation(self):
        content = Content(
            title="Test",
            description="Test",
            content_type="article",
            tags=["test", "validation"]
        )
        assert len(content.tags) == 2
        assert "test" in content.tags

    def test_status_transitions(self):
        content = Content(
            title="Test",
            description="Test",
            content_type="article",
            status="draft"
        )
        assert content.status == "draft"
        
        with pytest.raises(ValidationError):
            content.status = "invalid_status"

    def test_url_validation(self):
        content = Content(
            title="Test",
            description="Test",
            content_type="article",
            url="https://example.com/"
        )
        assert str(content.url).rstrip('/') == "https://example.com"
        
        with pytest.raises(ValidationError):
            Content(
                title="Test",
                description="Test",
                content_type="article",
                url="not-a-url"
            )
    def test_bson_id_serialization(self):
        object_id = ObjectId()
        content = Content(
            _id=object_id,
            title="Test",
            description="Test",
            content_type="article"
        )
        assert str(content._id) == str(object_id)