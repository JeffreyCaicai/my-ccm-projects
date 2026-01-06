import unittest
from algorithms import binary_search, bubble_sort

class TestAlgorithms(unittest.TestCase):

    def test_binary_search_found(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(binary_search(arr, 3), 2)
        self.assertEqual(binary_search(arr, 1), 0)
        self.assertEqual(binary_search(arr, 5), 4)

    def test_binary_search_not_found(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(binary_search(arr, 6), -1)
        self.assertEqual(binary_search(arr, 0), -1)

    def test_binary_search_empty(self):
        self.assertEqual(binary_search([], 1), -1)

    def test_binary_search_single(self):
        self.assertEqual(binary_search([5], 5), 0)
        self.assertEqual(binary_search([5], 1), -1)

    def test_bubble_sort_unsorted(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = bubble_sort(arr)
        self.assertEqual(sorted_arr, [11, 12, 22, 25, 34, 64, 90])
        # Ensure original list is not modified
        self.assertEqual(arr, [64, 34, 25, 12, 22, 11, 90])

    def test_bubble_sort_sorted(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(bubble_sort(arr), [1, 2, 3, 4, 5])

    def test_bubble_sort_reverse(self):
        arr = [5, 4, 3, 2, 1]
        self.assertEqual(bubble_sort(arr), [1, 2, 3, 4, 5])

    def test_bubble_sort_empty(self):
        self.assertEqual(bubble_sort([]), [])

    def test_bubble_sort_single(self):
        self.assertEqual(bubble_sort([1]), [1])

    def test_bubble_sort_float(self):
        arr = [3.3, 1.1, 2.2]
        self.assertEqual(bubble_sort(arr), [1.1, 2.2, 3.3])

if __name__ == '__main__':
    unittest.main()
