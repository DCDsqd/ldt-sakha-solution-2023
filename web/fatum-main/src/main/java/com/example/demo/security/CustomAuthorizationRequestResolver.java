package com.example.demo.security;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.oauth2.client.web.DefaultOAuth2AuthorizationRequestResolver;
import org.springframework.security.oauth2.client.web.OAuth2AuthorizationRequestResolver;
import org.springframework.security.oauth2.core.endpoint.OAuth2AuthorizationRequest;

import java.util.HashMap;
import java.util.Map;

public class CustomAuthorizationRequestResolver
        implements OAuth2AuthorizationRequestResolver {

    private OAuth2AuthorizationRequestResolver defaultResolver;

    public CustomAuthorizationRequestResolver(
            ClientRegistrationRepository repo, String authorizationRequestBaseUri) {
        defaultResolver = new DefaultOAuth2AuthorizationRequestResolver(repo, authorizationRequestBaseUri);
    }

    @Override
    public OAuth2AuthorizationRequest resolve(HttpServletRequest request) {
        OAuth2AuthorizationRequest req = defaultResolver.resolve(request);
        //System.out.println(req);
        if(req != null) {
            req = customizeAuthorizationRequest(req);
        }
        return req;
    }

    @Override
    public OAuth2AuthorizationRequest resolve(HttpServletRequest request, String clientRegistrationId) {
        OAuth2AuthorizationRequest req = defaultResolver.resolve(request, clientRegistrationId);
        //System.out.println(req);
        if(req != null) {
            req = customizeAuthorizationRequest(req);
        }
        return req;
    }

    private OAuth2AuthorizationRequest customizeAuthorizationRequest(
            OAuth2AuthorizationRequest req) {
//        System.out.println("Resolver enter");
//        System.out.println(req.getAttributes());
//        System.out.println(req.getRedirectUri());

        Map<String,Object> extraParams = new HashMap<String,Object>();
        extraParams.putAll(req.getAdditionalParameters());

        if(req.getAttributes().get("registration_id").equals("vk"))
            return vkAuthorizationRequest(req, extraParams);

        return OAuth2AuthorizationRequest
                .from(req)
                .additionalParameters(extraParams)
                .build();
    }

    private OAuth2AuthorizationRequest vkAuthorizationRequest(
            OAuth2AuthorizationRequest req, Map<String, Object> extraParams) {
//        extraParams.put("client_id", req.getClientId());
//        extraParams.put("redirect_uri", req.getRedirectUri());
//        extraParams.put("scope", "friends");
//        System.out.println(extraParams);

        return OAuth2AuthorizationRequest
                .from(req)
                .additionalParameters(extraParams)
                .build();
    }

}
