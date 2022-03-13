// SPDX-License-Identifier: MIT

// Requirements:
//      1) Mint NFT with ERC721 and can mint max 5000 NFTs
//      2) Create a whitelist user for NFT
//          - Only smart contract creators can add whitelisted users
//          - Whitelist users can mint up to 10 NFT and other users can mint 5 NFTs
//      3) Function to burn NFTs
//      4) Create an ERC20 token named foxbrains

pragma solidity ^0.8.4;

import "/home/rohan/node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract FoxbrainsNFT is ERC721 {
    using Strings for uint256;

    // VARIABLES
    address private admin;
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
    constructor() ERC721("InterviewNFT", "INFT") {
        admin = msg.sender;
        tokenCount = 0;
        tokenIDCounter = 0;
        baseURIUnique = "FoxbrainsInterview";
    }

    function setBaseURI(
        string memory baseURI
    )
        public
        adminOnly()
    {
        baseURIUnique = baseURI;
    }


    // Arguments: NONE
    // Returns: Number of tokens currently in circulation
    // Note: none
    function getTokenCount(
        /*NO ARGUMENTS*/
    )
        public 
        view 
        returns (uint256) 
    {
        return tokenCount;
    }

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

    function whiteListUser(
        address blessed
    )
        public
        adminOnly()
    {
        _whiteList[blessed] = true;
    }
    

    function whiteListStatus()
        public
        view
        returns (bool)
    {
        return _whiteList[msg.sender];
    }


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
}
