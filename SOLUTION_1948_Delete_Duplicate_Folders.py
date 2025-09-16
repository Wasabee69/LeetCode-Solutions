from typing import List, Tuple, Dict, Callable
mod = (1<<30)-1
base = 41
powBase = [1] * (10**5+1)
# Leetcode Question 1948 solution
# Implementation using Rolling hash, Depth-first-search & Trie structure for subpaths
for i in range(1, 10**5+1):
    powBase[i] = powBase[i-1]*base % mod
class Solution:
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        asci = {chr(i+97):i for i in range(26)}
        DELIMETER_HASH = 29
        START_TUPLE_HASH = 31
        END_TUPLE_HASH = 37
        hash_cache = {}
        def get_hash(s: str) -> Tuple[int, int]:
            if s in hash_cache:
                return hash_cache[s]
            x = 0
            for ch in s:
                x = (x * base + asci[ch]) % mod
            hash_cache[s] = (x, len(s))
            return hash_cache[s]

        def seperate_nums_by_delimeter(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
            (hash1, length1), (hash2, length2) = t1, t2
            return (hash1*powBase[length2] + hash2 * base + DELIMETER_HASH) % mod, length1+length2

        def combine_child_parent_into_brackets(hashes_with_lengths: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
            x = 0
            length = 0
            for (h1, l1), (h2, l2) in hashes_with_lengths:

                length += 1 + l1 + 1 + l2 + 1

                x = (x * base + START_TUPLE_HASH) % mod
                
                x = (x * powBase[l1] + h1) % mod

                x = (x * base + DELIMETER_HASH) % mod

                x = (x * powBase[l2] + h2) % mod

                x = (x * base + END_TUPLE_HASH) % mod

                x = (x * base + DELIMETER_HASH) % mod

            return (x, length)


        trie = {}
        path_hashes = {}
        for path in paths:
            node = trie
            path_hash = (0, 0)
            for folder in path:
                folder = get_hash(folder)
                if folder not in node:
                    node[folder] = {}
                node = node[folder]
                path_hash = seperate_nums_by_delimeter(path_hash, folder)
            path_hashes[path_hash] = path

        def set_paths_to_None(trie: Dict[Tuple[int, int], Dict], counts: Dict[int, int], criteria_to_delete: Callable[[int], bool]) -> Dict[Tuple[int, int], Dict]:
            subtree_cache = {}
            def subtree_hashes(node: Tuple[int, int]) -> Tuple[int, int]:
                node_id = id(node)
                if not node:
                    subtree_cache[node_id] = 0
                    return (0, 0)

                subtree = [( folder, subtree_hashes(node[folder]) ) for folder in sorted(node)]

                combined_hash, length = combine_child_parent_into_brackets(subtree)

                counts[combined_hash] = counts.get(combined_hash, 0)+1
                subtree_cache[node_id] = combined_hash
                return (combined_hash, length)
            subtree_hashes(trie)

            def rec_delete(node: Tuple[int, int], par=None, par_key=None) -> None:
                node_id = id(node)
                for folder in list(node):
                    rec_delete(node[folder], node, folder)
                    
                if criteria_to_delete( counts[subtree_cache[node_id]] ):
                    del par[par_key]
            rec_delete(trie)
            return trie


        def get_remaining_paths(path_hashes: Dict[Tuple[int, int], str], trie: Dict[Tuple[int, int], Dict]) -> List:
            res = []
            def rec(node: Tuple[int, int], path_hash: int):
                if path_hash in path_hashes:
                    res.append(path_hashes[path_hash])

                for folder in node:
                    new_hash = seperate_nums_by_delimeter(path_hash, folder)
                    rec(node[folder], new_hash)

            rec(trie, (0, 0))
            return res

        reduced_trie = set_paths_to_None(trie, {0:0}, lambda x: x > 1)

        return get_remaining_paths(path_hashes, reduced_trie)
