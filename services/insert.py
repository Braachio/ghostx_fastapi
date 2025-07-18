import pandas as pd
from utils.supabase_client import supabase
import csv
from io import StringIO

# ✅ 트랙/차량 이름 추출 (Venue, Vehicle 기준)
def extract_value(lines, keyword):
    for line in lines:
        try:
            row = next(csv.reader([line.strip()]))
            if len(row) > 1 and row[0].strip('"').strip().lower() == keyword.lower():
                return row[1].strip('"').strip()
        except Exception:
            continue
    return "알 수 없음"



def chunked_insert(table_name: str, records: list, chunk_size: int = 100):
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        try:
            res = supabase.table(table_name).insert(chunk).execute()
            if not res.data:
                print(f"❌ {table_name} insert 실패 (chunk {i // chunk_size}): 응답 없음")
            else:
                print(f"✅ {table_name} insert 성공 (chunk {i // chunk_size}, {len(chunk)} rows)")
        except Exception as e:
            print(f"❌ {table_name} insert 예외 발생 (chunk {i // chunk_size}): {repr(e)}")



def chunked_insert_lap_raw(lap_id: str, df: pd.DataFrame, chunk_size: int = 100):
    records = df.to_dict(orient="records")
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        res = supabase.table("lap_raw").insert({
            "lap_id": lap_id,
            "chunk_index": i // chunk_size,
            "data": chunk
        }).execute()
        if not res.data:
            print(f"❌ lap_raw insert 실패 (chunk {i // chunk_size})")
        else:
            print(f"✅ lap_raw chunk {i // chunk_size} 삽입 성공 ({len(chunk)}개)")


def fetch_all_controls(lap_id: str, page_size: int = 1000) -> list:
    all_data = []
    for offset in range(0, 100000, page_size):
        response = (
            supabase
            .table("lap_controls")
            .select("*")
            .eq("lap_id", lap_id)
            .order("time")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        chunk = response.data or []
        all_data.extend(chunk)

        # 🔚 마지막 페이지인 경우 break
        if len(chunk) < page_size:
            break
    print(f"🔍 전체 가져온 lap_controls 수: {len(all_data)}")
    return all_data



def fetch_all_vehicle_status(lap_id: str, page_size: int = 1000) -> list:
    all_data = []
    for offset in range(0, 100000, page_size):
        response = (
            supabase
            .table("lap_vehicle_status")
            .select("*")
            .eq("lap_id", lap_id)
            .order("time")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        chunk = response.data or []
        all_data.extend(chunk)

        # 🔚 마지막 페이지이면 종료
        if len(chunk) < page_size:
            break

    print(f"🔍 전체 가져온 lap_vehicle_status 수: {len(all_data)}")
    return all_data

