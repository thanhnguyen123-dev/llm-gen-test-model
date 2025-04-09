package org.example;

import sootup.core.Project;
import sootup.core.inputlocation.AnalysisInputLocation;
import sootup.core.model.SootMethod;
import sootup.core.model.SootClass;
import sootup.core.views.View;
import sootup.java.bytecode.inputlocation.JavaClassPathAnalysisInputLocation;
import sootup.java.core.JavaProject;
import sootup.java.core.JavaSootClass;
import sootup.java.core.JavaSootClassSource;
import sootup.java.core.language.JavaLanguage;
import sootup.core.types.Type;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class SootUpRunner {
    public static void main(String[] args) {
        // Point SootUp to the compiled classes
        AnalysisInputLocation<JavaSootClass> inputLocation =
                new JavaClassPathAnalysisInputLocation("target/classes");

        // Build the project (using Java 8 here)
        JavaLanguage language = new JavaLanguage(8);
        Project project = JavaProject.builder(language)
                .addInputLocation(inputLocation)
                .build();

        // Create a View for reading class/method data
        View view = project.createView();

        // Retrieve all classes discovered by SootUp
        Collection<SootClass<JavaSootClassSource>> allClasses = view.getClasses();


        // Iterate over each class
        for (SootClass<JavaSootClassSource> sootClass : allClasses) {
            String fullClassName = sootClass.getName();

            // If this is the runner class, skip it
            if (fullClassName.equals("org.example.SootUpRunner")) {
                continue;
            }

            // Iterate over each method in the class
            for (SootMethod method : sootClass.getMethods()) {
                // Only proceed if the method is concrete
                if (!method.isConcrete() || method.getName().equals("<init>") || method.getName().equals("<clinit>")) {
                    continue;
                }

                // Extract method name, parameter types, and return type
                String methodName = method.getName();
                List<Type> paramTypes = method.getParameterTypes();
                Type returnType = method.getReturnType();

                String paramListString = paramTypes.stream()
                        .map(Type::toString)
                        .collect(Collectors.joining(", "));

                StringBuilder fqnStringBuilder = new StringBuilder();
                StringBuilder signatureStringBuilder = new StringBuilder();

                // Construct the FQN
                fqnStringBuilder
                        .append(fullClassName)
                        .append(".")
                        .append(methodName)
                        .append("(")
                        .append(paramListString)
                        .append(")");

                // Construct the signature
                signatureStringBuilder
                        .append(returnType)
                        .append(" ")
                        .append(methodName)
                        .append("(")
                        .append(paramListString)
                        .append(")");

                // Retrieve the Jimple code
                String jimpleCode = method.getBody().toString();

                // Print the information
                System.out.println("-----------------------------------------------------------------");
                System.out.println("CODE INFORMATION:\n");
                System.out.println("- FQN: " + fqnStringBuilder);
                System.out.println("- Signature: " + signatureStringBuilder);
                System.out.println("- Jimple Code:\n" + jimpleCode);
                System.out.println("-----------------------------------------------------------------");
            }
        }
    }
}
