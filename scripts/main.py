from functions.nft_functions import NFT_Maker
import os

NFT = NFT_Maker()

NFT.compile_contract()
NFT.deploy_ganache()
NFT.set_base_URI("OMG")
for _ in range(6):
    NFT.create_INFT("ThisIsMyToken")
