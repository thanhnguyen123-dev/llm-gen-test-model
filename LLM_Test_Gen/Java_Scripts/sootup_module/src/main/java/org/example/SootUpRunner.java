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

import java.io.FileWriter;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class SootUpRunner {
    private static final String TEST_DATA_RELATIVE_PATH = "../../Data/Test_Data.csv";
    private static final String CSV_DELIMITER = ",";
    private static final String CSV_HEADER = "\"FQN\",\"Signature\",\"Jimple Code Representation\"";

    public static void main(String[] args) {
        String targetClassesPathToLang1Buggy = "../../../lang_1_buggy/target/classes";
        String targetClasses = "target/classes";

        Path moduleBasePath = Paths.get(".").toAbsolutePath().normalize();
        Path outputCsvAbsPath = moduleBasePath.resolve(TEST_DATA_RELATIVE_PATH).normalize();

        // Point SootUp to the compiled classes
        AnalysisInputLocation<JavaSootClass> inputLocation =
                new JavaClassPathAnalysisInputLocation(targetClassesPathToLang1Buggy);

        // Build the project (using Java 8 here)
        JavaLanguage language = new JavaLanguage(8);
        Project project = JavaProject.builder(language)
                .addInputLocation(inputLocation)
                .build();

        // Create a View for reading class/method data
        View view = project.createView();

        // Retrieve all classes discovered by SootUp
        Collection<SootClass<JavaSootClassSource>> allClasses = view.getClasses();

        // Define the targeted classes
        Set<String> targetClassesNames = Set.of(
            "org.apache.commons.lang3.CharRange",
            "org.apache.commons.lang3.CharSetUtils",
            "org.apache.commons.lang3.text.WordUtils"
        );


        // Iterate over each class

        try (PrintWriter writer = new PrintWriter(new FileWriter(outputCsvAbsPath.toString())))  {
            writer.println(CSV_HEADER);

            for (SootClass<JavaSootClassSource> sootClass : allClasses) {
                String fullClassName = sootClass.getName();

                // If this is the runner class or the methods isn't from CharRange, CharSetUtils, or WordUtils, skip it
                if (fullClassName.equals("org.example.SootUpRunner") || !targetClassesNames.contains(fullClassName)) {
                    continue;
                }

                // Iterate over each method in the class
                for (SootMethod method : sootClass.getMethods()) {
                    // Only proceed if the method is concrete
                    if (!method.isConcrete() || method.getName().equals("<init>") || method.getName().equals("<clinit>") || method.getName().startsWith("access$")) {
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

                    String quotedFqn = quoteField(fqnStringBuilder.toString());
                    String quotedSignature = quoteField(signatureStringBuilder.toString());
                    String quotedJimpleCode = quoteField(jimpleCode);

                    String csvLine = String.join(CSV_DELIMITER, quotedFqn, quotedSignature, quotedJimpleCode);
                    writer.println(csvLine);

                    // Print the information
                    System.out.println("-----------------------------------------------------------------");
                    System.out.println("CODE INFORMATION:\n");
                    System.out.println("- FQN: " + fqnStringBuilder);
                    System.out.println("- Signature: " + signatureStringBuilder);
                    System.out.println("- Jimple Code:\n" + jimpleCode);
                    System.out.println("-----------------------------------------------------------------");
                }
            }
        } catch (Exception e) {
            System.err.println("An error occurred while processing the classes: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static String quoteField(String data) {
        if (data == null) {
            return "\"\"";
        }
        String escapedData = data.replace("\"", "\"\"");
        return "\"" + escapedData + "\"";
    }
}
