import json

import requests
import streamlit as st


st.set_page_config(page_title="Role-Based Masking UI", layout="wide")
st.title("Role-Based Masking UI")

with st.sidebar:
    st.header("API Connection")
    base_url = st.text_input("Base URL", value="http://localhost:8000")
    st.caption("Set this to your running FastAPI server.")

    st.divider()
    st.header("View Mode")
    view_mode = st.radio(
        "Choose a route",
        ["User (all)", "User by ID", "Support", "Admin", "Create User"],
        index=0,
    )


def api_get(path: str):
    url = f"{base_url.rstrip('/')}{path}"
    return requests.get(url, timeout=15)


def api_post(path: str, payload: dict):
    url = f"{base_url.rstrip('/')}{path}"
    return requests.post(url, json=payload, timeout=15)


def show_response(resp: requests.Response):
    if resp.ok:
        try:
            data = resp.json()
            if isinstance(data, list) and data and isinstance(data[0], dict):
                st.dataframe(data, use_container_width=True, hide_index=True)
            elif isinstance(data, dict):
                st.dataframe([data], use_container_width=True, hide_index=True)
            else:
                st.write(data)
        except json.JSONDecodeError:
            st.text(resp.text)
    else:
        st.error(f"Request failed: {resp.status_code}")
        try:
            st.json(resp.json(), expanded=False)
        except json.JSONDecodeError:
            st.text(resp.text)


if view_mode == "User (all)":
    st.subheader("All Users (masked as user)")
    if st.button("Fetch /users"):
        show_response(api_get("/users"))

elif view_mode == "User by ID":
    st.subheader("User By ID (masked as user)")
    user_id = st.number_input("User ID", min_value=1, step=1, value=1)
    if st.button("Fetch /users/{id}"):
        show_response(api_get(f"/users/{int(user_id)}"))

elif view_mode == "Support":
    st.subheader("Support View (masked as support)")
    if st.button("Fetch /support"):
        show_response(api_get("/support"))

elif view_mode == "Admin":
    st.subheader("Admin View (full data)")
    if st.button("Fetch /admin"):
        show_response(api_get("/admin"))

elif view_mode == "Create User":
    st.subheader("Create User")
    with st.form("create_user_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="Full name")
            phone = st.text_input("Phone", placeholder="10-digit Indian number")
            email = st.text_input("Email", placeholder="name@example.com")
            pan = st.text_input("PAN", placeholder="ABCDE1234F")
        with col2:
            ifsc = st.text_input("IFSC", placeholder="HDFC0001234")
            upi = st.text_input("UPI (optional)", placeholder="name@bank")
            account = st.text_input("Account Number")
            balance = st.number_input("Balance", min_value=0.0, step=0.01, value=0.0)

        submitted = st.form_submit_button("Create (/upload_users)")
        if submitted:
            payload = {
                "name": name,
                "phone": phone,
                "email": email,
                "pan": pan,
                "ifsc": ifsc,
                "upi": upi or None,
                "account": account,
                "balance": float(balance),
            }
            show_response(api_post("/upload_users", payload))
