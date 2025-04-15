from check_input import check_input
import random
import matplotlib.pyplot as plt



def get_sorted(to_sort):
    """
    Convert each element of 'to_sort' to its rank in [0..n-1].
    """
    to_return = []
    for i in range(len(to_sort)):
        rank = 0
        for j in to_sort:
            if j < to_sort[i]:
                rank += 1
        to_return.append(rank)
    return to_return

class stacks:
    def __init__(self, stack_a):
        check_input(stack_a)
        self.stack_a = get_sorted(stack_a)
        self.stack_b = []
        self.moves = []
        self.size_a = len(stack_a)

    def check_sorted(self):
        """
        True if self.stack_a == [0,1,2,...,n-1].
        """
        return all(i == j for i, j in enumerate(self.stack_a))


    def sa(self, silent=False):
        if len(self.stack_a) > 1:
            self.stack_a[0], self.stack_a[1] = self.stack_a[1], self.stack_a[0]
            if not silent:
                self.moves.append("sa")

    def sb(self, silent=False):
        if len(self.stack_b) > 1:
            self.stack_b[0], self.stack_b[1] = self.stack_b[1], self.stack_b[0]
            if not silent:
                self.moves.append("sb")

    def ss(self):
        self.sa(silent=True)
        self.sb(silent=True)
        self.moves.append("ss")

    def pa(self):
        if self.stack_b:
            self.stack_a.insert(0, self.stack_b.pop(0))
            self.moves.append("pa")

    def pb(self):
        if self.stack_a:
            self.stack_b.insert(0, self.stack_a.pop(0))
            self.moves.append("pb")

    def ra(self, silent=False):
        """
        rotate A: top item -> bottom
        """
        if len(self.stack_a) > 1:
            self.stack_a.append(self.stack_a.pop(0))
            if not silent:
                self.moves.append("ra")

    def rb(self, silent=False):
        """
        rotate B: top item -> bottom
        """
        if len(self.stack_b) > 1:
            self.stack_b.append(self.stack_b.pop(0))
            if not silent:
                self.moves.append("rb")

    def rr(self):
        """
        rotate both
        """
        self.ra(silent=True)
        self.rb(silent=True)
        self.moves.append("rr")

    def rra(self, silent=False):
        """
        reverse rotate A: bottom item -> top
        """
        if len(self.stack_a) > 1:
            self.stack_a.insert(0, self.stack_a.pop())
            if not silent:
                self.moves.append("rra")

    def rrb(self, silent=False):
        """
        reverse rotate B: bottom item -> top
        """
        if len(self.stack_b) > 1:
            self.stack_b.insert(0, self.stack_b.pop())
            if not silent:
                self.moves.append("rrb")

    def rrr(self):
        """
        reverse rotate both
        """
        self.rra(silent=True)
        self.rrb(silent=True)
        self.moves.append("rrr")



    def _lis_indices(self, arr):
        """
        Returns a set of indices which form one Longest Increasing Subsequence.
        We'll use a patience-sort or DP approach, then backtrack to find the LIS.
        This is standard LIS in O(n log n) or O(n^2). For simplicity, here's O(n^2).
        """
        n = len(arr)
        if n <= 1:
            return set(range(n))

        # dp[i] = length of LIS ending at i
        dp = [1]*n
        # parent[i] = index of prev element in the LIS that ends at i
        parent = [-1]*n
        max_len = 1
        max_idx = 0

        for i in range(n):
            for j in range(i):
                if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
            if dp[i] > max_len:
                max_len = dp[i]
                max_idx = i

        lis_idx = []
        cur = max_idx
        while cur != -1:
            lis_idx.append(cur)
            cur = parent[cur]
        lis_idx.reverse() 

        return set(lis_idx)

    def _best_insert_position_in_a(self, val):
        """
        For re-inserting 'val' from B into A in ascending order:
         - We find the correct spot in A so that A remains sorted by rank.
         - Return the index where 'val' should be inserted (0-based from top).
        """

        arr = self.stack_a
        if not arr:
            return 0  # A is empty => top is the only place

        if val < min(arr):
            return arr.index(min(arr))
        if val > max(arr):
            return arr.index(max(arr)) + 1

        for i in range(len(arr)):
            if arr[i] > val:
                return i
        return len(arr)  # fallback at bottom

    def _rotate_both_min_cost(self, idx_a, idx_b):
        """
        Perform minimal rotation to bring self.stack_a[idx_a] on top
        and self.stack_b[idx_b] on top, using combos of ra/rb or rra/rrb, etc.
        We'll do a typical "cost-based" approach:
          - if idx_a <= half(A) and idx_b <= half(B) => use rr
          - if idx_a > half(A) and idx_b > half(B) => use rrr
          - otherwise rotate A and B separately
        """
        size_a = len(self.stack_a)
        size_b = len(self.stack_b)

        dist_a = idx_a
        dist_b = idx_b
        rdist_a = size_a - idx_a
        rdist_b = size_b - idx_b

        if dist_a <= size_a//2 and dist_b <= size_b//2:
            while dist_a > 0 and dist_b > 0:
                self.rr()
                dist_a -= 1
                dist_b -= 1
            while dist_a > 0:
                self.ra()
                dist_a -= 1
            while dist_b > 0:
                self.rb()
                dist_b -= 1
        elif rdist_a <= size_a//2 and rdist_b <= size_b//2:
            while rdist_a > 0 and rdist_b > 0:
                self.rrr()
                rdist_a -= 1
                rdist_b -= 1
            while rdist_a > 0:
                self.rra()
                rdist_a -= 1
            while rdist_b > 0:
                self.rrb()
                rdist_b -= 1
        else:

            if dist_a <= size_a//2:
                while dist_a > 0:
                    self.ra()
                    dist_a -= 1
            else:
                while rdist_a > 0:
                    self.rra()
                    rdist_a -= 1
            if dist_b <= size_b//2:
                while dist_b > 0:
                    self.rb()
                    dist_b -= 1
            else:
                while rdist_b > 0:
                    self.rrb()
                    rdist_b -= 1


    def sort_large(self):

        n = len(self.stack_a)
        if n <= 1 or self.check_sorted():
            return
        arr = self.stack_a
        lis_set = self._lis_indices(arr)
        original_count = len(self.stack_a)
        for _ in range(original_count):
            if len(self.stack_a) == 0:
                break
            top_index = 0  # obviously
            if top_index in lis_set:
            
                self.ra()
                lis_set = { (x-1) % len(self.stack_a) for x in lis_set }
            else:
                self.pb()
   
                new_set = set()
                for x in lis_set:
                    if x > 0:
                        new_set.add(x-1)
                lis_set = new_set

      
        while len(self.stack_b) > 0:
            val_b_top = self.stack_b[0]
            insert_idx = self._best_insert_position_in_a(val_b_top)
           
            idx_b = 0
            idx_a = insert_idx
            self._rotate_both_min_cost(idx_a, idx_b)
            self.pa()

    def sort_2(self):
        if not self.check_sorted():
            self.sa()

    def sort_3(self):
        pass


