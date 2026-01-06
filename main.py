import algorithms


def example_algorithms():
    """
    Demonstrates the usage of binary search and bubble sort algorithms.
    """
    print("--- Bubble Sort Example ---")
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original list: {unsorted_list}")
    
    sorted_list = algorithms.bubble_sort(unsorted_list)
    print(f"Sorted list:   {sorted_list}")
    print()

    print("--- Binary Search Example ---")
    # Using the sorted list from bubble sort for binary search (binary search requires sorted input)
    target = 22
    print(f"Searching for target: {target}")
    
    result_index = algorithms.binary_search(sorted_list, target)
    
    if result_index != -1:
        print(f"Element found at index: {result_index}")
    else:
        print("Element not found in list")
        
    # Test with an element that doesn't exist
    target_not_found = 100
    print(f"Searching for target: {target_not_found}")
    result_index_nf = algorithms.binary_search(sorted_list, target_not_found)
    
    if result_index_nf != -1:
        print(f"Element found at index: {result_index_nf}")
    else:
        print("Element not found in list")


def main():
    """
    Main entry point of the application.
    """
    example_algorithms()


if __name__ == "__main__":
    main()
