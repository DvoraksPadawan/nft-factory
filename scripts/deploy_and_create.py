from metadata.sample_metadata import metadata_template
from pathlib import Path
import json
import os
import requests
from brownie import NFTFactory
import scripts.helpful_scripts as helpful_scripts

OPENSEA_URL = "https://testnets.opensea.io/assets/sepolia/{}/{}"

def main():
    deploy()
    create_collectible("GerardWay", "40", "singer")
    create_collectible("FrankIero", "39", "guitarist")
    

def create_collectible(collectible_name, age, position, desription = "", account = None):
    account = account if account else helpful_scripts.get_account()
    image_hash = upload_to_Pinata(get_filepath(collectible_name, True))
    image_uri = get_ipfs_link(image_hash, collectible_name, True)
    create_metadata(collectible_name, age, position, image_uri)
    metadata_uri = upload_to_Pinata(get_filepath(collectible_name))
    NFTFactory[-1].createCollectible(metadata_uri, {"from" : account})
    collectible = NFTFactory[-1]
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(collectible.address, collectible.tokenCounter() - 1)}"
    )


def create_metadata(collectible_name, age, position, image, description = ""):
    metadata = metadata_template
    metadata_filepath = f"./metadata/{collectible_name}.json"
    metadata["name"] = collectible_name
    metadata["description"] = description
    metadata["image"] = image
    metadata["attributes"][0]["value"] = age
    metadata["attributes"][1]["value"] = position
    with open(metadata_filepath, "w") as file:
        json.dump(metadata, file)

def get_ipfs_link(hash, filename, image = False):
    if not image:
        return f"https://ipfs.io/ipfs/{hash}?filename={filename}.json"
    else:
        return f"https://ipfs.io/ipfs/{hash}?filename={filename}.jpg"

def deploy(account = None):
    account = account if account else helpful_scripts.get_account()
    publish_source = helpful_scripts.get_publish_source()
    nft_factory = NFTFactory.deploy("MCR bandmates", "MCR", {"from" : account}, publish_source=publish_source)

def print_metadata(collectible_name):
    metadata_filepath = f"./metadata/{collectible_name}.json"
    with Path(metadata_filepath).open("rb") as fp:
        metadata = fp.read()
        print(metadata)

def get_filepath(name, image = False):
    if not image:
        return f"./metadata/{name}.json"
    else:
        return f"./image/{name}.jpg"

def upload_to_Pinata(filepath):
    filename = filepath.split("/")[-1]
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET_KEY"),
    }
    with Path(filepath).open("rb") as fp:
        data = fp.read()
        response = requests.post(url = url,files = {"file" : (filename, data)}, headers = headers)
        ipfs_hash = response.json()["IpfsHash"]
        return ipfs_hash

#https://ipfs.io/ipfs/Qmd1vSMNgdHoqpWPYDwDeghdnyMr4CJ6R2QuLfYa9zFeHS?filename=Gee.json
#https://ipfs.io/ipfs/Qmd1vSMNgdHoqpWPYDwDeghdnyMr4CJ6R2QuLfYa9zFeHS?filename=Gee.json
#QmaiusU7enA3nLKh8mxsJBWseX5mCQ5r36w4oEebuQA9UZ
#ipfs://ipfs.io/ipfs://QmaiusU7enA3nLKh8mxsJBWseX5mCQ5r36w4oEebuQA9UZ?filename=FrankIero.json
#ipfs://QmaiusU7enA3nLKh8mxsJBWseX5mCQ5r36w4oEebuQA9UZ?filename=FrankIero.json
#Qmao8ZbzuhbwzuLyQ5xxG13r37nvFQj3NUNF2ySoZLkC8W
#https://ipfs.io/ipfs/Qmao8ZbzuhbwzuLyQ5xxG13r37nvFQj3NUNF2ySoZLkC8W?filename=FrankIero.jpg
