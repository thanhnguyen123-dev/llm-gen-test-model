package org.example;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Rigorous JUnit 5 tests for the AddTwo class.
 * Covers typical cases, edge cases, corner cases, and overflow/underflow behavior.
 */
class AddTwoTest {

    private AddTwo addTwo;

    @BeforeEach
    void setUp() {
        addTwo = new AddTwo();
    }

    // COMMON CASES

    @Test
    @DisplayName("Test adding two positive numbers")
    void testAddTwoPositiveNumbers() {
        assertEquals(5, addTwo.add(2, 3), "Adding 2 and 3 should result in 5");
        assertEquals(100, addTwo.add(50, 50), "Adding 50 and 50 should result in 100");
        assertEquals(999, addTwo.add(123, 876), "Adding 123 and 876 should result in 999");
    }

    @Test
    @DisplayName("Test adding two negative numbers")
    void testAddTwoNegativeNumbers() {
        assertEquals(-5, addTwo.add(-2, -3), "Adding -2 and -3 should result in -5");
        assertEquals(-100, addTwo.add(-50, -50), "Adding -50 and -50 should result in -100");
        assertEquals(-999, addTwo.add(-123, -876), "Adding -123 and -876 should result in -999");
    }

    @Test
    @DisplayName("Test adding a positive and a negative number (positive result)")
    void testAddPositiveAndNegativeResultingInPositive() {
        assertEquals(2, addTwo.add(5, -3), "Adding 5 and -3 should result in 2");
        assertEquals(10, addTwo.add(-5, 15), "Adding -5 and 15 should result in 10");
    }

    @Test
    @DisplayName("Test adding a positive and a negative number (negative result)")
    void testAddPositiveAndNegativeResultingInNegative() {
        assertEquals(-2, addTwo.add(-5, 3), "Adding -5 and 3 should result in -2");
        assertEquals(-10, addTwo.add(5, -15), "Adding 5 and -15 should result in -10");
    }

    @Test
    @DisplayName("Test adding a positive and a negative number (zero result)")
    void testAddPositiveAndNegativeResultingInZero() {
        assertEquals(0, addTwo.add(5, -5), "Adding 5 and -5 should result in 0");
        assertEquals(0, addTwo.add(-100, 100), "Adding -100 and 100 should result in 0");
    }

    // EDGE CASES (involving zeroes)

    @Test
    @DisplayName("Test adding zero to a positive number")
    void testAddZeroToPositive() {
        assertEquals(5, addTwo.add(0, 5), "Adding 0 and 5 should result in 5");
        assertEquals(5, addTwo.add(5, 0), "Adding 5 and 0 should result in 5 (commutativity)");
    }

    @Test
    @DisplayName("Test adding zero to a negative number")
    void testAddZeroToNegative() {
        assertEquals(-5, addTwo.add(0, -5), "Adding 0 and -5 should result in -5");
        assertEquals(-5, addTwo.add(-5, 0), "Adding -5 and 0 should result in -5 (commutativity)");
    }

    @Test
    @DisplayName("Test adding zero to zero")
    void testAddZeroToZero() {
        assertEquals(0, addTwo.add(0, 0), "Adding 0 and 0 should result in 0");
    }

    // EDGE CASES (integer limits)

    @Test
    @DisplayName("Test adding involving Integer.MAX_VALUE")
    void testAddWithMaxValue() {
        assertEquals(Integer.MAX_VALUE, addTwo.add(Integer.MAX_VALUE, 0), "Adding MAX_VALUE and 0 should be MAX_VALUE");
        assertEquals(Integer.MAX_VALUE - 1, addTwo.add(Integer.MAX_VALUE, -1), "Adding MAX_VALUE and -1");
        assertEquals(0, addTwo.add(Integer.MAX_VALUE, -Integer.MAX_VALUE), "Adding MAX_VALUE and -MAX_VALUE");
    }

    @Test
    @DisplayName("Test adding involving Integer.MIN_VALUE")
    void testAddWithMinValue() {
        assertEquals(Integer.MIN_VALUE, addTwo.add(Integer.MIN_VALUE, 0), "Adding MIN_VALUE and 0 should be MIN_VALUE");
        assertEquals(Integer.MIN_VALUE + 1, addTwo.add(Integer.MIN_VALUE, 1), "Adding MIN_VALUE and 1");
        assertEquals(-1, addTwo.add(Integer.MIN_VALUE, Integer.MAX_VALUE), "Adding MIN_VALUE and MAX_VALUE should be -1");
        //
    }

    // --- Corner Cases / Error-like Cases (Integer Overflow/Underflow) ---
    // Java integer addition wraps around on overflow/underflow, it does not throw an exception.
    // These tests verify the wrap-around behavior.

    @Test
    @DisplayName("Test integer overflow (positive wrap-around)")
    void testPositiveOverflow() {
        // MAX_VALUE is 2^31 - 1. Adding 1 should wrap to MIN_VALUE (-2^31).
        assertEquals(Integer.MIN_VALUE, addTwo.add(Integer.MAX_VALUE, 1),
                "Adding 1 to MAX_VALUE should overflow to MIN_VALUE");
        assertEquals(Integer.MIN_VALUE + 9, addTwo.add(Integer.MAX_VALUE - 10, 20),
                "Adding large numbers causing overflow");
    }

    @Test
    @DisplayName("Test integer underflow (negative wrap-around)")
    void testNegativeUnderflow() {
        // MIN_VALUE is -2^31. Subtracting 1 (adding -1) should wrap to MAX_VALUE (2^31 - 1).
        assertEquals(Integer.MAX_VALUE, addTwo.add(Integer.MIN_VALUE, -1),
                "Adding -1 to MIN_VALUE should underflow to MAX_VALUE");
        assertEquals(Integer.MAX_VALUE - 9, addTwo.add(Integer.MIN_VALUE + 10, -20),
                "Adding large negative numbers causing underflow");
    }

    @Test
    @DisplayName("Test adding two large positive numbers causing overflow")
    void testAddTwoLargePositivesOverflow() {
        int largeNum1 = Integer.MAX_VALUE - 100;
        int largeNum2 = 200;
        // Expected result is (MAX_VALUE - 100) + 200 = MAX_VALUE + 100
        // This overflows. MAX_VALUE + 1 = MIN_VALUE
        // MAX_VALUE + 100 = MIN_VALUE + 99
        int expected = Integer.MIN_VALUE + 99;
        assertEquals(expected, addTwo.add(largeNum1, largeNum2),
                "Adding two large positive numbers should cause overflow and wrap around");
    }

    @Test
    @DisplayName("Test adding two large negative numbers causing underflow")
    void testAddTwoLargeNegativesUnderflow() {
        int largeNum1 = Integer.MIN_VALUE + 100;
        int largeNum2 = -200;
        // Expected result is (MIN_VALUE + 100) - 200 = MIN_VALUE - 100
        // This underflows. MIN_VALUE - 1 = MAX_VALUE
        // MIN_VALUE - 100 = MAX_VALUE - 99
        int expected = Integer.MAX_VALUE - 99;
        assertEquals(expected, addTwo.add(largeNum1, largeNum2),
                "Adding two large negative numbers should cause underflow and wrap around");
    }
}