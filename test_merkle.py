from hashlib import sha256
from random import random
from typing import List
from unittest import TestCase

from merkle_tree import MerkleTree


def create_random_input(n: int) -> List[bytes]:
    return [sha256(f"{random()}".encode("utf-8")).digest() for _ in range(n)]


class TestMerkle(TestCase):
    def test_valid_merkle_proof(self):
        merkle_leafs = create_random_input(10)
        merkle = MerkleTree(merkle_leafs)
        merkle_proof = merkle.get_proof(5)
        self.assertTrue(MerkleTree.verify(merkle_proof, merkle.root, merkle_leafs[5]))

    def test_invalid_merkle_proof(self):
        merkle_leafs = create_random_input(11)
        merkle = MerkleTree(merkle_leafs)
        merkle_proof = merkle.get_proof(7)
        self.assertFalse(MerkleTree.verify(merkle_proof, merkle.root, merkle_leafs[5]))

    def test_empty_list(self):
        merkle = MerkleTree([])
        self.assertListEqual(merkle.root, [])

    def test_merkle_get_merkle_proof_out_of_range(self):
        merkle = MerkleTree(create_random_input(10))
        with self.assertRaises(IndexError) as error:
            merkle.get_proof(20)
        self.assertEqual(str(error.exception), "Merkle leaf position out of range")

    def test_one_element_list(self):
        merkle_leafs = create_random_input(1)
        merkle = MerkleTree(merkle_leafs)
        merkle_proof = merkle.get_proof(0)

        self.assertTrue(MerkleTree.verify(merkle_proof, merkle.root, merkle_leafs[0]))
        self.assertListEqual(merkle_proof, [])
        self.assertEqual(merkle.root, merkle_leafs[0])
