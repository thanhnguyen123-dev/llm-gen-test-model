package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Rigorous JUnit 5 tests for the TheArray class's sortArray method.
 * Covers typical cases, edge cases, and error handling.
 */
class TheArrayTest {

    private TheArray theArray;

    @BeforeEach
    void setUp() {
        theArray = new TheArray();
    }

    // TYPICAL CASES

    @Test
    @DisplayName("Test sorting an unsorted array of positive numbers")
    void testSortUnsortedPositiveNumbers() {
        int[] array = {5, 3, 8, 1, 2};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {1, 2, 3, 5, 8}, array, "Array should be sorted to [1, 2, 3, 5, 8]");
    }

    @Test
    @DisplayName("Test sorting an unsorted array with negative and positive numbers")
    void testSortUnsortedMixedNumbers() {
        int[] array = {-3, 0, 2, -5, 4};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {-5, -3, 0, 2, 4}, array, "Array should be sorted to [-5, -3, 0, 2, 4]");
    }

    // EDGE CASES

    @Test
    @DisplayName("Test sorting an empty array")
    void testSortEmptyArray() {
        int[] array = {};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {}, array, "Empty array should remain empty");
    }

    @Test
    @DisplayName("Test sorting a single-element array")
    void testSortSingleElementArray() {
        int[] array = {42};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {42}, array, "Single-element array should remain unchanged");
    }

    @Test
    @DisplayName("Test sorting an array with all identical elements")
    void testSortAllIdenticalElements() {
        int[] array = {7, 7, 7, 7};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {7, 7, 7, 7}, array, "Array of identical elements should remain unchanged");
    }

    @Test
    @DisplayName("Test sorting an already sorted array")
    void testSortAlreadySortedArray() {
        int[] array = {1, 2, 3, 4, 5};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {1, 2, 3, 4, 5}, array, "Already sorted array should remain unchanged");
    }

    @Test
    @DisplayName("Test sorting an array sorted in reverse order")
    void testSortReverseSortedArray() {
        int[] array = {5, 4, 3, 2, 1};
        theArray.sortArray(array);
        assertArrayEquals(new int[] {1, 2, 3, 4, 5}, array, "Reverse sorted array should be sorted to [1, 2, 3, 4, 5]");
    }

    // ERROR CASES

    @Test
    @DisplayName("Test sorting a null array")
    void testSortNullArray() {
        int[] array = null;

        assertThrows(NullPointerException.class, () -> {
            theArray.sortArray(array);
        }, "Sorting a null array should throw a NullPointerException");
    }
}