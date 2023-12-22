package com.example.demo.controllers;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.HashMap;
import java.util.Map;

@Controller
public class LoginController {
    private static final String authorizationRequestBaseUri = "oauth2/authorization";
    Map<String, String> oauth2AuthenticationUrls = new HashMap<>();

    public LoginController() {
    }

    @RequestMapping(value = {"/exit"}, method = RequestMethod.GET)
    public String fetchSignoutSite(HttpServletRequest request, HttpServletResponse response){

        HttpSession session = request.getSession(false);
        SecurityContextHolder.clearContext();

        session = request.getSession(false);
        if(session != null) {
            session.invalidate();
        }

        for(Cookie cookie : request.getCookies()) {
            cookie.setMaxAge(0);
        }

        return "redirect:/login";
    }

    @RequestMapping(value = "/login", method = RequestMethod.GET)
    public String getLoginPage(Model model, @AuthenticationPrincipal OAuth2User principal) {
        final boolean isLogin = !(principal == null || ("anonymousUser").equals(principal.getName()));
        model.addAttribute("isLogin", isLogin);
        if(isLogin)
            return "redirect:/";
        return "login";
    }


    @GetMapping("/policy")
    public String getPolicyPage(){
        return "policyPage";
    }

}