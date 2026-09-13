"""Tests for the mock provider."""

import pytest
from app.providers import (
    provision_server, destroy_server, start_server,
    stop_server, restart_server, generate_mock_ip,
)


@pytest.mark.asyncio
async def test_provision_returns_ips():
    result = await provision_server("test", "us-east-1", "ubuntu-24.04")
    assert "provider_id" in result
    assert "ipv4" in result
    assert "ipv6" in result
    assert result["provider_id"].startswith("srv-")


@pytest.mark.asyncio
async def test_destroy_returns_true():
    assert await destroy_server("srv-test123") is True


@pytest.mark.asyncio
async def test_start_stop_restart():
    assert await start_server("srv-test123") is True
    assert await stop_server("srv-test123") is True
    assert await restart_server("srv-test123") is True


def test_generate_mock_ip():
    ip = generate_mock_ip()
    parts = ip.split(".")
    assert len(parts) == 4
    assert all(0 <= int(p) <= 255 for p in parts)
