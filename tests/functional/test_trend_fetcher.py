"""
Test Suite for Trend Fetcher

Asserts that the trend data structure matches the API contract
as specified in specs/technical.md.

Assignment Requirement: Task 3.1
Status: FAILING (TDD approach - implement trend fetcher to make these pass)
"""

import pytest
from datetime import datetime


# THIS IMPORT WILL FAIL - That's expected! (TDD)
try:
    from src.perception.trend_fetcher import TrendFetcher
    from src.schemas.trend import Trend, TrendResponse
except ImportError:
    # Tests will fail initially - that's the point of TDD!
    pass


class TestTrendDataStructure:
    """Test that trend data matches the API contract from technical.md."""
    
    def test_trend_response_has_required_fields(self):
        """
        API Contract: TrendResponse must have trends list and retrieved_at timestamp.
        
        Given: A TrendResponse object
        When: Accessing fields
        Then: Required fields must be present
        """
        # Arrange & Act
        response = TrendResponse(
            trends=[],
            retrieved_at=datetime.utcnow()
        )
        
        # Assert
        assert hasattr(response, 'trends'), "TrendResponse must have 'trends' field"
        assert hasattr(response, 'retrieved_at'), "TrendResponse must have 'retrieved_at' field"
        assert isinstance(response.trends, list), "'trends' must be a list"
        assert isinstance(response.retrieved_at, datetime), "'retrieved_at' must be datetime"
    
    def test_trend_object_has_required_fields(self):
        """
        API Contract: Trend object must have topic, relevance_score, source, and url.
        
        Given: A Trend object
        When: Creating with required fields
        Then: All fields must be present and correct type
        """
        # Arrange & Act
        trend = Trend(
            topic="Ethiopian fashion trends 2026",
            relevance_score=0.92,
            source="Fashion Industry News",
            url="https://example.com/article"
        )
        
        # Assert
        assert trend.topic == "Ethiopian fashion trends 2026"
        assert trend.relevance_score == 0.92
        assert trend.source == "Fashion Industry News"
        assert trend.url == "https://example.com/article"
    
    def test_relevance_score_is_between_zero_and_one(self):
        """
        API Contract: relevance_score must be float between 0.0 and 1.0.
        
        Given: Trend with relevance score
        When: Score is validated
        Then: Must be in valid range
        """
        # Arrange & Act
        trend = Trend(
            topic="Test topic",
            relevance_score=0.85,
            source="Test source",
            url="https://example.com"
        )
        
        # Assert
        assert 0.0 <= trend.relevance_score <= 1.0, "relevance_score must be between 0.0 and 1.0"
        assert isinstance(trend.relevance_score, float), "relevance_score must be float"
    
    def test_relevance_score_validation_rejects_invalid_values(self):
        """
        API Contract: relevance_score outside 0.0-1.0 range should raise error.
        
        Given: Trend with invalid relevance score
        When: Creating Trend object
        Then: ValidationError should be raised
        """
        # Act & Assert - score too high
        with pytest.raises(Exception):  # Pydantic ValidationError
            Trend(
                topic="Test",
                relevance_score=1.5,  # Invalid: > 1.0
                source="Test",
                url="https://example.com"
            )
        
        # Act & Assert - score too low
        with pytest.raises(Exception):  # Pydantic ValidationError
            Trend(
                topic="Test",
                relevance_score=-0.1,  # Invalid: < 0.0
                source="Test",
                url="https://example.com"
            )
    
    def test_url_must_be_valid_format(self):
        """
        API Contract: url must be valid HTTP/HTTPS URL.
        
        Given: Trend with URL
        When: URL is validated
        Then: Must start with http:// or https://
        """
        # Arrange & Act
        trend = Trend(
            topic="Test topic",
            relevance_score=0.75,
            source="Test source",
            url="https://example.com/article"
        )
        
        # Assert
        assert trend.url.startswith("http://") or trend.url.startswith("https://"), \
            "URL must be valid HTTP/HTTPS"


