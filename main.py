from sort import get_sorted
from check_input import check_input
import random

class stacks:
    def __init__(self, stack_a):
        check_input(stack_a)
        self.stack_a = get_sorted(stack_a)
        self.stack_b = []
        self.moves = []
        self.size_a = len(stack_a)

    def sort(self):
        if len(self.stack_a) < 2:
            return 0
        elif len(self.stack_a) == 2:
            print(self.stack_a)
            self.sort_2()
            print(self.stack_a)
            return self.moves
        
        elif len(self.stack_a) == 3:
            print(self.stack_a)
            self.sort_3()
            print(self.stack_a)
            return self.moves

    def check_sorted(self):
        # Checks if self.stack_a is exactly [0, 1, 2, ..., n-1]
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
        if len(self.stack_b):
            self.stack_a.insert(0, self.stack_b.pop(0))
        self.moves.append("pa")

    def pb(self):
        if len(self.stack_a):
            self.stack_b.insert(0, self.stack_a.pop(0))
        self.moves.append("pb")

    def ra(self, silent=False):
        if len(self.stack_a) > 1:
            self.stack_a.insert(0, self.stack_a.pop())
            if not silent:
                self.moves.append("ra")

    def rb(self, silent=False):
        if len(self.stack_b) > 1:
            self.stack_b.insert(0, self.stack_b.pop())
            if not silent:
                self.moves.append("rb")
    
    def rr(self):
        self.ra(silent=True)
        self.rb(silent=True)
        self.moves.append("rr")

    def rra(self, silent=False):
        if len(self.stack_a) > 1:
            self.stack_a.append(self.stack_a.pop(0))
            if not silent:
                self.moves.append("rra")

    def rrb(self, silent=False):
        if len(self.stack_b) > 1:
            self.stack_b.append(self.stack_b.pop(0))
            if not silent:
                self.moves.append("rrb")

    def rrr(self):
        self.rra(silent=True)
        self.rrb(silent=True)
        self.moves.append("rrr")

    def sort_2(self):
        if not self.check_sorted():
            self.ra()

    def sort_3(self):
        if not self.check_sorted():
            #case 0 2 1
            if self.stack_a[0] == 0:
                self.ra()
                self.sa()
            #case 1 X X
            elif self.stack_a[0] == 1:
                #case 1 0 2
                if self.stack_a[1] == 0:
                    self.sa()
                #case 1 2 0
                else:
                    self.ra()
            #case 2 X X
            else:
                #case 2 0 1:
                if self.stack_a[1] == 0:
                    self.rra()
                #case 2 1 0
                else:
                    self.sa()
                    self.ra()

    # -----------------------------------------------------------------
    # The main "larger" sorting logic:
    # -----------------------------------------------------------------
    def sort_large(self):
        """
        1) Partition stack A to create a 'cluster' (via find_start & push_list).
        2) Repeatedly find the next cluster in B, rotate B so the cluster's smallest is on top,
           and push that cluster back to A.
        3) Sort the final cluster in A.
        4) Move the smallest value to the top (position 1).
        """

        # If stack A is already perfectly sorted [0,1,2,...], just return.
        if self.check_sorted():
            return

        # 1) Partition stack A into a cluster (pushing all "non-cluster" elements to B)
        #    This step picks up a subset of A (marked with 1) and rotates them,
        #    while pushing the 0-marked elements to B
        start_a = self.find_start("a")
        self.push_list("a", start_a)
        print("After partitioning A => B, stack A:", self.stack_a)
        print("Stack B:", self.stack_b)
        self.sort_cluster("a")

        # 2) Repeatedly find next cluster in B, rotate so smallest is on top,
        #    push that cluster back to A
        while len(self.stack_b) > 0:
            # find cluster in B
            next_cluster_b = self.find_start("b")

            # (Optional) rotate B so that the cluster's smallest element is on top
            # We find the smallest element index among those that are part of the cluster (marked 1).
            idxs_in_cluster = [i for i, mark in enumerate(next_cluster_b) if mark == 1]
            if not idxs_in_cluster:
                # If there's no "1" at all, that means everything is "not in cluster"
                # so effectively push all B -> A or break
                # We'll just push_list anyway; that will push everything not in cluster
                # But let's handle it gracefully:
                self.push_list("b", next_cluster_b)
                self.sort_cluster("a")
                continue

            # Find the index of the global smallest among the "1"s
            smallest_index = min(idxs_in_cluster, key=lambda i: self.stack_b[i])

            # Decide whether to rotate forward or backward
            if smallest_index <= len(self.stack_b)//2:
                for _ in range(smallest_index):
                    self.rb()
            else:
                for _ in range(len(self.stack_b) - smallest_index):
                    self.rrb()

            # Now push the "non-cluster" from B to A, rotating the cluster in place
            self.push_list("b", next_cluster_b)
            print("After pushing cluster from B => A, stack A:", self.stack_a)
            print("Stack B:", self.stack_b)

        # 3) Finally, with everything in A, do a quick cluster-sort on A 
        self.sort_cluster("a")

        # 4) Move the smallest value to the top (index 0)
        if len(self.stack_a) > 1:
            idx_min = min(range(len(self.stack_a)), key=lambda i: self.stack_a[i])
            # rotate forward or backward
            if idx_min <= len(self.stack_a)//2:
                for _ in range(idx_min):
                    self.ra()
            else:
                for _ in range(len(self.stack_a) - idx_min):
                    self.rra()

        print("Final stack A:", self.stack_a)
        print("Moves:", self.moves)

    # -----------------------------------------------------------------
    #  Helper methods for "clusters":
    # -----------------------------------------------------------------
    def find_start(self, stack="a"):
        """
        Looks for a subset of the given stack that can be considered
        a 'cluster' by building up the largest run within +/- 3
        (per your original logic). 
        Returns a list of 0/1 indicating membership in that cluster.
        """
        best_start_sort = []
        best_start_size = 0
        st = self.stack_a if stack == "a" else self.stack_b

        if len(st) == 0:
            return []
        
        if len(st) < 5:
            return [0] * len(st)

        for i, j in enumerate(st):
            track = 0
            to_push = [0]*len(st)
            for k in range(len(st)):
                # shift(...) gets some index offset
                # res is self.stack_a[ shifted_index ], compared to j
                # if it's within track ± 3, mark that as part of the cluster
                if track - 3 < (res := self.shift(self.stack_a[self.shift(k, i)], j)) < track + 3:
                    track += 1
                    to_push[self.shift(k, i)] = 1
            if track > best_start_size:
                best_start_size = track
                best_start_sort = to_push
        return best_start_sort

    def shift(self, i, j):
        return (len(self.stack_a) + i - j) % len(self.stack_a)

    def push_list(self, stack, lst):
        pshd = 0
        st = self.stack_a if stack == "a" else self.stack_b
        size_st = len(st)

        if size_st <= 1:
            return

        for i in range(size_st):
            # Compare current element vs next (cyclically),
            # if out of order, apply 'sa' or 'sb'
            cur_idx = (i - pshd) % size_st
            nxt_idx = ((i + 1) - pshd) % size_st

            # Because st changes as we push/rotate, guard if it becomes too short
            if len(st) > 1:
                if st[nxt_idx % len(st)] < st[cur_idx]:
                    if stack == "a":
                        self.sa()
                    else:
                        self.sb()
                    # also swap bits in lst to keep them aligned
                    lst[i], lst[(i+1) % size_st] = lst[(i+1) % size_st], lst[i]

            # Now push or rotate based on lst[i]
            if stack == "a":
                if not lst[i]:    # i.e. 0 => push from A to B
                    self.pb()
                    pshd += 1
                else:
                    self.rra()
            else:
                if not lst[i]:    # i.e. 0 => push from B to A
                    self.pa()
                    pshd += 1
                else:
                    self.rrb()

    def check_in_order(self, stack):
        st = self.stack_a if stack == "a" else self.stack_b
        if len(st) <= 1:
            return True
        for i in range(len(st) - 1):
            if st[i] > st[i+1]:
                return False
        return True

    def sort_cluster(self, stack):
        """
        Sorts the cluster in-place using a bubble-sort-by-rotation approach.
        This will rotate through the stack, swapping out-of-order pairs, until
        the entire cluster is in ascending order.
        """
        st = self.stack_a if stack == "a" else self.stack_b
        
        # If there's 0 or 1 element, or it's already in order, nothing to do
        if len(st) < 2 or self.check_in_order(stack):
            return

        while not self.check_in_order(stack):
            swapped = False
            
            # One full "bubble" pass through the stack, rotating forward
            for _ in range(len(st) - 1):
                # Compare top two; if out of order, swap
                if st[0] > st[1]:
                    if stack == "a":
                        self.sa()
                    else:
                        self.sb()
                    swapped = True

                # Rotate so we can compare the next pair on the next iteration
                if stack == "a":
                    self.ra()
                else:
                    self.rb()

            # After the pass, rotate back to the original top
            for _ in range(len(st) - 1):
                if stack == "a":
                    self.rra()
                else:
                    self.rrb()

            # If we went through a whole pass with no swaps, we're done
            if not swapped:
                break


if __name__ == "__main__":
    input_data = random.sample(range(100), 10)  # smaller range for demo
    stack = stacks(input_data)
    # Perform your "large" sort:
    stack.sort_large()
    print(len(stack.moves))
    # For reference, see the final result & moves:
    # print("Final stack A:", stack.stack_a)
    # print("Moves used:", stack.moves)
