public class HttpRequest {
    private String method;
    private String url;
    private boolean followRedirects;
    private int timeoutSec;
    private Headers headers;
    private AuthConfig auth;
    private String body;

    public HttpRequest(String method, String url, boolean followRedirects,
                       Headers headers, AuthConfig auth) {
        this.method = method;
        this.url = url;
        this.followRedirects = followRedirects;
        this.timeoutSec = 30;
        this.headers = headers;
        this.auth = auth;
    }

    public HttpRequest(String method, String url, boolean followRedirects,
                       int timeoutSec, Headers headers, AuthConfig auth, String body) {
        this.method = method;
        this.url = url;
        this.followRedirects = followRedirects;
        this.timeoutSec = timeoutSec;
        this.headers = headers;
        this.auth = auth;
        this.body = body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public HttpResponse send() {
        // Stub: no real HTTP — just acknowledge the request was "sent"
        return new HttpResponse(200, "OK");
    }
}
