from fastapi import APIRouter, Request
from utils.api_response import success_response, error_response
from utils.async_handler import async_handler
from config.supabase_client import supabase
from dotenv import load_dotenv
import os
import requests

load_dotenv()
router = APIRouter(prefix="/auth", tags=["Authentication"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# 🟢 SIGN UP
@router.post("/signup")
@async_handler
async def signup_user(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return error_response("Email and password are required", 400)

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not response or not response.user:
            return error_response("Signup failed. Please try again.", 400)

        return success_response(
            {
                "id": response.user.id,
                "email": response.user.email
            },
            "User signed up successfully ✅"
        )

    except Exception as e:
        return error_response(str(e), 400)


# 🟠 LOGIN
@router.post("/login")
@async_handler
async def login_user(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return error_response("Email and password are required", 400)

    try:
        session = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not session or not session.session:
            return error_response("Invalid email or password", 401)

        return success_response(
            {
                "access_token": session.session.access_token,
                "refresh_token": session.session.refresh_token,
                "user": session.session.user
            },
            "Login successful ✅"
        )

    except Exception as e:
        return error_response(str(e), 400)


# 🔵 VERIFY TOKEN
@router.post("/verify")
@async_handler
async def verify_token(request: Request):
    body = await request.json()
    token = body.get("access_token")

    if not token:
        return error_response("Access token required", 400)

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "apikey": SUPABASE_KEY
        }

        res = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)

        if res.status_code == 200:
            return success_response(res.json(), "Token is valid ✅")

        return error_response("Invalid or expired token", 401)

    except Exception as e:
        return error_response(str(e), 400)
