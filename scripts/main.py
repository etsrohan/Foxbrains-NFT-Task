from functions.nft_functions import NFT_Maker
import os

NFT = NFT_Maker()


def main():
    print(
        """\n\nPlease enter your choice from one of the following below:
        Please make sure you have ganache CLI started in deterministic mode!!!
        ($ ganache -d)
        1) Compile Smart Contract
        2) Deploy Smart Contract
        3) Set base URI for Smart Contract
        4) Mint an FoxbrainsInterviewNFT
        5) Burn an existing INFT
        6) Get total number of tokens in circulation
        7) Get the URI for a given token
        8) [ADMIN] Bless a user by whitelisting them
        9) Get the whitelist statius of a user
        10) Create foxbrains ERC20 token for user
        11) Get the address where FoxbrainsERC20 token is deployed
        12) Get user balance for FOX20 token
        13) Find owner of a token\n\n"""
    )
    choice = int(input("Please enter your choice [1-13] or -1 to exit: "))
    print("\n")

    if choice == 1:
        NFT.compile_contract()
        main()

    elif choice == 2:
        NFT.deploy_ganache()
        print(f"Deploy Successful! Current token count: {NFT.get_token_count()}")
        main()

    elif choice == 3:
        NFT.set_base_URI(input("Please enter the new Base URI: "))
        main()

    elif choice == 4:
        token_uri = input("Please enter a URI you would want to attach to your NFT: ")
        NFT.create_INFT(token_uri)
        user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        print(f"Success! New NFT created...\nCurrent Balance: {NFT.get_balance(user)}")
        main()

    elif choice == 5:
        token_id = int(input("Please enter a token id: "))
        if NFT.burn_INFT(token_id):
            print(f"Success! Burned NFT with tokenID: {token_id}")
        else:
            print(f"Failure! Could not burn NFT with tokenID: {token_id}")
        main()

    elif choice == 6:
        print(f"Total number of tokens in circulation: {NFT.get_token_count()}")
        main()

    elif choice == 7:
        token_id = int(input("Please enter a token id: "))
        print(f"URI of Token with tokenID: {token_id}\n{NFT.get_token_URI(token_id)}")
        main()

    elif choice == 8:
        user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        NFT.whitelist_user(user)
        main()

    elif choice == 9:
        user = int(
            input("Please select whitelisted user (1) or non-whitelisted user(2): ")
        )
        if user == 1:
            user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        else:
            user = "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
        if NFT.get_whitelist_status(user):
            print(f"User: {user[:6]} is whitelisted!")
        else:
            print(f"User: {user[:6]} is not whitelisted!")
        main()

    elif choice == 10:
        user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        NFT.create_fox20()
        print(f"Success! New balance: {NFT.get_fox20_balance(user)}")
        main()

    elif choice == 11:
        print(f"Address of FoxbrainsERC20 Contract:\n{NFT.get_fox20_address()}")
        main()

    elif choice == 12:
        user = int(input("Please select user(1) or user(2): [1 or 2] "))
        if user == 1:
            user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"
        else:
            user = "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b"
        print(f"User: {user[:6]}, FOX20 Balance: {NFT.get_fox20_balance(user)}")
        main()

    elif choice == 13:
        token_id = int(input("Please enter a tokenID: "))
        print(
            f"Owner of Token with tokenID: {token_id}\nOwner: {NFT.get_owner(token_id)}"
        )
        main()

    elif choice == -1:
        print("Closing Main Program...")
        exit()
    else:
        main()


if __name__ == "__main__":
    main()
