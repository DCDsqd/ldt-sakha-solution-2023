package com.example.demo.security;

import com.example.demo.services.MyUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.client.oidc.userinfo.OidcUserRequest;
import org.springframework.security.oauth2.client.oidc.userinfo.OidcUserService;
import org.springframework.security.oauth2.core.OAuth2AccessToken;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

@Service("customOidcUserService")
public class CustomOidcUserService extends OidcUserService {

    private final MyUserService myUserService;

    @Autowired
    public CustomOidcUserService(MyUserService myUserService) {
        this.myUserService = myUserService;
    }

    @Override
    public OidcUser loadUser(OidcUserRequest userRequest) throws OAuth2AuthenticationException {
        OidcUser user = super.loadUser(userRequest);
        userRequest.getClientRegistration().getRegistrationId().equals("google");
//        System.out.println("User service");
//        System.out.println(user.getEmail());
        multiPrincipal(user, userRequest.getAccessToken());

        return user;
    }

    private void multiPrincipal(OidcUser user, OAuth2AccessToken token){
        SecurityContext context = SecurityContextHolder.getContext();
        Authentication authentication = context.getAuthentication();
        if(authentication == null){
            myUserService.oauth2MyUserGoogle(user, token);
            return;
        }
        System.out.println(((DefaultOAuth2User)authentication.getPrincipal()).getAttributes());
        myUserService.connectGoogleAccount((DefaultOAuth2User) authentication.getPrincipal(), user, token);
    }


}
