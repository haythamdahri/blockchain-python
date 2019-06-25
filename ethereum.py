import json
from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract
import time

# web3.py instance
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print(f"{web3.eth.accounts}")

balance = web3.fromWei(web3.eth.getBalance(
    "0xef238754E52e106b43116503284f219205549035"), 'ether')
print(f"0xef238754E52e106b43116503284f219205549035 Balance => {balance}")

votingAbiDefinition = '''[
	{
		"constant": true,
		"inputs": [
			{
				"name": "candidate",
				"type": "bytes32"
			}
		],
		"name": "totalVotesFor",
		"outputs": [
			{
				"name": "",
				"type": "uint8"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "candidate",
				"type": "bytes32"
			}
		],
		"name": "validCandidate",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "voterAddress",
				"type": "bytes32"
			}
		],
		"name": "markVoter",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "candidate",
				"type": "bytes32"
			}
		],
		"name": "voteForCandidate",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "winner",
		"outputs": [
			{
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "voterAddress",
				"type": "bytes32"
			}
		],
		"name": "checkVoteStatus",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getCandidateList",
		"outputs": [
			{
				"name": "",
				"type": "bytes32[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"name": "candidateNames",
				"type": "bytes32[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]
'''

address = web3.toChecksumAddress('0xf9b090ef5b56a4f387f069ae6bb5dadd0cc34b8a')
contract = web3.eth.contract(
    address=address, abi=votingAbiDefinition)

# Convert string to bytes32 to be passed as an argument
rama_name = bytes('Rama', 'utf-8')
rama_votes = contract.functions.totalVotesFor(rama_name).call()
print(f"Total votes for {rama_name.decode('utf8')} => {rama_votes} votes")

# Vote for rama
tx_hash = contract.functions.voteForCandidate(rama_name).transact({'from': web3.eth.accounts[1]})
tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
print("Vote has been done successflly")

# Retrieve new votes counter for rama
rama_votes = contract.functions.totalVotesFor(rama_name).call()
print(f"New Total votes for {rama_name.decode('utf8')} => {rama_votes} votes")
