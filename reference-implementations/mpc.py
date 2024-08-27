from hashlib import sha256
from dataclasses import dataclass
from typing import Self, Sequence
from math import log2
from functools import cached_property

NODE_TAG = b"urn:ubideco:merkle:node#2024-01-31"
MPC_TAG = b"urn:ubideco:mpc:commitment#2024-01-31"

def tagged_hash(tag, *elems: bytes):
    th = sha256(tag).digest()
    return sha256(th + th + b"".join(elems)).digest()


@dataclass
class Leaf:
    def hash(self) -> bytes:
        return NotImplemented


@dataclass
class PopulatedLeaf(Leaf):
    protocol: bytes
    message: bytes
    ident = b"\x10"

    def hash(self) -> bytes:
        return tagged_hash(NODE_TAG, self.ident, self.protocol, self.message)


@dataclass
class EntropyLeaf(Leaf):
    entropy: int
    pos: int
    ident = b"\x11"

    @property
    def entropy_bytes(self) -> bytes:
        return self.entropy.to_bytes(8, "little")

    @property
    def pos_bytes(self) -> bytes:
        assert self.pos is not None, "Leaf does not belong to a tree"
        return self.pos.to_bytes(4, "little")

    def hash(self) -> bytes:
        return tagged_hash(NODE_TAG, self.ident, self.entropy_bytes, self.pos_bytes)


@dataclass
class MerkleNode:
    left: Leaf | Self
    right: Leaf | Self
    depth: int
    tree_width: int

    @classmethod
    def from_cross_section(cls, leaves: Sequence[Leaf]) -> "MerkleNode":
        tree_width = len(leaves)
        tree_depth = int(log2(tree_width))
        assert 2**tree_depth == tree_width, f"tree must have 2^h leaves, {tree_depth}"
        return cls._from_cross_section(leaves, 0, tree_width)

    @classmethod
    def _from_cross_section(
        cls, leaves: Sequence[Leaf], depth: int, tree_width: int
    ) -> "MerkleNode":
        subtree_width = len(leaves)
        if subtree_width == 2:
            left, right = leaves
        else:
            # recursively build the two subtrees before creating the current node
            half = subtree_width // 2
            left = MerkleNode._from_cross_section(leaves[:half], depth + 1, tree_width)
            right = MerkleNode._from_cross_section(leaves[half:], depth + 1, tree_width)
        return MerkleNode(left, right, depth, tree_width)

    @property
    def branching(self) -> bytes:
        if self.left is None and self.right is None:
            return b"\x00"
        if self.left is None or self.right is None:
            return b"\x01"
        return b"\x02"

    @property
    def depth_bytes(self) -> bytes:
        assert self.depth is not None, "Node does not belong to a tree"
        return self.depth.to_bytes(1)

    @property
    def tree_width_bytes(self) -> bytes:
        assert self.tree_width is not None, "Node does not belong to a tree"
        return self.tree_width.to_bytes(32, "little")

    def hash(self) -> bytes:
        return tagged_hash(
            NODE_TAG,
            self.branching,
            self.depth_bytes,
            self.tree_width_bytes,
            self.left.hash(),
            self.right.hash(),
        )


@dataclass
class MerkleTree:
    depth: int
    cofactor: int
    entropy: int
    message_map: dict[int, tuple[bytes, bytes]]

    @cached_property
    def cross_section(self) -> list[Leaf]:
        return [
            (
                PopulatedLeaf(*self.message_map[pos])
                if pos in self.message_map
                else EntropyLeaf(self.entropy, pos)
            )
            for pos in range(2**self.depth)
        ]

    @cached_property
    def root(self) -> MerkleNode:
        return MerkleNode.from_cross_section(self.cross_section)

    @property
    def depth_bytes(self):
        return self.depth.to_bytes(1)

    @property
    def cofactor_bytes(self):
        return self.cofactor.to_bytes(2, "little")

    def hash(self):
        return tagged_hash(
            MPC_TAG, self.depth_bytes, self.cofactor_bytes, self.root.hash()
        )
