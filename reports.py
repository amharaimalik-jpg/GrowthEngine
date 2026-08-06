from datetime import datetime
import sqlite3
import pandas as pd


def export_executive_report():
  print("=== GrowthEngine V3 - Executive Report Generator ===")
  conn = sqlite3.connect("leads_database.db")
  df = pd.read_sql_query("SELECT * FROM leads", conn)
  conn.close()

  if df.empty:
    print("No data available to generate report.")
    return

  # إنشاء اسم ملف فريد يعتمد على التوقيت الحالي
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  report_filename = f"Executive_Report_{timestamp}.xlsx"

  try:
    # تصدير البيانات إلى ملف إكسيل
    df.to_excel(report_filename, index=False)
    print(
        f"✅ تم بنجاح إنشاء وتصدير التقرير التنفيذي بصيغة Excel باسم:"
        f" {report_filename}"
    )
  except Exception as e:
    # نظام احتياطي في حال تطلب تصدير الإكسيل مكتبات إضافية، نحفظه كـ CSV منظم
    fallback_filename = f"Executive_Report_{timestamp}.csv"
    df.to_csv(fallback_filename, index=False)
    print(
        f"⚠️ تم الحفظ بصيغة CSV الاحترافية بنجاح باسم: {fallback_filename}"
    )

  print("التقرير جاهز الآن تماماً للاستخدام الميداني!")


if __name__ == "__main__":
  export_executive_report()