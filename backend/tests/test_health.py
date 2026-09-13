"""Tests for the health endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_returns_200(client):
    res = await client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "version" in data
    assert "redis_connected" in data
    assert "worker_active" in data


@pytest.mark.asyncio
async def test_root_returns_info(client):
    res = await client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "name" in data
    assert "version" in data
