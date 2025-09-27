"""
Tests for authentication functionality
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock

from main import app
from app.models import User, UserRole
from app.auth import get_password_hash, verify_password, create_access_token

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
async def db_session():
    """Database session fixture"""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Test user fixture"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        first_name="Test",
        last_name="User",
        role=UserRole.CASEWORKER,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

class TestPasswordHashing:
    """Test password hashing functionality"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Hash should be a string
        assert isinstance(hashed, str)
        
        # Hash should start with bcrypt identifier
        assert hashed.startswith("$2b$")
    
    def test_password_verification(self):
        """Test password verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Correct password should verify
        assert verify_password(password, hashed) is True
        
        # Wrong password should not verify
        assert verify_password("wrongpassword", hashed) is False
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2

class TestTokenCreation:
    """Test JWT token creation"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser", "role": "caseworker"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Token should have three parts (header.payload.signature)
        parts = token.split(".")
        assert len(parts) == 3
    
    def test_token_with_expiration(self):
        """Test token creation with custom expiration"""
        from datetime import timedelta
        
        data = {"sub": "testuser", "role": "caseworker"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0

class TestUserRegistration:
    """Test user registration"""
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
            "role": "caseworker"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["role"] == user_data["role"]
        assert "id" in data
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_register_user_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        user_data = {
            "email": "different@example.com",
            "username": "testuser",  # Same as existing user
            "password": "password123",
            "first_name": "Different",
            "last_name": "User",
            "role": "caseworker"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "Username already registered" in data["detail"]
    
    def test_register_user_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        user_data = {
            "email": "test@example.com",  # Same as existing user
            "username": "differentuser",
            "password": "password123",
            "first_name": "Different",
            "last_name": "User",
            "role": "caseworker"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "Email already registered" in data["detail"]
    
    def test_register_user_invalid_data(self, client):
        """Test registration with invalid data"""
        user_data = {
            "email": "invalid-email",
            "username": "",
            "password": "123",  # Too short
            "first_name": "",
            "last_name": "",
            "role": "invalid_role"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

class TestUserLogin:
    """Test user login"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
        
        data = response.json()
        assert "Incorrect username or password" in data["detail"]
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
        
        data = response.json()
        assert "Incorrect username or password" in data["detail"]
    
    def test_login_inactive_user(self, client, db_session):
        """Test login with inactive user"""
        # Create inactive user
        inactive_user = User(
            email="inactive@example.com",
            username="inactive",
            hashed_password=get_password_hash("password123"),
            first_name="Inactive",
            last_name="User",
            role=UserRole.CLIENT,
            is_active=False,
            is_verified=True
        )
        db_session.add(inactive_user)
        await db_session.commit()
        
        login_data = {
            "username": "inactive",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "Inactive user" in data["detail"]

class TestCurrentUser:
    """Test current user functionality"""
    
    def test_get_current_user_success(self, client, test_user):
        """Test getting current user with valid token"""
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "hashed_password" not in data
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_get_current_user_expired_token(self, client):
        """Test getting current user with expired token"""
        # Create expired token
        from datetime import datetime, timedelta
        import jwt
        import os
        
        secret_key = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-here-change-in-production")
        expired_time = datetime.utcnow() - timedelta(hours=1)
        
        token_data = {
            "sub": "testuser",
            "role": "caseworker",
            "exp": expired_time
        }
        
        expired_token = jwt.encode(token_data, secret_key, algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401

class TestPasswordChange:
    """Test password change functionality"""
    
    def test_change_password_success(self, client, test_user):
        """Test successful password change"""
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Change password
        headers = {"Authorization": f"Bearer {token}"}
        change_data = {
            "current_password": "password123",
            "new_password": "newpassword123"
        }
        
        response = client.post("/api/v1/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "Password changed successfully" in data["message"]
    
    def test_change_password_wrong_current(self, client, test_user):
        """Test password change with wrong current password"""
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Try to change password with wrong current password
        headers = {"Authorization": f"Bearer {token}"}
        change_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        
        response = client.post("/api/v1/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 400
        
        data = response.json()
        assert "Incorrect current password" in data["detail"]

class TestLogout:
    """Test logout functionality"""
    
    def test_logout_success(self, client, test_user):
        """Test successful logout"""
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/v1/auth/logout", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "Successfully logged out" in data["message"]

class TestRoleBasedAccess:
    """Test role-based access control"""
    
    def test_admin_access(self, client, db_session):
        """Test admin user access"""
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        db_session.add(admin_user)
        await db_session.commit()
        
        # Login as admin
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Test admin access
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["role"] == "admin"
    
    def test_caseworker_access(self, client, test_user):
        """Test caseworker user access"""
        # Login as caseworker
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        token = login_response.json()["access_token"]
        
        # Test caseworker access
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["role"] == "caseworker"

@pytest.mark.asyncio
async def test_authentication_flow():
    """Test complete authentication flow"""
    client = TestClient(app)
    
    # 1. Register user
    user_data = {
        "email": "flowtest@example.com",
        "username": "flowtest",
        "password": "password123",
        "first_name": "Flow",
        "last_name": "Test",
        "role": "caseworker"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # 2. Login user
    login_data = {
        "username": "flowtest",
        "password": "password123"
    }
    
    login_response = client.post("/api/v1/auth/token", data=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    # 3. Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    
    # 4. Change password
    change_data = {
        "current_password": "password123",
        "new_password": "newpassword123"
    }
    
    change_response = client.post("/api/v1/auth/change-password", json=change_data, headers=headers)
    assert change_response.status_code == 200
    
    # 5. Login with new password
    new_login_data = {
        "username": "flowtest",
        "password": "newpassword123"
    }
    
    new_login_response = client.post("/api/v1/auth/token", data=new_login_data)
    assert new_login_response.status_code == 200
    
    # 6. Logout
    logout_response = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_response.status_code == 200
