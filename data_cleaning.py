from pymongo import ASCENDING
from bson.regex import Regex

def remove_duplicates(mongo, collection_name, key_field):
    """
    Removes duplicate documents from a collection based on a key field.
    Keeps the first occurrence.
    """
    seen = set()
    duplicates = []

    collection = mongo.db[collection_name]
    for doc in collection.find({}, {key_field: 1}):
        value = doc.get(key_field)
        if value in seen:
            duplicates.append(doc["_id"])
        else:
            seen.add(value)

    if duplicates:
        collection.delete_many({"_id": {"$in": duplicates}})
        print(f"Removed {len(duplicates)} duplicate records from {collection_name}.")
    else:
        print("No duplicates found.")


def normalize_text_case(mongo, collection_name, field, case="lower"):
    """
    Normalizes text field to lowercase or uppercase.
    """
    collection = mongo.db[collection_name]
    for doc in collection.find({field: {"$exists": True}}):
        value = doc.get(field, "")
        if isinstance(value, str):
            new_value = value.lower() if case == "lower" else value.upper()
            collection.update_one({"_id": doc["_id"]}, {"$set": {field: new_value}})

    print(f"Normalized text case for {field} in {collection_name}.")


def handle_missing_data(mongo, collection_name, field, default_value):
    """
    Replaces missing or empty string values with a default.
    """
    collection = mongo.db[collection_name]
    result = collection.update_many(
        { "$or": [{field: {"$exists": False}}, {field: ""}] },
        { "$set": {field: default_value} }
    )
    print(f"Filled {result.modified_count} missing '{field}' fields with '{default_value}'.")


def create_index(mongo, collection_name, field):
    """
    Adds an index on a specific field to speed up queries.
    """
    mongo.db[collection_name].create_index([(field, ASCENDING)])
    print(f"Index created on {field} in {collection_name}.")


def run_all_cleaning(mongo):
    """
    Runs all cleaning and optimization routines.
    Update the field/collection names based on your schema.
    """
    collection = "users"

    remove_duplicates(mongo, collection_name=collection, key_field="email")
    normalize_text_case(mongo, collection_name=collection, field="name")
    handle_missing_data(mongo, collection_name=collection, field="status", default_value="Unknown")
    create_index(mongo, collection_name=collection, field="email")