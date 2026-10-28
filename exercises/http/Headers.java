import java.util.HashMap;
import java.util.Map;

public class Headers {
    public Map<String, String> values;

    public Headers() {
        this.values = new HashMap<>();
    }

    public Headers(Map<String, String> values) {
        this.values = values != null ? new HashMap<>(values) : new HashMap<>();
    }

    public static Headers of(Map<String, String> values) {
        return new Headers(values);
    }

    public void add(String key, String value) {
        values.put(key, value);
    }

    public String get(String key) {
        return values.get(key);
    }
}
