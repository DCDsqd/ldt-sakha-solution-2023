package com.example.demo.security;

import org.springframework.security.oauth2.client.registration.ClientRegistration;
import org.springframework.security.oauth2.core.AuthorizationGrantType;
import org.springframework.security.oauth2.core.ClientAuthenticationMethod;
import org.springframework.security.oauth2.core.oidc.IdTokenClaimNames;

import java.util.HashMap;
import java.util.Map;

public enum CustomRegistrationProvider {
    GOOGLE {
        public ClientRegistration.Builder getBuilder(String registrationId) {
            ClientRegistration.Builder builder = this.getBuilder(registrationId, ClientAuthenticationMethod.CLIENT_SECRET_BASIC, DEFAULT_REDIRECT_URL);
            builder.scope(new String[]{"openid", "profile", "email", "https://www.googleapis.com/auth/youtube.readonly"});
            builder.authorizationUri("https://accounts.google.com/o/oauth2/v2/auth");
            builder.tokenUri("https://www.googleapis.com/oauth2/v4/token");
            builder.jwkSetUri("https://www.googleapis.com/oauth2/v3/certs");
            builder.issuerUri("https://accounts.google.com");
            builder.userInfoUri("https://www.googleapis.com/oauth2/v3/userinfo");
            builder.userNameAttributeName("sub");
            builder.clientName("Google");
            return builder;
        }
    },
    VK {
        public ClientRegistration.Builder getBuilder(String registrationId) {
            ClientRegistration.Builder builder = getBuilder("vk", ClientAuthenticationMethod.CLIENT_SECRET_POST, DEFAULT_REDIRECT_URL);
            builder.scope("email");
            builder.authorizationUri("https://oauth.vk.com/authorize?v=5.131");
            builder.tokenUri("https://oauth.vk.com/access_token");
            builder.userInfoUri("https://api.vk.com/method/users.get?v=5.131");
            builder.clientName("vkontakte");
            builder.userNameAttributeName("id");
            builder.authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE);
            builder.registrationId("vk");
            return builder;
        }
    };


    private static final String DEFAULT_REDIRECT_URL = "{baseUrl}/{action}/oauth2/code/{registrationId}";
    private static final String CALLBACK_REDIRECT_URL = "{baseUrl}/{action}/oauth2/callback/{registrationId}";

    private CustomRegistrationProvider() {
    }

    protected final ClientRegistration.Builder getBuilder(String registrationId, ClientAuthenticationMethod method, String redirectUri) {
        ClientRegistration.Builder builder = ClientRegistration.withRegistrationId(registrationId);
        builder.clientAuthenticationMethod(method);
        builder.authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE);
        builder.redirectUri(redirectUri);
        return builder;
    }

    public abstract ClientRegistration.Builder getBuilder(String registrationId);
}
