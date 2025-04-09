from openai_service import generate_test_for_prompt_template

if __name__ == "__main__":
    # test for checkPassing
    fqn = "org.example.CheckPassing.checkPassing(int)"
    signature = "boolean checkPassing(int)"
    jimple_code = """
    {
        int score;
        org.example.CheckPassing this;
        unknown $stack2, $stack3, $stack4;
    
    
        this := @this: org.example.CheckPassing;
        score := @parameter0: int;
    
        if score < 0 goto label1;
    
        if score <= 100 goto label2;
    
      label1:
        $stack2 = new java.lang.IllegalArgumentException;
        $stack4 = "Score must be between 0 and 100";
        specialinvoke $stack2.<java.lang.IllegalArgumentException: void <init>(java.lang.String)>($stack4);
    
        throw $stack2;
    
      label2:
        if score < 50 goto label3;
        $stack3 = 1;
    
        goto label4;
    
      label3:
        $stack3 = 0;
    
      label4:
        return $stack3;
    }
    """

    output_for_checkPassing = generate_test_for_prompt_template(fqn, signature, jimple_code)
    print(output_for_checkPassing)