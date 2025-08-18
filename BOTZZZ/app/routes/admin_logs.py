# file: app/routes/admin_logs.py
from fastapi import APIRouter, Depends, Query, Header, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
from typing import Optional
import os
import httpx
import re

router = APIRouter(prefix="/admin/logs", tags=["admin-logs"])

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme_admin_token_123")
SMM_PANEL_URL = os.getenv("SMM_PANEL_URL", "https://example-smm-panel.com/api/v2")
SMM_API_KEY = os.getenv("SMM_API_KEY", "your_smm_api_key_here")

def verify_admin_token(x_token: Optional[str] = Header(None)):
    if x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")

@router.get("/boosts", summary="View boost logs with optional filters")
def get_boost_logs(
    username: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_retries: Optional[int] = Query(None),
    _: str = Depends(verify_admin_token)
):
    conn = sqlite3.connect("logs/boost_logs.db")
    c = conn.cursor()
    query = "SELECT id, username, amount, status, message, retry_count, before_count, after_count, source_url, created_at FROM boost_logs WHERE 1=1"
    params = []
    if username:
        query += " AND username = ?"
        params.append(username)
    if status:
        query += " AND status = ?"
        params.append(status)
    if min_retries is not None:
        query += " AND retry_count >= ?"
        params.append(min_retries)
    query += " ORDER BY created_at DESC LIMIT 100"
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return JSONResponse([
        {
            "id": r[0],
            "username": r[1],
            "amount": r[2],
            "status": r[3],
            "message": r[4],
            "retry_count": r[5],
            "before_count": r[6],
            "after_count": r[7],
            "source_url": r[8],
            "created_at": r[9]
        }
        for r in rows
    ])

@router.get("/stats/hosts", summary="Host performance stats")
def get_host_stats(_: str = Depends(verify_admin_token)):
    conn = sqlite3.connect("logs/boost_logs.db")
    c = conn.cursor()
    c.execute("SELECT source_url, success_count, error_count, cooldown_count FROM host_stats ORDER BY success_count DESC")
    rows = c.fetchall()
    conn.close()
    return JSONResponse([
        {
            "source_url": r[0],
            "success": r[1],
            "errors": r[2],
            "cooldowns": r[3],
            "success_rate": round((r[1] / max(r[1] + r[2] + r[3], 1)) * 100, 2)
        }
        for r in rows
    ])

@router.post("/smm/order", summary="Order followers from SMM panel")
def order_smm_followers(
    username: str = Query(...),
    amount: int = Query(...),
    _: str = Depends(verify_admin_token)
):
    payload = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": 1,
        "link": f"https://www.tiktok.com/@{username}",
        "quantity": amount
    }
    try:
        response = httpx.post(SMM_PANEL_URL, data=payload, timeout=15)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.get("/zefoy/mirrors", summary="Discover Zefoy mirror links")
def get_zefoy_mirrors(_: str = Depends(verify_admin_token)):
    try:
        search_url = "https://html.duckduckgo.com/html/?q=site:zefoy.com+followers"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(search_url, headers=headers)
        links = list(set(re.findall(r'href=\"(https://[^"]*zefoy[^"]*)\"', response.text)))[:10]

        working = []
        for url in links:
            try:
                r = httpx.get(url, headers=headers, timeout=5)
                if r.status_code == 200 and ("Followers" in r.text or "captcha" in r.text):
                    working.append(url)
            except Exception:
                continue

        return {"working_mirrors": working, "total_checked": len(links)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
