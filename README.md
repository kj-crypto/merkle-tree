# Merkle Tree
Example of merkle tree implementation in python using single sha256 hashing.


## Usage
Example of merkle tree usage
```python
from merkle_tree import MerkleTree


merkle = MerkleTree([b"a", b"b", b"c"])
print("Merkle Tree", merkle, sep="\n")
print("Merkle Proof", [item.hex()[:8] for item in merkle.get_proof(1)])
```

with following output
```bash
Merkle Tree
['75761571']
['fb8e20fc', '355b1bbf']
['61', '62', '63']

Merkle Proof ['61', '355b1bbf']
```


## Tests
Run `python -m unittest test_merkle.py` to execute tests.
