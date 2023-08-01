from hashlib import sha256
from typing import List


class MerkleTree:
    def __init__(self, leafs: List[bytes]):
        self.tree = [leafs.copy()]
        self._create_merkle_tree(leafs)
        self.root = self.tree[-1][0] if len(self.tree[-1]) == 1 else []

    def __str__(self) -> str:
        output = ""
        for branch in self.tree[::-1]:
            output += str([item.hex()[:8] for item in branch]) + "\n"
        return output

    def _create_merkle_tree(self, branch: List[bytes]):
        if len(branch) <= 1:
            return

        if len(branch) % 2 == 1:
            branch.append(branch[-1])

        branch = [MerkleTree.hash_pair(branch[2 * i], branch[2 * i + 1]) for i in range(len(branch) // 2)]
        self.tree.append(branch)
        self._create_merkle_tree(branch)

    def get_proof(self, leaf_position: int) -> List[bytes]:
        if leaf_position > len(self.tree[0]) - 1:
            raise IndexError(f"Merkle leaf position out of range")

        proof = []
        item_position = leaf_position
        for branch in self.tree[:-1]:
            complementary_hash = branch[item_position + 1] if item_position % 2 == 0 else branch[item_position - 1]
            proof.append(complementary_hash)
            item_position = item_position // 2

        return proof

    @staticmethod
    def hash_pair(a, b):
        if a < b:
            return sha256(a + b).digest()
        return sha256(b + a).digest()

    @staticmethod
    def verify(proof: List[bytes], root: bytes, item: bytes) -> bool:
        if len(proof) == 0:
            return root == item

        new_root = MerkleTree.hash_pair(proof[0], item)
        for item in proof[1:]:
            new_root = MerkleTree.hash_pair(new_root, item)

        return root == new_root