#
# Demo
#
if __name__ == "__main__":
    results_100 = []
    # Typically run multiple times to see average move counts
    for i in range(10000):
        input_data = random.sample(range(1000), 500)  # distinct integers from 0..99
        s = stacks(input_data)
        s.sort_large()
        results_100.append(len(s.moves))
    
    plt.hist(results_100)
    import pandas as pd
    df = pd.DataFrame(results_100)
    print(df.describe())
    plt.show()


# class stacks:
#     def __init__(self, stack_a):
#         check_input(stack_a)
#         self.stack_a = get_sorted(stack_a)
#         self.stack_b = []
#         self.moves = []
#         self.size_a = len(stack_a)

#     def sort(self):
#         if len(self.stack_a) < 2:
#             return 0
#         elif len(self.stack_a) == 2:
#             print(self.stack_a)
#             self.sort_2()
#             print(self.stack_a)
#             return self.moves
        
#         elif len(self.stack_a) == 3:
#             print(self.stack_a)
#             self.sort_3()
#             print(self.stack_a)
#             return self.moves
#         else:
#             print(self.stack_a)
#             self.sort_large()
#             print(self.stack_a)
#             return self.moves

#     def check_sorted(self):
#         # Checks if self.stack_a is exactly [0, 1, 2, ..., n-1]
#         return all(i == j for i, j in enumerate(self.stack_a))

