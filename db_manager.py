# db_manager.py
import sqlite3
import os

DB_NAME = "growth_engine.db"

def init_db():
    """إنشاء قاعدة البيانات وجدول العملاء إذا لم يكن موجوداً"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            niche TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_leads_to_db(leads_list):
    """حفظ العملاء الجدد داخل قاعدة البيانات"""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # مسح القديم لتجديد القائمة الحية
    cursor.execute("DELETE FROM leads")
    for lead in leads_list:
        cursor.execute('''
            INSERT INTO leads (name, email, niche, status)
            VALUES (?, ?, ?, ?)
        ''', (lead['name'], lead['email'], lead['niche'], lead['status']))
    conn.commit()
    conn.close()
    print(f"[+] Successfully saved {len(leads_list)} leads to SQLite Database ({DB_NAME})!")

def mark_all_as_paid():
    """تحديث حالة جميع العملاء إلى مدفوع عند اكتمال التحصيل"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = 'Paid'")
    conn.commit()
    conn.close()

def get_all_leads():
    """استرجاع كافة العملاء من قاعدة البيانات"""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, niche, status FROM leads")
    rows = cursor.fetchall()
    conn.close()
    return rows