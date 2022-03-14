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
    NOTE: This class only works with deterministic mode of Ganache CLI
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
    GOERLI_URL = "https://goerli.infura.io/v3/d3db5ee9981b4500be7eff014c43ecdb"
    GOERLI_CHAIN_ID = 5

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
        # #################################################################
        # CHANGE THE PATH ABOVE TO LINK TO THE CORRESPONDING DIRECTORIES!!!
        # #################################################################

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

        print("Saving contract address...")
        # Making the build directory where we will dump the compiled sol
        try:
            os.mkdir("./build")
        except:
            print("'build' Directory already exists")
        with open("./build/contract_address_ganache.info", "w") as file:
            file.write(self.contract_address_ganache)

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
        if self.contract_address_ganache == None:
            pass
        else:
            # 2nd address of the Ganache CLI in deterministic mode
            contract_address = self.contract_address_ganache
            user_address = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
            pvt_key = (
                "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
            )

        nonce = self.w3.eth.get_transaction_count(user_address)
        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction

        print(f"Minting FoxbrainsNFT for {user_address[:6]}...")
        try:
            tx = self.contract.functions.createINFT(token_uri).buildTransaction(
                {"chainId": self.GANACHE_CHAIN_ID, "from": user_address, "nonce": nonce}
            )
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Wait for transaction to finish
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except:
            print("[ERROR] Exceeded maximum allowed limit!")

    def burn_INFT(self, token_id):
        """
        This method burns a particular NFT.
        Arguments: token_id - unique identifier for NFT
        Note: only the owner and the admin can burn NFTs
        """
        choice = int(input("Are you the Admin (1), Owner (2) or None (3)? [1-3] "))

        if choice == 1:
            sender_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
            pvt_key = (
                "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
            )

        elif choice == 2:
            sender_address = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
            pvt_key = (
                "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
            )

        else:
            sender_address = "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
            pvt_key = (
                "0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c"
            )

        nonce = self.w3.eth.get_transaction_count(sender_address)

        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction
        try:
            print(f"Burning FoxbrainsNFT for tokenID: {token_id}...")
            tx = self.contract.functions.burnINFT(token_id).buildTransaction(
                {
                    "chainId": self.GANACHE_CHAIN_ID,
                    "from": sender_address,
                    "nonce": nonce,
                }
            )
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Wait for transaction to finish
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return True
        except:
            print("UNAUTHORIZED USER - Cannot burn Token!")
            return False

    def get_token_count(self):
        "A simple method to call the getTokenCount ABI"
        return self.contract.functions.getTokenCount().call()

    def get_token_URI(self, token_id):
        """
        A simple method to call the URI of a particular token
        Note: token_id must exist"""
        try:
            ret = self.contract.functions.tokenURI(token_id).call()
        except:
            print("[ERROR] Token does not exist!")
            ret = None
        return ret

    def whitelist_user(self, blessed):
        """
        A method to be used by the admin to whitelist a user
        """
        sender_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
        pvt_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

        nonce = self.w3.eth.get_transaction_count(sender_address)

        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction
        print(f"Whitelisting user: {blessed[:6]}...")
        tx = self.contract.functions.whiteListUser(blessed).buildTransaction(
            {
                "chainId": self.GANACHE_CHAIN_ID,
                "from": sender_address,
                "nonce": nonce,
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # Wait for transaction to finish
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_whitelist_status(self, user):
        "A simple method that returns the whitelist status of a given user"
        return self.contract.functions.whiteListStatus().call({"from": user})

    def create_fox20(self):
        "A method to create a FOX20 ERC20 token"
        sender_address = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        pvt_key = "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"

        nonce = self.w3.eth.get_transaction_count(sender_address)

        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction
        print(f"Minting FOX20 Token for user: {sender_address[:6]}...")
        tx = self.contract.functions.createFOX20().buildTransaction(
            {
                "chainId": self.GANACHE_CHAIN_ID,
                "from": sender_address,
                "nonce": nonce,
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pvt_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # Wait for transaction to finish
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_fox20_address(self):
        "A method that returns the address of the deployed FoxbrainsERC20 contract"
        return self.contract.functions.getFOX20Address().call()

    def get_fox20_balance(self, user):
        "A method that returns the balance of foxbrains(FOX20) tokens for a given user"
        return self.contract.functions.getFOX20Balance().call({"from": user})

    def get_balance(self, user):
        "Get the number of INFTs a user has"
        return self.contract.functions.balanceOf(user).call()

    def get_owner(self, token_id):
        "Get the owner of a given token_id"
        return self.contract.functions.ownerOf(token_id).call()

    def deploy_goerli(self):
        """This function deploys our smart contract to a Goerli Testnet instance"""

        # connect to ganache
        self.w3 = Web3(Web3.HTTPProvider(self.GOERLI_URL))

        # create contract
        self.contract = self.w3.eth.contract(
            abi=self.contract_abi, bytecode=self.contract_bytecode
        )

        admin_address = os.getenv("ACCOUNT_ADDRESS")
        pvt_key = os.getenv("PRIVATE_KEY")
        nonce = self.w3.eth.get_transaction_count(admin_address)

        # We do the following steps:
        # 1. Build Transaction
        # 2. Sign Transaction
        # 3. Send Transaction

        print("Deploying FoxbrainsNFT contract to Goerli Testnet...")
        transaction = self.contract.constructor().buildTransaction(
            {"chainId": self.GOERLI_CHAIN_ID, "from": admin_address, "nonce": nonce}
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

        self.contract_address_ganache = None
        self.contract_address_goerli = tx_receipt.contractAddress
        print("[SUCCESS] Deployed contract to Goerli Testnet...")

        print("Saving contract address...")
        # Making the build directory where we will dump the compiled sol
        try:
            os.mkdir("./build")
        except:
            print("'build' Directory already exists")
        with open("./build/contract_address_goerli.info", "w") as file:
            file.write(self.contract_address_goerli)
        print(f"Contract deployed to: {self.contract_address_goerli}")
