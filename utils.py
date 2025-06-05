import os
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generate_product_description(name: str, category: str) -> str:
    system_message = {"role": "system", "content": "You are an assistant that generates concise, helpful product descriptions."}
    user_message = {
        "role": "user",
        "content": f"Generate a short product description for the following:\nName: {name}\nCategory: {category}"
    }

    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[system_message, user_message],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def extract_item_data_from_text(user_input: str) -> Dict:
    system_message = {
        "role": "system",
        "content": "You are an assistant that extracts inventory item data from user input and returns it in JSON."
    }

    function_def = {
        "name": "add_inventory_item",
        "description": "Extract item details from user message to add to inventory",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the item"},
                "quantity": {"type": "integer", "description": "Quantity of the item"},
                "category": {"type": "string", "description": "Item category"},
                "status": {
                    "type": "string",
                    "enum": ["in_stock", "low_stock", "ordered", "discontinued"],
                    "description": "Inventory status"
                }
            },
            "required": ["name", "quantity", "category", "status"]
        }
    }

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            system_message,
            {"role": "user", "content": user_input}
        ],
        functions=[function_def],
        function_call={"name": "add_inventory_item"},
        temperature=0.5
    )

    arguments = response.choices[0].message.function_call.arguments
    import json
    return json.loads(arguments)