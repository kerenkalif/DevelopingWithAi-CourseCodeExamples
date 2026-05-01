import unittest

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

class TestBubbleSort(unittest.TestCase):

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort([4, 2, 1, 3]), [1, 2, 3, 4])
        self.assertEqual(bubble_sort([5, 3, 8, 1, 2]), [1, 2, 3, 5, 8])
        self.assertEqual(bubble_sort([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(bubble_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()