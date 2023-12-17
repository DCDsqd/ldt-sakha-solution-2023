package com.example.demo.controllers;

import com.example.demo.entitys.MyUser;
import com.example.demo.services.MyUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AccountController {
    private final MyUserService myUserService;

    @Autowired
    public AccountController(MyUserService myUserService) {
        this.myUserService = myUserService;
    }

    @GetMapping("/account")
    public String mainPage(Model model, @AuthenticationPrincipal OAuth2User principal){
        final boolean isLogin = !(principal == null || ("anonymousUser").equals(principal.getName()));
        MyUser myUser = new MyUser();
        model.addAttribute("isLogin", isLogin);

        if(isLogin) {
            myUser = myUserService.getUserById(principal);
        }
        model.addAttribute("user", myUser);

        return "account";
    }

}
