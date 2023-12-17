package com.example.demo.controllers;

import com.example.demo.entitys.Predict;
import com.example.demo.services.ApiRequestService;
import com.example.demo.services.CourseService;
import com.fasterxml.jackson.core.JsonProcessingException;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.Map;

@RestController
public class WebController {
    private final ApiRequestService apiRequestService;
    private final CourseService courseService;

    @Autowired
    public WebController(ApiRequestService apiRequestService, CourseService courseService) {
        this.apiRequestService = apiRequestService;
        this.courseService = courseService;
    }


    @RequestMapping("/user")
    public Map<String, Object> user(HttpSession httpSession, @AuthenticationPrincipal OAuth2User principal) {

        return Collections.singletonMap("name", principal.getAttributes());
    }

    @RequestMapping("/secret")
    public String secret() {
        return "protected data";
    }

    @RequestMapping("/oauth2/callback/vk")
    public String callback(HttpSession httpSession, @AuthenticationPrincipal OAuth2User principal) {
        System.out.println("vk");
        return "hello";
    }

    @RequestMapping("/test")
    public String test(@AuthenticationPrincipal OAuth2User principal) throws JsonProcessingException {
        Predict data = apiRequestService.sendTestRequest();
        String answer = data.getTopProfessions().toString();
        if(answer == null)
            return "server error";

        return answer;
    }

    @RequestMapping("/createdb")
    public String create(){
        courseService.fillDb();
        return "complete";
    }
}
