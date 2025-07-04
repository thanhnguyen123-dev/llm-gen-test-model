prompt = """
You are provided with the following code knowledge:
- Fully Qualified Name (FQN): It uniquely identifies the method, preventing conflicts with
other methods of the same name across different packages. Providing the FQN helps the
LLM correctly reference the focal method within the project structure. The format of FQN
is packageName.ClassName.MethodName(ParameterTypes).
- Signature: It defines the input and return types, helping the LLM generate appropriate
test inputs. The format of the Signature is returnType MethodName(ParameterTypes).
- Jimple Code Representation: Jimple is an intermediate representation (IR) of Java bytecode
that provides a structured, low-level view of method execution. It explicitly details variable
assignments, conditional branches, and control flow, making it useful for analyzing program
behavior.

Here are your following tasks:
- Analyze the method's parameters and behaviour from the Jimple code representation. Take a look at the 
code knowledge provided above for the definitions.
- Generate as many JUnit tests as possible that cover typical, edge cases and any error cases. You have 
to examine carefully all possibilities that could happen to make sure that we can cover all cases, try to examine as 
rigorously as possible.

User input will be the three types of code knowledge of the focal method for which tests need to need to be generated.
The expected output is a list of JUnit tests that cover all possible cases: typical, edge cases and error cases.

Here are 3 examples of the input and output. The output generated tests should be in the same format as the example.
Also note that the output generated tests in the examples achieved 100% code coverage, meaning for each example, the 
generated tests achieved 100% method coverage, 100% line coverage, and 100% branch coverage.
"""

findMin_input = """
- FQN: org.example.FindMin.findMin(int[])
- Signature: int findMin(int[])
- Jimple Code:
{
    int[] array;
    org.example.FindMin this;
    unknown $stack10, $stack4, $stack5, $stack6, $stack7, $stack8, $stack9, i, min;


    this := @this: org.example.FindMin;
    array := @parameter0: int[];

    if array == null goto label1;
    $stack5 = lengthof array;

    if $stack5 != 0 goto label2;

  label1:
    $stack4 = new java.lang.IllegalArgumentException;
    $stack10 = "Array cannot be null or empty";
    specialinvoke $stack4.<java.lang.IllegalArgumentException: void <init>(java.lang.String)>($stack10);

    throw $stack4;

  label2:
    min = array[0];
    i = 1;

  label3:
    $stack9 = i;
    $stack8 = array;
    $stack6 = lengthof $stack8;

    if $stack9 >= $stack6 goto label5;
    $stack7 = array[i];

    if $stack7 >= min goto label4;
    min = array[i];

  label4:
    i = i + 1;

    goto label3;

  label5:
    return min;
}
"""

findMin_output = """
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
"""

findMax_input = """
- FQN: org.example.FindMax.findMax(int[])
- Signature: int findMax(int[])
- Jimple Code:
{
int[] array;
org.example.FindMax this;
unknown $stack10, $stack4, $stack5, $stack6, $stack7, $stack8, $stack9, i, max;


this := @this: org.example.FindMax;
array := @parameter0: int[];

if array == null goto label1;
$stack5 = lengthof array;

if $stack5 != 0 goto label2;

label1:
$stack4 = new java.lang.IllegalArgumentException;
$stack10 = "Array cannot be null or empty";
specialinvoke $stack4.<java.lang.IllegalArgumentException: void <init>(java.lang.String)>($stack10);

throw $stack4;

label2:
max = array[0];
i = 1;

label3:
$stack9 = i;
$stack8 = array;
$stack6 = lengthof $stack8;

if $stack9 >= $stack6 goto label5;
$stack7 = array[i];

if $stack7 <= max goto label4;
max = array[i];

label4:
i = i + 1;

goto label3;

label5:
return max;
}
"""

findMax_output = """         
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
"""

addTwo_input = """
- FQN: org.example.AddTwo.add(int, int)
- Signature: int add(int, int)
- Jimple Code:
{
    int a, b;
    org.example.AddTwo this;
    unknown $stack3;


    this := @this: org.example.AddTwo;
    a := @parameter0: int;
    b := @parameter1: int;
    $stack3 = a + b;

    return $stack3;
}
"""

addTwo_output = """
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
"""

def get_prompt():
    string_builder = ""
    string_builder += prompt
    string_builder += findMin_input + "\n"
    string_builder += findMin_output + "\n"
    string_builder += findMax_input + "\n"
    string_builder += findMax_output + "\n"
    string_builder += addTwo_input + "\n"
    string_builder += addTwo_output + "\n"

    return string_builder



