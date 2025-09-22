import pytest
from unittest.mock import AsyncMock, patch
import aiohttp
from src.timeAnalyzer.core.exceptions import ValidationError, NetworkError, TimeServiceError


class TestTimeService:
    @pytest.mark.asyncio
    async def test_successful_fetch_time_data(self, time_service, mock_session, sample_time_data):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = sample_time_data.raw_data
        mock_session.get.return_value.__aenter__.return_value = mock_response

        result = await time_service.fetch_time_data("213")

        assert result.timestamp == sample_time_data.timestamp
        assert result.timezone_name == "Москва"
        assert result.offset_string == "UTC+3:00"
        mock_session.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_time_data_validation_error(self, time_service, mock_session):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"invalid": "data"}  # Missing required fields
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with pytest.raises(ValidationError, match="Некорректные данные от API"):
            await time_service.fetch_time_data("213")

    @pytest.mark.asyncio
    async def test_fetch_time_data_http_error(self, time_service, mock_session):
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError(
            request_info=None, history=None, status=500
        )
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with pytest.raises(NetworkError):
            await time_service.fetch_time_data("213")

    def test_validate_time_data_valid(self, time_service, sample_time_data):
        assert time_service._validate_time_data(sample_time_data.raw_data) is True

    def test_validate_time_data_invalid(self, time_service):
        invalid_data = [
            {},
            {"time": "invalid"},
            {"clocks": {}},
            {"time": None, "clocks": {}}
        ]

        for data in invalid_data:
            assert time_service._validate_time_data(data) is False

    def test_parse_time_data(self, time_service, sample_time_data):
        parsed_data = time_service._parse_time_data(sample_time_data.raw_data, "213")

        assert parsed_data.timestamp == sample_time_data.timestamp
        assert parsed_data.timezone_name == "Москва"
        assert parsed_data.offset_string == "UTC+3:00"
        assert parsed_data.raw_data == sample_time_data.raw_data