#     def sa(self, silent=False):
#         if len(self.stack_a) > 1:
#             self.stack_a[0], self.stack_a[1] = self.stack_a[1], self.stack_a[0]
#             if not silent:
#                 self.moves.append("sa")
    
#     def sb(self, silent=False):
#         if len(self.stack_b) > 1:
#             self.stack_b[0], self.stack_b[1] = self.stack_b[1], self.stack_b[0]
#             if not silent:
#                 self.moves.append("sb")

#     def ss(self):
#         self.sa(silent=True)
#         self.sb(silent=True)
#         self.moves.append("ss")

#     def pa(self):
#         if len(self.stack_b):
#             self.stack_a.insert(0, self.stack_b.pop(0))
#         self.moves.append("pa")

#     def pb(self):
#         if len(self.stack_a):
#             self.stack_b.insert(0, self.stack_a.pop(0))
#         self.moves.append("pb")def check_input(x):
    # Stub for your original input checks
    pass

#     def rra(self, silent=False):
#         if len(self.stack_a) > 1:
#             self.stack_a.insert(0, self.stack_a.pop())
#             if not silent:
#                 self.moves.append("ra")

#     def rb(self, silent=False):
#         if len(self.stack_b) > 1:
#             self.stack_b.insert(0, self.stack_b.pop())
#             if not silent:
#                 self.moves.append("rb")
    
#     def rr(self):
#         self.ra(silent=True)
#         self.rb(silent=True)
#         self.moves.append("rr")

#     def ra(self, silent=False):
#         if len(self.stack_a) > 1:
#             self.stack_a.append(self.stack_a.pop(0))
#             if not silent:
#                 self.moves.append("rra")

#     def rb(self, silent=False):
#         if len(self.stack_b) > 1:
#             self.stack_b.append(self.stack_b.pop(0))
#             if not silent:
#                 self.moves.append("rrb")

#     def rrr(self):
#         self.rra(silent=True)
#         self.rrb(silent=True)
#         self.moves.append("rrr")

#     def sort_2(self):
#         if not self.check_sorted():
#             self.ra()

#     def sort_3(self):
#         if not self.check_sorted():
#             #case 0 2 1
#             if self.stack_a[0] == 0:
#                 self.ra()
#                 self.sa()
#             #case 1 X X
#             elif self.stack_a[0] == 1:
#                 #case 1 0 2
#                 if self.stack_a[1] == 0:
#                     self.sa()def check_input(x):
    # Stub for your original input checks
    pass
#                 #case 1 2 0
#                 else:
#                     self.ra()
#             #case 2 X X
#             else:
#                 #case 2 0 1:
#                 if self.stack_a[1] == 0:
#                     self.rra()
#                 #case 2 1 0
#                 else:
#                     self.sa()
#                     self.ra()

#     def sort_large(self):
#         if len(self.stack_a) <= 1 or self.check_sorted():
#             return

#         max_num = max(self.stack_a)
#         max_bits = max_num.bit_length()

#         for bit in range(max_bits):
#             size = len(self.stack_a)
#             for _ in range(size):
#                 top_val = self.stack_a[0]
#                 if ((top_val >> bit) & 1) == 0:
#                     self.pb()
#                 else:
#                     self.ra()

#             # Debug: show partial result
#             # print(f"End of bit {bit} partition => stack_a: {self.stack_a}, stack_b: {self.stack_b}")

#             # push everything back
#             while self.stack_b:
#                 self.pa()

#             # Debug: show stack after pushing back
#             # print(f"After bit {bit}, stack_a: {self.stack_a}\n")

#         # Check final
#         # print("Final stack A:", self.stack_a)
#         # print("Check sorted?", self.check_sorted())


# def get_sorted(to_sort):
#     to_return = []
#     for i in range(len(to_sort)):
#         to_return.append(0)
#         for j in to_sort:
#             if j < to_sort[i]:
#                 to_return[i]+=1
#     return to_return



# if __name__ == "__main__":
#     input_data = random.sample(range(100), 10
#                                )  # smaller range for demo
#     stack = stacks(input_data)
#     # Perform your "large" sort:
#     stack.sort()
#     print(len(stack.moves))
#     # For reference, see the final result & moves:
#     # print("Final stack A:", stack.stack_a)
#     # print("Moves used:", stack.moves)
