# Foxbrains-NFT-Task
Repository for the NFT Task from Foxbrains 2nd Round Interview
![Task](./images/Foxbrains%20-%20Interview%20Task.PNG)

The steps to install requirements are in the Ubuntu20.04-Blockchain-Setup.docx word file.

*Step 1:*
To start the system first open ganache CLI in deterministic mode using the following command in terminal:
`$ ganache -d`

*Step 2:*
Open **scripts/functions/** directory and open the **nft_functions.py** file.
Scroll down to the **compile_contracts** method and change the `allowed_paths=` paths to your own path in your machine. Save and close the python script.

*Step 3:*
Open another terminal in the main directory of the project. And enter the following command: `python3 scritps/main.py` This will run the main program for the project. 

*Step 4:*
Start by compiling the solidity file for the NFT (selecting option 1 in main.py interface). Then deploy the same onto ganache CLI. NOTE: make sure the ganache URL is **127.0.0.1:8545** with a chain code **1337**. After the system is deployed to ganache we can start testing the system.

*Step 5:*
NOTE: we will be using the first 3 addresses in ganache where address at index 0 is admin, 1 is minter and 2 is non whitelisted user.
We can change the base URI of the NFT using option 3.
We can mint a new NFT for user 1 using option 4. Similarly burn an NFT using option 5. After we mint 5 NFTs for user 1 the program will not mint anymore until we run option 8, where we whitelist user 1. we can check the whitelist status of users 1 and 2 using option 9.

*Step 6:* currently the testing scripts are missing due to the time constraint of making this project but the above steps clearly demonstrates that the smart contract fulfills the requirements. I will add Goerli testnet functionality on this later but for now the Smart contract is deployed on address: **0x704E9eB681D91d31F57BcA8A9370d52Bd6c0189e**