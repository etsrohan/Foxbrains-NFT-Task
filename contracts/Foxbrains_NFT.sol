// SPDX-License-Identifier: MIT

// Developer: Rohan Srivastava
// Requirements:
//      1) Mint NFT with ERC721 and can mint max 5000 NFTs
//      2) Create a whitelist user for NFT
//          - Only smart contract creators can add whitelisted users
//          - Whitelist users can mint up to 10 NFT and other users can mint 5 NFTs
//      3) Function to burn NFTs
//      4) Create an ERC20 token named foxbrains

pragma solidity ^0.8.4;

import "/home/rohan/node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "/home/rohan/node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

// This is the smart contract that step 4 is talking about.
// This will be deployed from the FoxbrainsNFT contract.
// Since the email said "Create 'AN' ERC20 token..." I took this to mean that we are
// minting only one ERC20 token at a time.
// We will be able to interact with this contract using the getFOX20Address function
// or the external functions present in FoxbrainsNFT contract
contract FoxbrainsERC20 is ERC20 {
    // VARIABLES
    address private admin;

    // FUNCTIONS
    constructor() ERC20("foxbrains", "FOX20"){
        admin = msg.sender;
    }
    

    // Arguments: owner - address for whom we are minting the token
    // Returns: None
    // Note: to be used by NFT contract
    function mintFOX20(
        address owner
    )
        external
    {
        _mint(owner, 1);
    }

    // Arguments: owner - address for whom we are minting the token
    // Returns: number of tokens owned by 'owner'
    // Note: to be used by NFT contract
    function getBalance(
        address owner
    )
        external
        view
        returns (uint256)
    {
        return balanceOf(owner);
    }
}

// This is the main NFT contract corresponding to requirements
// 1-3 in the requirements above
contract FoxbrainsNFT is ERC721 {
    using Strings for uint256; // to convert tokenID into a string

    // VARIABLES
    address private admin;
    FoxbrainsERC20 private fox20;
    uint256 private maxMint = 5000;
    uint256 private tokenCount;
    uint256 private tokenIDCounter;
    string private baseURIUnique;

    mapping (uint256 => string) private _tokenURIs;
    mapping (address => bool) private _whiteList;

    // MODIFIERS
    modifier adminOnly() {
        require(msg.sender == admin, "Only the admin can access this functionality.");
        _;
    }

    // EVENTS

    // FUNCTIONS
    constructor() ERC721("FoxbrainsInterviewNFT", "INFT") {
        admin = msg.sender;
        baseURIUnique = "FoxbrainsInterview";

        // Deploy ERC20 token contract "foxbrains"
        FoxbrainsERC20 erc20Token = new FoxbrainsERC20();
        fox20 = erc20Token;
    }

    // Arguments: baseURI - The base string that will be attached to every tokenURI call
    // Returns: None
    // Note: This is just the base information about the contract set to "FoxbrainsInterview"
    // in the constructor, can only be set byt the admin.
    function setBaseURI(
        string memory baseURI
    )
        public
        adminOnly()
    {
        baseURIUnique = baseURI;
    }


    // Arguments: None
    // Returns: Number of tokens currently in circulation
    // Note: None
    function getTokenCount(
        /*NO ARGUMENTS*/
    )
        public 
        view 
        returns (uint256) 
    {
        return tokenCount;
    }

    // Arguments: tokenID - The unique ID of a minted NFT, tokenURI_ - token information
    // regarding the token, can be empty ("")
    // Returns: None
    // Note: requires tokenID to exist
    function _setTokenURI(
        uint256 tokenID,
        string memory tokenURI_
    )
        internal
        virtual
    {
        require(_exists(tokenID), "ERC721Metadata: URI set of nonexistent token");

        _tokenURIs[tokenID] = tokenURI_;
    }

    // Arguments: None
    // Returns: base URI string for the contract
    // Note: None
    function _baseURI(
        /*NO ARGUMENTS*/
    )
        internal
        view
        virtual
        override
        returns (string memory)
    {
        return baseURIUnique;
    }

    // Arguments: tokenID - The unique ID of a minted NFT
    // Returns: string URI for a given token, if tokenURI_ is an empty string (from mapping) then
    // returns the base string + tokenID 
    // Note: tokenID must exist
    function tokenURI(
        uint256 tokenID
    )
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(_exists(tokenID), "ERC721Metadata: URI set of nonexistent token");
        
        string memory tokenURI_ = _tokenURIs[tokenID];
        string memory base = _baseURI();
        
        return bytes(tokenURI_).length > 0 ? string(abi.encodePacked(base, tokenURI_)) : string(abi.encodePacked(base, tokenID.toString()));
    }

    // Arguments: blessed - The particular address our contract admin has blessed to be whitelisted
    // Returns: None
    // Note: None
    function whiteListUser(
        address blessed
    )
        public
        adminOnly()
    {
        _whiteList[blessed] = true;
    }
    
    // Arguments: None
    // Returns: The whitelist status of a particular user
    // Note: None
    function whiteListStatus()
        public
        view
        returns (bool)
    {
        return _whiteList[msg.sender];
    }


    // Arguments: tokenURI_ - The string information you want to attach to a newly minted NFT
    // Returns: None
    // Note: tokenCount needs to be less than 5000, if user is whitelisted then he/she can mint 10 NFTs
    // otherwise he/she can only mint 5
    function createINFT(
        string memory tokenURI_
    )
        public
    {
        // Requirements
        require(tokenCount <= maxMint, "Max limit on minting tokens reached!");
        if (_whiteList[msg.sender]) require(balanceOf(msg.sender) < 10, "Premium User: Mint limit reached, 10 Mints");
        else require(balanceOf(msg.sender) < 5, "Basic User: Mint limit reached, 5 Mints");

        // Update the tokenCount and tokenIDCounter
        uint256 itemID = tokenIDCounter++;
        tokenCount++;

        // Mint the NFT
        _safeMint(msg.sender, itemID);
        _setTokenURI(itemID, tokenURI_);
    }

    // Arguments: tokenID - The unique ID of a minted NFT
    // Returns: None
    // Note: tokenID must exist, only owner of token or admin can burn tokens
    function burnINFT(
        uint256 tokenID
    )
        public
    {
        require(_exists(tokenID), "ERC721Metadata: URI set of nonexistent token");
        // Only admin or token owner can burn the token
        require(
            msg.sender == admin || msg.sender == ownerOf(tokenID),
            "Unauthorized to burn this token!"
        );

        // Burn Token
        _burn(tokenID);

        // Reduce token count
        tokenCount--;
    }

    // Arguments: None
    // Returns: None
    // Note: sends a transaction to the FoxbrainsERC20 token deployed by this contract to create 1 token
    function createFOX20()
        public
    {
        FoxbrainsERC20(address(fox20)).mintFOX20(msg.sender);
    }

    // Arguments: None
    // Returns: the address of the deployed FoxbrainsERC20 token
    // Note: we need this to get the address and use the FoxbrainsERC20 functions
    function getFOX20Address()
        public
        view
        returns (address)
    {
        return address(fox20);
    }

    // Arguments: None
    // Returns: balance of FoxbrainsERC20 token for the msg.sender
    // Note: Just checks how many tokens a user has minted
    function getFOX20Balance()
        public
        view
        returns (uint256)
    {
        return FoxbrainsERC20(address(fox20)).getBalance(msg.sender);
    }
}
