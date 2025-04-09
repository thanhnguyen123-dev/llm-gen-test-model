package org.example;

public class CheckPassing {
    public boolean checkPassing(int score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("Score must be between 0 and 100");
        }
        return score >= 50;
    }
}
