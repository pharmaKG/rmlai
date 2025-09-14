import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.util.*;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.json.JSONArray;
import java.math.BigDecimal;
import java.util.Collections;

public class RmlCustomFunctions {
    public static String generateUUID() {
        return UUID.randomUUID().toString() ;
    }

    public static List<String> getListFromLLM(String prompt, String model) {
        String marker = "text:";
        String content = prompt.substring(prompt.indexOf(marker) + marker.length()).strip();
        if (content == null || content.equals("null") || content.equalsIgnoreCase("adult") || content.equalsIgnoreCase("child") || content.equalsIgnoreCase("neonate") || content.equalsIgnoreCase("")) return null;

        String output = getStrFromLLM("query_llama.py", prompt, model, "list");

        if (output == null || output.strip().equals("")) return null;

        JSONArray jsonArray = new JSONArray(output);
        List<String> resultList = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++) {
            resultList.add(jsonArray.getString(i));
        }

        return resultList;
    }

    public static BigDecimal getFloatFromLLM(String prompt, String model) {
        String marker = "text:";
        String content = prompt.substring(prompt.indexOf(marker) + marker.length()).strip();
        if (content == null || content.equals("null") || content.equalsIgnoreCase("adult") || content.equalsIgnoreCase("child") || content.equalsIgnoreCase("neonate") || content.equalsIgnoreCase("")) return null;

        String output = getStrFromLLM("query_llama.py", prompt, model, "float");

        if (output == null || output.strip().equals("")) return null;

        return new BigDecimal(output.strip());
    }

    public static String getStrFromLLM(String prompt, String model) {
        String marker = "text:";
        String content = prompt.substring(prompt.indexOf(marker) + marker.length()).strip();
        if (content == null || content.equals("null") || content.equalsIgnoreCase("adult") || content.equalsIgnoreCase("child") || content.equalsIgnoreCase("neonate") || content.equalsIgnoreCase("")) return null;

        String output = getStrFromLLM("query_llama.py", prompt, model, "str");
        if (output == null || output.strip().equals(""))
            return null;
        else return output;
    }

    public static String getStrFromLLM(String pyFileName, String prompt, String model, String returnType) {
        StringBuilder result = new StringBuilder();
        try {
            ProcessBuilder pb = new ProcessBuilder(
                    "python",
                    pyFileName,
                    "--return_type",
                    returnType,
                    "--prompt",
                    prompt,
                    "--model",
                    model
            );
            Process process = pb.start();

            // Read the output of the Python process
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                result.append(line);
            }

            // Wait for the Python process to finish
            int exitCode = process.waitFor();
            String promptInstruction = prompt.substring(0, prompt.indexOf("\n"));
            System.out.println("Python script exited with code: " + exitCode + " for promptInstruction: " + promptInstruction);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result.toString();
    }

    public static String concat(String valueParam, String valueParam2) {
        return valueParam + " " + valueParam2 ;
    }

    public static String concat(List<String> list, String valueParam) {
        return list.stream().collect(Collectors.joining(" ")) + " " + valueParam ;
    }

    public static List<String> getRoute(String value) {
        if (value.contains(",")) {
            return Arrays.asList(value.split(",")).stream().map(v -> v.toLowerCase()).collect(Collectors.toList());
        }
        value = value.toLowerCase();
        return Collections.singletonList(value);
    }
}
