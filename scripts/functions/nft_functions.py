"""
This file contains a class that has all the functionality to compile, deploy and use 
all the functionality of the FoxbrainsNFT smart contract. 
"""
import os
from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()


class NFT_Maker:
    """
    This is the the class that provides all the functionality to interact with the
    FoxbrainsNFT contract and the FoxbrainsERC20 contract.
    Methods provided:
        1) compile
        2) deploy
        3) set_base_URI
        4) create_INFT
        5) burn_INFT
        6) get_token_count
        7) get_token_URI
        8) whitelist_user
        9) get_whitelist_status
        10) create_fox20
        11) get_fox20_address
        12) get_fox20_balance
    """

    GANACHE_URL = "http://127.0.0.1:8545"
    GANACHE_CHAIN_ID = 1337

    def __init__(self):
        self.contract_address_ganache = None
        self.contract_address_goerli = None
        self.contract_abi = None
        self.contract_bytecode = None
        self.w3 = None
        self.contract = None

    def compile_contract(self):
        """This method compiles the NFT contract and saves the results in the
        build folder"""
        with open("./contracts/Foxbrains_NFT.sol", "r") as file:
            nft_file = file.read()

        print("Compiling solidity source code...")
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Foxbrains_NFT.sol": {"content": nft_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.8.7",
            allow_paths=[
                "/home/rohan/node_modules/@openzeppelin/contracts/token/ERC721/",
                "/home/rohan/node_modules/@openzeppelin/contracts/token/ERC20/",
                "/home/rohan/node_modules/@openzeppelin/contracts/utils",
            ],
        )

        # Making the build directory where we will dump the compiled sol
        try:
            os.mkdir("./build")
        except:
            print("'build' Directory already exists")

        print("Saving compiled contract...")
        with open("./build/compiled_code.json", "w") as file:
            json.dump(compiled_sol, file)

        # get bytecode/abi
        self.contract_bytecode = compiled_sol["contracts"]["Foxbrains_NFT.sol"][
            "FoxbrainsNFT"
        ]["evm"]["bytecode"]["object"]
        self.contract_abi = compiled_sol["contracts"]["Foxbrains_NFT.sol"][
            "FoxbrainsNFT"
        ]["abi"]
        print("Set the ABI and Bytecode for the contract!")

    def deploy_ganache(self):
        """This function deploys our smart contract to a Ganache CLI instance
        Note: Run ganache CLI in deterministic mode"""

        # connect to ganache
        self.w3 = Web3(Web3.HTTPProvider(self.GANACHE_URL))

        # create contract
        self.contract = self.w3.eth.contract(
            abi=self.contract_abi, bytecode=self.contract_bytecode
        )

        admin_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
        pvt_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
        nonce = self.w3.eth.get_transaction_count(admin_address)

        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction

        print("Deploying FoxbrainsNFT contract")
        transaction = self.contract.constructor().buildTransaction(
            {"chainId": self.GANACHE_CHAIN_ID, "from": admin_address, "nonce": nonce}
        )
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, private_key=pvt_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # Wait for transaction to finish
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract = self.w3.eth.contract(
            abi=self.contract_abi, address=tx_receipt.contractAddress
        )

        self.contract_address_ganache = tx_receipt.contractAddress
        self.contract_address_goerli = None
        print("[SUCCESS] Deployed contract to Ganache CLI...")

    def set_base_URI(self, uri_string):
        "Sets the default URI string for the NFTs as 'uri_string'"
        if self.contract_address_ganache == None:
            contract_address = self.contract_address_goerli
        else:
            contract_address = self.contract_address_ganache
            admin_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
            pvt_key = (
                "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
            )

        nonce = self.w3.eth.get_transaction_count(admin_address)
        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction

        print("Sending setBaseURI transaction...")
        tx = self.contract.functions.setBaseURI(uri_string).buildTransaction(
            {"chainId": self.GANACHE_CHAIN_ID, "from": admin_address, "nonce": nonce}
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # Wait for transaction to finish
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def create_INFT(self, token_uri):
        "This method creates a token for a given user"
        contract_address = self.contract_address_ganache
        user_address = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        pvt_key = "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"

        nonce = self.w3.eth.get_transaction_count(user_address)
        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction

        print(f"Minting FoxbrainsNFT for 0x{user_address[:4]}...")
        tx = self.contract.functions.createINFT(token_uri).buildTransaction(
            {"chainId": self.GANACHE_CHAIN_ID, "from": user_address, "nonce": nonce}
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # Wait for transaction to finish
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        print(self.contract.functions.balanceOf(user_address).call())
        print(self.contract.functions.ownerOf(0).call())
        print(self.contract.functions.tokenURI(0).call())
