public class Main {
    public static void main(String[] args) {
        // Method, URL and follow redirects are required for all requests

        // Request 1: GET with API Key authentication (no Headers)
        AuthConfig auth1 = new ApiKeyAuth("my-secret-api-key-12345");
        HttpRequest request1 = new HttpRequest("GET", "https://api.com/users", true, null, auth1);
        HttpResponse response1 = request1.send();
        // Request 2: POST with OAuth authentication, Header, and Body
        Headers headers = new Headers();
        headers.add("Content-Type", "application/json");
        AuthConfig auth2 = new OAuthAuth("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9");
        HttpRequest request2 = new HttpRequest("POST", "https://api.com/data", false, headers, auth2);
        request2.setBody("{\"name\": \"John Doe\", \"email\": \"john@example.com\"}");
        HttpResponse response2 = request2.send();

        // Request 3: GET without authentication, redirects, body, or headers
        HttpRequest request3 = new HttpRequest("GET", "https://api.com/public", false, null, null);
        HttpResponse response3 = request3.send();
    }
}
