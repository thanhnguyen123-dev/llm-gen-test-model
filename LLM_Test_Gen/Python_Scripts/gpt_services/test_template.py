from openai_service import generate_test_for_prompt_template

if __name__ == "__main__":
    # test for sumEven
    fqn = "org.example.SumEven.sumEven(int[])"
    signature = "int sumEven(int[])"
    jimple_code = """
    {
        int[] arr;
        org.example.SumEven this;
        unknown $stack10, $stack11, $stack7, $stack8, $stack9, l3, l4, l5, num, sum;
    
    
        this := @this: org.example.SumEven;
        arr := @parameter0: int[];
    
        if arr == null goto label1;
        $stack7 = lengthof arr;
    
        if $stack7 != 0 goto label2;
    
      label1:
        $stack11 = 0;
    
        return $stack11;
    
      label2:
        sum = 0;
        l3 = arr;
        l4 = lengthof l3;
        l5 = 0;
    
      label3:
        $stack10 = l5;
        $stack9 = l4;
    
        if $stack10 >= $stack9 goto label5;
        num = l3[l5];
        $stack8 = num % 2;
    
        if $stack8 != 0 goto label4;
        sum = sum + num;
    
      label4:
        l5 = l5 + 1;
    
        goto label3;
    
      label5:
        return sum;
    }
    """

    output_for_sumEven = generate_test_for_prompt_template(fqn, signature, jimple_code)
    print(output_for_sumEven)



