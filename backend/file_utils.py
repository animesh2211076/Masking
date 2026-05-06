import os
import json
from typing import List, Dict, Any
from datetime import datetime
from fastapi import HTTPException

from config import MASKED_LOG_FILE


# def ensure_user_data_file_exists():

#     if not os.path.exists(USER_DATA_FILE):
#         sample_data = [
#             {
#                 "id": 101,
#                 "name": "Animesh Maurya",
#                 "phone": "9876543210",
#                 "email": "animesh@gmail.com",
#                 "pan": "ABCDE1234F",
#                 "ifsc": "SBIN0001234",
#                 "upi": "animesh@upi",
#                 "account": "123456789012",
#                 "balance": 5400,
#             },
#             {
#                 "id": 102,
#                 "name": "Rahul Sharma",
#                 "phone": "9123456789",
#                 "email": "rahul@gmail.com",
#                 "pan": "PQRSX6789Z",
#                 "ifsc": "HDFC0005678",
#                 "upi": "rahul@okhdfcbank",
#                 "account": "987654321098",
#                 "balance": 8900,
#             },
#         ]

#         with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
#             json.dump(sample_data, f, indent=2)


# def read_users_from_file() -> List[Dict[str, Any]]:

#     ensure_user_data_file_exists()

#     try:
#         with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=500, detail="user_data.txt is corrupted (invalid JSON).")


def write_masked_log(role: str, route: str, masked_payload: Any):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "time": timestamp,
        "role": role,
        "route": route,
        "masked_payload": masked_payload,
    }

    with open(MASKED_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
