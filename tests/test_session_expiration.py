# tests/test_session_expiration.py
# SentinelOps — CI Test for 15-minute session expiration

import time
import requests

BASE = "https://crcybercop.dpdns.org"

def test_session_expiration():
    # Step 1: Login
    login_res = requests.post(
        f"{BASE}/auth/login",
        json={"email": "test@example.com", "password": "test"},
        allow_redirects=False
    )
    assert login_res.status_code == 200

    cookies = login_res.cookies

    # Step 2: Verify session is active
    me_res = requests.get(f"{BASE}/api/users/me", cookies=cookies)
    assert me_res.status_code == 200

    # Step 3: Wait 15 minutes
    time.sleep(15 * 60)

    # Step 4: Session should now be expired
    expired_res = requests.get(f"{BASE}/api/users/me", cookies=cookies)
    assert expired_res.status_code == 401
