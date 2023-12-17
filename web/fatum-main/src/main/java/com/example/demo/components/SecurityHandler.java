package com.example.demo.components;


import com.example.demo.services.MyUserService;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class SecurityHandler extends SimpleUrlAuthenticationSuccessHandler {

    public SecurityHandler() {
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException {
        //myUserService.updateUser2Full((DefaultOAuth2User) authentication.getPrincipal(), response);
        super.onAuthenticationSuccess(request, response, authentication);
    }
}
