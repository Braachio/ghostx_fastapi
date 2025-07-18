# services/lap_data.py
import pandas as pd
from utils.supabase_client import supabase
from services.insert import fetch_all_controls, fetch_all_vehicle_status

def fetch_lap_meta_and_data(lap_id: str):
    meta = supabase.table("lap_meta").select("*").eq("id", lap_id).single().execute().data
    if not meta:
        return None

    controls = fetch_all_controls(lap_id)
    vehicle = fetch_all_vehicle_status(lap_id)

    try:
        sector_results = supabase.table("sector_results").select("*").eq("lap_id", lap_id).execute().data
    except Exception:
        sector_results = []

    return {
        "meta": meta,
        "controls": controls,
        "vehicle": vehicle,
        "sector_results": sector_results
    }
