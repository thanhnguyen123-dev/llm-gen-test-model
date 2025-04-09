from openai_service import generate_test_for_prompt_template

if __name__ == "__main__":
    # test for divide
    fqn = "org.example.Divider.divide(int, int)"
    signature = "int divide(int, int)"
    jimple_code = """
    {
        int a, b;
        org.example.Divider this;
        unknown $stack3, $stack4;
    
    
        this := @this: org.example.Divider;
        a := @parameter0: int;
        b := @parameter1: int;
    
        if b != 0 goto label1;
        $stack4 = new java.lang.IllegalArgumentException;
        specialinvoke $stack4.<java.lang.IllegalArgumentException: void <init>(java.lang.String)>("Division by zero is not allowed");
    
        throw $stack4;
    
      label1:
        $stack3 = a / b;
    
        return $stack3;
    }
    """

    output_for_divide = generate_test_for_prompt_template(fqn, signature, jimple_code)
    print(output_for_divide)
