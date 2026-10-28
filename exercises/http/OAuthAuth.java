public class OAuthAuth extends AuthConfig {
    private final String token;

    public OAuthAuth(String token) {
        this.token = token;
    }

    public String getToken() {
        return token;
    }
}
