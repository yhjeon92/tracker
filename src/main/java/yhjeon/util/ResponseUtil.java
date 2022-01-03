package yhjeon.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ResponseUtil {
    public static String convertToJson(Object object) {
        ObjectMapper mapper = new ObjectMapper();
        String jsonString = "";
        try {
            jsonString = mapper.writeValueAsString(object);
        } catch (JsonProcessingException exception) {
            System.out.println(exception.getMessage());
        }

        return jsonString;
    }
}
