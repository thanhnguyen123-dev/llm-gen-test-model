package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Rigorous JUnit 5 tests for the FindMax class.
 * Covers typical cases, edge cases, corner cases, and error handling.
 */
class FindMaxTest {

    private FindMax findMax;

    @BeforeEach
    void setUp() {
        findMax = new FindMax();
    }

    // TYPICAL CASES

    @Test
    @DisplayName("Test finding max in an array with positive numbers")
    void testFindMaxPositiveNumbers() {
        int[] array = {1, 5, 2, 8, 3};
        assertEquals(8, findMax.findMax(array), "Max should be 8 in [1, 5, 2, 8, 3]");
    }

    @Test
    @DisplayName("Test finding max in an array with negative numbers")
    void testFindMaxNegativeNumbers() {
        int[] array = {-10, -5, -20, -2, -15};
        assertEquals(-2, findMax.findMax(array), "Max should be -2 in [-10, -5, -20, -2, -15]");
    }

    @Test
    @DisplayName("Test finding max in an array with mixed positive, negative, and zero numbers")
    void testFindMaxMixedNumbers() {
        int[] array = {-5, 10, 0, -2, 3, 8};
        assertEquals(10, findMax.findMax(array), "Max should be 10 in [-5, 10, 0, -2, 3, 8]");
    }

    @Test
    @DisplayName("Test finding max when max is the first element")
    void testFindMaxWhenMaxIsFirst() {
        int[] array = {100, 10, 50, 20};
        assertEquals(100, findMax.findMax(array), "Max should be 100 when it's the first element");
    }

    @Test
    @DisplayName("Test finding max when max is the last element")
    void testFindMaxWhenMaxIsLast() {
        int[] array = {10, 50, 20, 100};
        assertEquals(100, findMax.findMax(array), "Max should be 100 when it's the last element");
    }

    @Test
    @DisplayName("Test finding max in an array with duplicate maximum values")
    void testFindMaxWithDuplicates() {
        int[] array = {5, 2, 8, 1, 8, 3};
        assertEquals(8, findMax.findMax(array), "Max should be 8 even with duplicates");
    }

    // --- Edge Cases (Array Size) ---

    @Test
    @DisplayName("Test finding max in a single-element array")
    void testFindMaxSingleElementArray() {
        int[] array = {42};
        assertEquals(42, findMax.findMax(array), "Max in a single-element array should be the element itself");
    }

    @Test
    @DisplayName("Test finding max in a two-element array (max first)")
    void testFindMaxTwoElementsMaxFirst() {
        int[] array = {10, 5};
        assertEquals(10, findMax.findMax(array), "Max should be 10 in [10, 5]");
    }

    @Test
    @DisplayName("Test finding max in a two-element array (max last)")
    void testFindMaxTwoElementsMaxLast() {
        int[] array = {5, 10};
        assertEquals(10, findMax.findMax(array), "Max should be 10 in [5, 10]");
    }

    // --- Edge Cases (Array Content) ---

    @Test
    @DisplayName("Test finding max in an array containing Integer.MAX_VALUE")
    void testFindMaxWithMaxValue() {
        int[] array = {10, Integer.MAX_VALUE, 0, -100};
        assertEquals(Integer.MAX_VALUE, findMax.findMax(array), "Max should be Integer.MAX_VALUE");
    }

    @Test
    @DisplayName("Test finding max in an array containing Integer.MIN_VALUE")
    void testFindMaxWithMinValue() {
        // Max is MIN_VALUE only if it's the *only* element or all elements are MIN_VALUE
        int[] arrayWithMin = {Integer.MIN_VALUE};
        assertEquals(Integer.MIN_VALUE, findMax.findMax(arrayWithMin), "Max should be Integer.MIN_VALUE if it's the only element");

        int[] arrayWithMinAndOthers = {Integer.MIN_VALUE, -10, -100};
        assertEquals(-10, findMax.findMax(arrayWithMinAndOthers), "Max should be -10 when Integer.MIN_VALUE is present but not max");
    }

    @Test
    @DisplayName("Test finding max in an array containing both Integer.MAX_VALUE and Integer.MIN_VALUE")
    void testFindMaxWithMinAndMaxValues() {
        int[] array = {0, Integer.MAX_VALUE, -50, Integer.MIN_VALUE, 100};
        assertEquals(Integer.MAX_VALUE, findMax.findMax(array), "Max should be Integer.MAX_VALUE when both MIN and MAX are present");
    }

    @Test
    @DisplayName("Test finding max in an array with all identical elements")
    void testFindMaxAllIdentical() {
        int[] array = {7, 7, 7, 7, 7};
        assertEquals(7, findMax.findMax(array), "Max in an array of identical elements should be that element");
    }

    @Test
    @DisplayName("Test finding max in an array with all zeros")
    void testFindMaxAllZeros() {
        int[] array = {0, 0, 0, 0};
        assertEquals(0, findMax.findMax(array), "Max in an array of zeros should be 0");
    }

    // ERROR CASES (Invalid Input)

    @Test
    @DisplayName("Test finding max in a null array")
    void testFindMaxNullArray() {
        int[] array = null;
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            findMax.findMax(array);
        }, "Should throw IllegalArgumentException for null array");

        assertEquals("Array cannot be null or empty", exception.getMessage(), "Exception message should match expected");
    }

    @Test
    @DisplayName("Test finding max in an empty array")
    void testFindMaxEmptyArray() {
        int[] array = {};
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            findMax.findMax(array);
        }, "Should throw IllegalArgumentException for empty array");

        assertEquals("Array cannot be null or empty", exception.getMessage(), "Exception message should match expected");
    }
}