class TestTrendFetcherAPI:
    """Test TrendFetcher class API contract."""
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_accepts_niche_parameter(self):
        """
        API Contract: TrendFetcher.fetch() must accept 'niche' parameter.
        
        Given: TrendFetcher instance
        When: Calling fetch() with niche
        Then: Should accept the parameter without error
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act & Assert - should not raise error
        try:
            result = await fetcher.fetch(niche="fashion")
            assert result is not None, "fetch() should return a result"
        except TypeError as e:
            pytest.fail(f"fetch() should accept 'niche' parameter: {e}")
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_accepts_time_window_parameter(self):
        """
        API Contract: TrendFetcher.fetch() must accept 'time_window' parameter.
        
        Given: TrendFetcher instance
        When: Calling fetch() with time_window
        Then: Should accept the parameter
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act & Assert
        try:
            result = await fetcher.fetch(
                niche="fashion",
                time_window="24h"
            )
            assert result is not None
        except TypeError as e:
            pytest.fail(f"fetch() should accept 'time_window' parameter: {e}")
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_accepts_min_relevance_parameter(self):
        """
        API Contract: TrendFetcher.fetch() must accept 'min_relevance' parameter.
        
        Given: TrendFetcher instance
        When: Calling fetch() with min_relevance
        Then: Should accept the parameter
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act & Assert
        try:
            result = await fetcher.fetch(
                niche="fashion",
                time_window="24h",
                min_relevance=0.75
            )
            assert result is not None
        except TypeError as e:
            pytest.fail(f"fetch() should accept 'min_relevance' parameter: {e}")
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_returns_trend_response_object(self):
        """
        API Contract: TrendFetcher.fetch() must return TrendResponse object.
        
        Given: TrendFetcher instance
        When: Calling fetch()
        Then: Should return TrendResponse object
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act
        result = await fetcher.fetch(niche="fashion")
        
        # Assert
        assert isinstance(result, TrendResponse), \
            "fetch() must return TrendResponse object"
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_returns_list_of_trends(self):
        """
        API Contract: TrendResponse.trends must be list of Trend objects.
        
        Given: TrendFetcher instance
        When: Calling fetch()
        Then: Response should contain list of Trend objects
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act
        result = await fetcher.fetch(niche="fashion")
        
        # Assert
        assert isinstance(result.trends, list), "trends must be a list"
        # If any trends returned, they must be Trend objects
        if result.trends:
            assert all(isinstance(t, Trend) for t in result.trends), \
                "All items in trends list must be Trend objects"
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_filters_by_min_relevance(self):
        """
        API Contract: TrendFetcher must filter trends by min_relevance.
        
        Given: TrendFetcher with min_relevance=0.80
        When: Calling fetch()
        Then: All returned trends must have relevance >= 0.80
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act
        result = await fetcher.fetch(
            niche="fashion",
            min_relevance=0.80
        )
        
        # Assert
        if result.trends:
            for trend in result.trends:
                assert trend.relevance_score >= 0.80, \
                    f"Trend '{trend.topic}' has relevance {trend.relevance_score} < 0.80"


class TestTrendFetcherEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_handles_empty_niche(self):
        """
        Edge case: Empty niche string should raise error.
        
        Given: TrendFetcher instance
        When: Calling fetch() with empty niche
        Then: Should raise ValueError
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act & Assert
        with pytest.raises(ValueError):
            await fetcher.fetch(niche="")
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_handles_invalid_time_window(self):
        """
        Edge case: Invalid time_window should raise error.
        
        Given: TrendFetcher instance
        When: Calling fetch() with invalid time_window
        Then: Should raise ValueError
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act & Assert
        with pytest.raises(ValueError):
            await fetcher.fetch(
                niche="fashion",
                time_window="invalid"  # Not one of: 1h, 6h, 24h, 7d
            )
    
    @pytest.mark.asyncio
    async def test_trend_fetcher_returns_empty_list_when_no_trends(self):
        """
        Edge case: When no trends found, should return empty list (not None).
        
        Given: TrendFetcher instance
        When: No trends match criteria
        Then: Should return TrendResponse with empty trends list
        """
        # Arrange
        fetcher = TrendFetcher()
        
        # Act
        result = await fetcher.fetch(
            niche="obscure_topic_12345",
            min_relevance=0.99  # Very high threshold
        )
        
        # Assert
        assert result is not None, "Should return TrendResponse, not None"
        assert isinstance(result.trends, list), "trends should be list"
        # Empty list is acceptable
        assert len(result.trends) >= 0, "trends list can be empty"


class TestTrendSerialization:
    """Test that trends can be serialized/deserialized."""
    
    def test_trend_to_dict(self):
        """
        API Contract: Trend must be serializable to dict.
        
        Given: A Trend object
        When: Converting to dict
        Then: All fields should be present
        """
        # Arrange
        trend = Trend(
            topic="Test topic",
            relevance_score=0.85,
            source="Test source",
            url="https://example.com"
        )
        
        # Act
        trend_dict = trend.model_dump()  # Pydantic v2
        
        # Assert
        assert "topic" in trend_dict
        assert "relevance_score" in trend_dict
        assert "source" in trend_dict
        assert "url" in trend_dict
    
    def test_trend_to_json(self):
        """
        API Contract: Trend must be serializable to JSON.
        
        Given: A Trend object
        When: Converting to JSON
        Then: Valid JSON string should be produced
        """
        # Arrange
        trend = Trend(
            topic="Test topic",
            relevance_score=0.85,
            source="Test source",
            url="https://example.com"
        )
        
        # Act
        trend_json = trend.model_dump_json()  # Pydantic v2
        
        # Assert
        assert isinstance(trend_json, str)
        assert "Test topic" in trend_json
        assert "0.85" in trend_json
    
    def test_trend_from_dict(self):
        """
        API Contract: Trend must be creatable from dict.
        
        Given: A dict with trend data
        When: Creating Trend object
        Then: Object should be created successfully
        """
        # Arrange
        trend_dict = {
            "topic": "Test topic",
            "relevance_score": 0.85,
            "source": "Test source",
            "url": "https://example.com"
        }
        
        # Act
        trend = Trend(**trend_dict)
        
        # Assert
        assert trend.topic == "Test topic"
        assert trend.relevance_score == 0.85


# ============================================================================
# EXPECTED TEST RESULTS
# ============================================================================
"""
When you run: pytest tests/functional/test_trend_fetcher.py

Expected output:
================= FAILURES =================
test_trend_response_has_required_fields - ImportError: No module named 'src.perception.trend_fetcher'
test_trend_object_has_required_fields - ImportError: No module named 'src.schemas.trend'
test_trend_fetcher_accepts_niche_parameter - ImportError
... (all tests fail with ImportError)

This is CORRECT for TDD!

Next step: 
1. Create src/schemas/trend.py with Trend and TrendResponse models
2. Create src/perception/trend_fetcher.py with TrendFetcher class
3. Implement according to API contract
4. Re-run tests - they should pass!
"""
