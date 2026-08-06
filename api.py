from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import sqlite3
import random
import string

app = FastAPI()

class UserRegister(BaseModel):
    name: str
    email: str
    referred_by: Optional[str] = None  # كود إحالة الصديق (اختياري)

@app.get("/user/stats/{email}")
def get_user_stats(email: str):
    conn = sqlite3.connect("leads_database.db")
    cursor = conn.cursor()
    
    query = (
        "SELECT name, email, referral_code, referral_count, is_unlocked "
        "FROM users WHERE email = ?"
    )
    cursor.execute(query, (email,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "name": user[0],
        "email": user[1],
        "referral_code": user[2],
        "referral_count": user[3],
        "commission_unlocked": bool(user[4])
    }

@app.post("/user/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    conn = sqlite3.connect("leads_database.db")
    cursor = conn.cursor()
    
    # التحقق مما إذا كان البريد مسجلاً مسبقاً
    cursor.execute("SELECT email FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # توليد رمز إحالة عشوائي فريد للمستخدم الجديد
    ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # معالجة نظام تتبع الإحالات وفتح العمولات تلقائياً (الشرط: 3 إحالات لفتح العمولة)
    if user.referred_by:
        cursor.execute("SELECT email, referral_count FROM users WHERE referral_code = ?", (user.referred_by,))
        referrer = cursor.fetchone()
        if referrer:
            new_count = referrer[1] + 1
            # إذا وصل عدد الإحالات 3 أو أكثر، يتم فتح العمولة تلقائياً
            is_unlocked_val = 1 if new_count >= 3 else 0
            
            cursor.execute(
                "UPDATE users SET referral_count = ?, is_unlocked = ? WHERE referral_code = ?",
                (new_count, is_unlocked_val, user.referred_by)
            )
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email, referral_code, referral_count, is_unlocked) VALUES (?, ?, ?, 0, 0)",
            (user.name, user.email, ref_code)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
        
    conn.close()
    return {
        "message": "User registered successfully with complete growth engine logic",
        "name": user.name,
        "email": user.email,
        "referral_code": ref_code,
        "referred_by": user.referred_by
    }