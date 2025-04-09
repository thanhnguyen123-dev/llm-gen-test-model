package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Rigorous JUnit 5 tests for the SumEven class.
 * Covers typical cases, edge cases, and special scenarios.
 */
class SumEvenTest {

    private SumEven sumEven;

    @BeforeEach
    void setUp() {
        sumEven = new SumEven();
    }

    // TYPICAL CASES

    @Test
    @DisplayName("Test sum of even numbers in an array of positive numbers")
    void testSumEvenPositiveNumbers() {
        int[] array = {1, 2, 3, 4, 5, 6};
        assertEquals(12, sumEven.sumEven(array), "Sum of evens should be 12 in [1, 2, 3, 4, 5, 6]");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array of negative numbers")
    void testSumEvenNegativeNumbers() {
        int[] array = {-1, -2, -3, -4, -5, -6};
        assertEquals(-12, sumEven.sumEven(array), "Sum of evens should be -12 in [-1, -2, -3, -4, -5, -6]");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with mixed positive, negative, and zero numbers")
    void testSumEvenMixedNumbers() {
        int[] array = {0, -2, 3, 5, 6, -7, -8};
        assertEquals(-4, sumEven.sumEven(array), "Sum of evens should be -4 in [0, -2, 3, 5, 6, -7, -8]");
    }

    // EDGE CASES

    @Test
    @DisplayName("Test sum of even numbers in a single-element array (even number)")
    void testSumEvenSingleEven() {
        int[] array = {8};
        assertEquals(8, sumEven.sumEven(array), "Sum should be 8 for single-element even array [8]");
    }

    @Test
    @DisplayName("Test sum of even numbers in a single-element array (odd number)")
    void testSumEvenSingleOdd() {
        int[] array = {7};
        assertEquals(0, sumEven.sumEven(array), "Sum should be 0 for single-element odd array [7]");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with two even numbers")
    void testSumEvenTwoEvens() {
        int[] array = {2, 4};
        assertEquals(6, sumEven.sumEven(array), "Sum of evens should be 6 in [2, 4]");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with all odd numbers")
    void testSumEvenAllOdds() {
        int[] array = {1, 3, 5, 7, 9};
        assertEquals(0, sumEven.sumEven(array), "Sum should be 0 for array of all odd numbers");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with all even numbers")
    void testSumEvenAllEvens() {
        int[] array = {2, 4, 6, 8, 10};
        assertEquals(30, sumEven.sumEven(array), "Sum of evens should be 30 for array of all evens");
    }

    @Test
    @DisplayName("Test sum of even numbers in an empty array")
    void testSumEvenEmptyArray() {
        int[] array = {};
        assertEquals(0, sumEven.sumEven(array), "Sum should be 0 for empty array");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with zeroes")
    void testSumEvenWithZeroes() {
        int[] array = {0, 0, 0};
        assertEquals(0, sumEven.sumEven(array), "Sum should be 0 for array of zeroes");
    }

    @Test
    @DisplayName("Test sum of even numbers in an array with Integer.MAX_VALUE and Integer.MIN_VALUE")
    void testSumEvenWithExtremeValues() {
        int[] array = {Integer.MAX_VALUE, Integer.MIN_VALUE, 2};
        assertEquals(Integer.MIN_VALUE + 2, sumEven.sumEven(array), "Sum should consider only valid even integers");
    }

    @Test
    @DisplayName("Test sum of even numbers in a null array")
    void testSumEvenNullArray() {
        int[] array = null;
        assertEquals(0, sumEven.sumEven(array), "Sum should be 0 for null array");
    }
}