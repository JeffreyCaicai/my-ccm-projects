from typing import List, Optional, TypeVar

T = TypeVar('T', int, float)


def binary_search(arr: List[T], target: T) -> int:
    """
    Performs binary search on a sorted list to find the index of a target value.

    Args:
        arr (List[T]): A sorted list of elements (int or float).
        target (T): The element to search for.

    Returns:
        int: The index of the target element if found, otherwise -1.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def bubble_sort(arr: List[T]) -> List[T]:
    """
    Sorts a list of elements using the bubble sort algorithm.
    This function returns a new sorted list and leaves the original list unchanged.

    Args:
        arr (List[T]): A list of elements to be sorted.

    Returns:
        List[T]: A new list containing the sorted elements.
    """
    n = len(arr)
    # Create a copy to avoid modifying the original list
    sorted_arr = arr.copy()
    
    for i in range(n):
        # Track if any swap happens in this pass
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
        
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
            
    return sorted_arr
