from check_input import check_input
import random
import matplotlib.pyplot as plt

def rot(li, idx):
    return li[idx:]+li[:idx]

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



    def _lis_indices_single(self, arr):
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
            lis_idx.append(arr[cur])
            cur = parent[cur]
        lis_idx.reverse() 

        return set(lis_idx)
    
    def _lis_indices(self, arr):
        if len(arr) == 1:
            return set(arr)
        best_set = set()
        for i in range(len(arr)):
            new_set = self._lis_indices_single(rot(arr, i))
            best_set = new_set if (len(new_set) > len(best_set)) else best_set
        return best_set
        
    def _best_insert_position_in_a(self, val):
        arr = self.stack_a
        if not arr:
            return 0  # A is empty => top is the only place

        if val < min(arr):
            return arr.index(min(arr))
        if val > max(arr):
            return arr.index(max(arr)) + 1

        diffs = [(i-val) for i in arr]
        value_diff = min(i for i in diffs if i > 0)
        return(diffs.index(value_diff))

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
        for i in range(len(self.stack_a)):
            if arr[1] + 1 == arr[0]:
                self.sa()
            if arr[0] in lis_set:            
                self.ra()
            else:
                self.pb()

      
        while self.stack_b:
            best_cost = float('inf')
            best_idx_b = 0
            best_idx_a = 0

            for idx_b, val in enumerate(self.stack_b):
                idx_a = self._best_insert_position_in_a(val)

                # cost model: how many operations required
                size_a = len(self.stack_a)
                size_b = len(self.stack_b)

                dist_a = idx_a if idx_a <= size_a // 2 else size_a - idx_a
                dist_b = idx_b if idx_b <= size_b // 2 else size_b - idx_b
                total_cost = max(dist_a, dist_b)  # rough estimate, more accurate models are possible

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_idx_b = idx_b
                    best_idx_a = idx_a

            self._rotate_both_min_cost(best_idx_a, best_idx_b)
            self.pa()


        if self.stack_a.index(0) < (len(self.stack_a)/2):
            while self.stack_a[0] != 0:
                self.ra()
        else:
            while self.stack_a[0] != 0:
                self.rra()

        if (not self.check_sorted()):
            ValueError("Not Sorted!")
        
    def sort_2(self):
        if not self.check_sorted():
            self.sa()

    def sort_3(self):
        pass


#
# Demo
#
if __name__ == "__main__":

    input_data = random.sample(range(1000), 500)  # distinct integers from 0..99
    s = stacks(input_data)
    s.sort_large()
    print (len(s.moves))

