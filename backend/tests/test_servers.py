"""Tests for server CRUD and lifecycle endpoints."""

import pytest


@pytest.mark.asyncio
async def test_list_servers_empty(client):
    res = await client.get("/api/v1/servers")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_create_server(client):
    res = await client.post("/api/v1/servers", json={
        "name": "test-server",
        "hostname": "test.shaheen.cloud",
        "plan": "small",
        "region": "us-east-1",
        "image": "ubuntu-24.04",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "test-server"
    assert data["hostname"] == "test.shaheen.cloud"
    assert data["plan"] == "small"
    assert data["status"] == "provisioning"
    assert data["cpu_cores"] == 2
    assert data["memory_mb"] == 2048
    assert data["disk_gb"] == 40


@pytest.mark.asyncio
async def test_get_server_not_found(client):
    res = await client.get("/api/v1/servers/nonexistent-id")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_plans_list(client):
    res = await client.get("/api/v1/plans")
    assert res.status_code == 200
    plans = res.json()
    assert len(plans) == 5
    assert plans[0]["id"] == "micro"


@pytest.mark.asyncio
async def test_regions_list(client):
    res = await client.get("/api/v1/regions")
    assert res.status_code == 200
    regions = res.json()
    assert len(regions) == 5


@pytest.mark.asyncio
async def test_images_list(client):
    res = await client.get("/api/v1/images")
    assert res.status_code == 200
    images = res.json()
    assert len(images) == 3
