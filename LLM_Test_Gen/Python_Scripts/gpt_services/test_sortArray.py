from simple_prompt import get_prompt
from openai_service import generate_test_for_simple_prompt

if __name__ == "__main__":
    prompt = get_prompt()
    sortArray_code_knowledge = """
    - FQN: org.example.TheArray.sortArray(int[])
    - Signature: void sortArray(int[])
    - Jimple Code:
    {
        int[] array;
        org.example.TheArray this;
        unknown $stack10, $stack11, $stack12, $stack13, $stack14, $stack15, $stack16, $stack17, $stack18, $stack19, $stack20, $stack21, $stack6, $stack7, $stack8, $stack9, i, j, n, temp;


        this := @this: org.example.TheArray;
        array := @parameter0: int[];
        n = lengthof array;
        i = 0;

      label1:
        $stack11 = i;
        $stack10 = n;
        $stack9 = 1;
        $stack6 = $stack10 - $stack9;

        if $stack11 >= $stack6 goto label5;
        j = 0;

      label2:
        $stack18 = j;
        $stack16 = n;
        $stack15 = i;
        $stack7 = $stack16 - $stack15;
        $stack17 = 1;
        $stack8 = $stack7 - $stack17;

        if $stack18 >= $stack8 goto label4;
        $stack14 = array[j];
        $stack12 = j + 1;
        $stack13 = array[$stack12];

        if $stack14 <= $stack13 goto label3;
        temp = array[j];
        $stack19 = j + 1;
        $stack20 = array[$stack19];
        array[j] = $stack20;
        $stack21 = j + 1;
        array[$stack21] = temp;

      label3:
        j = j + 1;

        goto label2;

      label4:
        i = i + 1;

        goto label1;

      label5:
        return;
    """
    final_prompt = prompt + "\n" + sortArray_code_knowledge
    result = generate_test_for_simple_prompt(final_prompt)
    print("Generated Test Codes:\n", result)

