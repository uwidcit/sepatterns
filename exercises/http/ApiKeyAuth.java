public class ApiKeyAuth extends AuthConfig {
    private final String apiKey;

    public ApiKeyAuth(String apiKey) {
        this.apiKey = apiKey;
    }

    public String getApiKey() {
        return apiKey;
    }
}
