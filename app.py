import streamlit as st
import requests

API_URL = "http://localhost:8000"  

USERS = {
    "alice": "admin",
    "bob": "viewer"
}

def login():
    st.sidebar.header("Login")
    username = st.sidebar.selectbox("Username", list(USERS.keys()))
    role = USERS[username]
    st.sidebar.markdown(f"**Role:** {role}")
    return username, role


def add_item():
    st.header("Add New Inventory Item")

    name = st.text_input("Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    category = st.text_input("Category")
    status = st.selectbox("Status", ["in_stock", "low_stock", "ordered", "discontinued"])
    description = st.text_area("Description (optional)")

    if st.button("Add Item"):
        data = {
            "name": name,
            "quantity": quantity,
            "category": category,
            "status": status,
            "description": description if description else None,
        }

        response = requests.post(f"{API_URL}/items/", json=data)
        if response.status_code == 200:
            st.success("Item added successfully!")
            st.json(response.json())
        else:
            st.error(f"Failed to add item: {response.text}")

def list_items():
    st.header("Inventory Items")

    # Filters
    name_filter = st.text_input("Filter by name")
    category_filter = st.text_input("Filter by category")
    status_filter = st.selectbox("Filter by status", ["", "in_stock", "low_stock", "ordered", "discontinued"])

    params = {}
    if name_filter:
        params["name"] = name_filter
    if category_filter:
        params["category"] = category_filter
    if status_filter:
        params["status"] = status_filter

    response = requests.get(f"{API_URL}/items/search", params=params)
    if response.status_code == 200:
        items = response.json()
        if items:
            for item in items:
                st.markdown(f"### {item['name']}")
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Quantity:** {item['quantity']}")
                st.write(f"**Status:** {item['status']}")
                st.write(f"**Description:** {item.get('description', 'N/A')}")
                st.markdown("---")
        else:
            st.info("No items found.")
    else:
        st.error(f"Error fetching items: {response.text}")

def main():
    st.title("Inventory Management System")

    menu = st.sidebar.selectbox("Menu", ["Add Item", "View Inventory"])
    if menu == "Add Item":
        add_item()
    elif menu == "View Inventory":
        list_items()

if __name__ == "__main__":
    main()
