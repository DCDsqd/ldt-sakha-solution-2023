package com.example.demo.controllers;

import jakarta.servlet.http.HttpSession;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {

    @GetMapping("/")
    public String mainPage(Model model, @AuthenticationPrincipal OAuth2User principal){
        final boolean isLogin = !(principal == null || ("anonymousUser").equals(principal.getName()));
        model.addAttribute("isLogin", isLogin);

        return "main";
    }
}
