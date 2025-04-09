package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Rigorous JUnit 5 tests for the FindMin class.
 * Covers typical cases, edge cases, corner cases, and error handling.
 */
class FindMinTest {

    private FindMin findMin;

    @BeforeEach
    void setUp() {
        findMin = new FindMin();
    }

    // TYPICAL CASES

    @Test
    @DisplayName("Test finding min in an array with positive numbers")
    void testFindMinPositiveNumbers() {
        int[] array = {5, 1, 8, 3, 2};
        assertEquals(1, findMin.findMin(array), "Min should be 1 in [5, 1, 8, 3, 2]");
    }

    @Test
    @DisplayName("Test finding min in an array with negative numbers")
    void testFindMinNegativeNumbers() {
        int[] array = {-5, -1, -8, -3, -2};
        assertEquals(-8, findMin.findMin(array), "Min should be -8 in [-5, -1, -8, -3, -2]");
    }

    @Test
    @DisplayName("Test finding min in an array with mixed positive, negative, and zero numbers")
    void testFindMinMixedNumbers() {
        int[] array = {5, -1, 8, 0, -3, 2};
        assertEquals(-3, findMin.findMin(array), "Min should be -3 in [5, -1, 8, 0, -3, 2]");
    }

    @Test
    @DisplayName("Test finding min when min is the first element")
    void testFindMinWhenMinIsFirst() {
        int[] array = {1, 5, 8, 3, 2};
        assertEquals(1, findMin.findMin(array), "Min should be 1 when it's the first element");
    }

    @Test
    @DisplayName("Test finding min when min is the last element")
    void testFindMinWhenMinIsLast() {
        int[] array = {5, 8, 3, 2, 1};
        assertEquals(1, findMin.findMin(array), "Min should be 1 when it's the last element");
    }

    @Test
    @DisplayName("Test finding min in an array with duplicate minimum values")
    void testFindMinWithDuplicates() {
        int[] array = {5, 1, 8, 1, 3, 2};
        assertEquals(1, findMin.findMin(array), "Min should be 1 even with duplicates");
    }

    // EDGE CASES (Array Size)

    @Test
    @DisplayName("Test finding min in a single-element array")
    void testFindMinSingleElementArray() {
        int[] array = {42};
        assertEquals(42, findMin.findMin(array), "Min in a single-element array should be the element itself");

        int[] arrayNegative = {-99};
        assertEquals(-99, findMin.findMin(arrayNegative), "Min in a single negative element array");
    }

    @Test
    @DisplayName("Test finding min in a two-element array (min first)")
    void testFindMinTwoElementsMinFirst() {
        int[] array = {5, 10};
        assertEquals(5, findMin.findMin(array), "Min should be 5 in [5, 10]");
    }

    @Test
    @DisplayName("Test finding min in a two-element array (min last)")
    void testFindMinTwoElementsMinLast() {
        int[] array = {10, 5};
        assertEquals(5, findMin.findMin(array), "Min should be 5 in [10, 5]");
    }

    // EDGE CASES (Special Values)

    @Test
    @DisplayName("Test finding min in an array containing Integer.MIN_VALUE")
    void testFindMinWithMinValue() {
        int[] array = {10, -50, Integer.MIN_VALUE, 0};
        assertEquals(Integer.MIN_VALUE, findMin.findMin(array), "Min should be Integer.MIN_VALUE");
    }

    @Test
    @DisplayName("Test finding min in an array containing Integer.MAX_VALUE")
    void testFindMinWithMaxValue() {
        // Min is MAX_VALUE only if it's the *only* element or all elements are MAX_VALUE
        int[] arrayWithMax = {Integer.MAX_VALUE};
        assertEquals(Integer.MAX_VALUE, findMin.findMin(arrayWithMax), "Min should be Integer.MAX_VALUE if it's the only element");

        int[] arrayWithMaxAndOthers = {Integer.MAX_VALUE, 100, 200};
        assertEquals(100, findMin.findMin(arrayWithMaxAndOthers), "Min should be 100 when Integer.MAX_VALUE is present but not min");
    }

    @Test
    @DisplayName("Test finding min in an array containing both Integer.MIN_VALUE and Integer.MAX_VALUE")
    void testFindMinWithMinAndMaxValues() {
        int[] array = {0, Integer.MAX_VALUE, -50, Integer.MIN_VALUE, 100};
        assertEquals(Integer.MIN_VALUE, findMin.findMin(array), "Min should be Integer.MIN_VALUE when both MIN and MAX are present");
    }

    @Test
    @DisplayName("Test finding min in an array with all identical elements")
    void testFindMinAllIdentical() {
        int[] array = {7, 7, 7, 7, 7};
        assertEquals(7, findMin.findMin(array), "Min in an array of identical elements should be that element");
    }

    @Test
    @DisplayName("Test finding min in an array with all zeros")
    void testFindMinAllZeros() {
        int[] array = {0, 0, 0, 0};
        assertEquals(0, findMin.findMin(array), "Min in an array of zeros should be 0");
    }


    // ERROR CASES (Invalid Input)

    @Test
    @DisplayName("Test finding min in a null array")
    void testFindMinNullArray() {
        int[] array = null;
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            findMin.findMin(array);
        }, "Should throw IllegalArgumentException for null array");

        // Verify the exception message for completeness
        assertEquals("Array cannot be null or empty", exception.getMessage(), "Exception message should match expected");
    }

    @Test
    @DisplayName("Test finding min in an empty array")
    void testFindMinEmptyArray() {
        int[] array = {}; // Equivalent to new int[0]
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            findMin.findMin(array);
        }, "Should throw IllegalArgumentException for empty array");

        // Verify the exception message for completeness
        assertEquals("Array cannot be null or empty", exception.getMessage(), "Exception message should match expected");
    }
}