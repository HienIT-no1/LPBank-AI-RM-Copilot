import os
import pandas as pd
from sqlalchemy import create_engine

# Cấu hình đường dẫn thư mục chứa CSV
output_dir = "Store_data"
os.makedirs(output_dir, exist_ok=True)

# --- BƯỚC 1: TÁCH FILE EXCEL THÀNH CÁC FILE CSV VÀO STORE_DATA ---
excel_file = "Bản sao của LPB_AI_Banking_Realistic_Mock_Data_v2.xlsx"

print("Đang tiến hành tách các sheet thành file CSV...")
sheets = pd.read_excel(excel_file, sheet_name=None)

for sheet_name, df in sheets.items():
  if sheet_name == "DATA_DICTIONARY":
    continue
  file_path = os.path.join(output_dir, f"{sheet_name}.csv")
  df.to_csv(file_path, index=False, encoding="utf-8-sig")
  print(f"Đã lưu: {file_path}")

# --- BƯỚC 2: ĐẨY DỮ LIỆU TỪ STORE_DATA VÀO MYSQL WORKBENCH ---
db_user = "root"
db_password = "123456"
db_host = "localhost"
db_port = "3306"
db_name = "lpb_ai_banking"

engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

print(f"\nĐang đẩy dữ liệu cấu trúc từ '{output_dir}' lên MySQL Workbench...")
for file in os.listdir(output_dir):
  if file.endswith(".csv"):
    table_name = file.replace(".csv", "")
    file_path = os.path.join(output_dir, file)
    df = pd.read_csv(file_path)
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    print(f"Đã nạp thành công bảng: {table_name}")

print("\nHoàn tất toàn bộ quá trình!")