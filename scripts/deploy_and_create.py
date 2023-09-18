from metadata.sample_metadata import metadata_template
from pathlib import Path
import json
import os
import requests


def main():
    #print_metadata()
    create_metadata("Gee", 40, "singer")
    print_metadata("Gee")
    collectible_name = "Gee"
    metadata_filepath = f"./metadata/{collectible_name}.json"
    upload_to_Pinata(metadata_filepath)

def create_metadata(collectible_name, age, position, image = "", description = ""):
    metadata = metadata_template
    metadata_filepath = f"./metadata/{collectible_name}.json"
    metadata["name"] = collectible_name
    metadata["description"] = description
    metadata["image"] = image
    metadata["attributes"][0]["value"] = age
    metadata["attributes"][1]["value"] = position
    with open(metadata_filepath, "w") as file:
        json.dump(metadata, file)


def print_metadata(collectible_name):
    metadata_filepath = f"./metadata/{collectible_name}.json"
    with Path(metadata_filepath).open("rb") as fp:
        metadata = fp.read()
        print(metadata)

def upload_to_Pinata(filepath):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET_KEY"),
    }
    with Path(filepath).open("rb") as fp:
        data = fp.read()
        response = requests.post(url = url,files = {"file" : ("Gee.json", data)}, headers = headers)
        print(response.text)

#https://ipfs.io/ipfs/Qmd1vSMNgdHoqpWPYDwDeghdnyMr4CJ6R2QuLfYa9zFeHS?filename=Gee.json