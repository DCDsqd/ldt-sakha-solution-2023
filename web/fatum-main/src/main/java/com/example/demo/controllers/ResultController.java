package com.example.demo.controllers;

import com.example.demo.entitys.Course;
import com.example.demo.entitys.Predict;
import com.example.demo.services.ApiRequestService;
import com.example.demo.services.CourseService;
import com.example.demo.services.MyUserService;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import java.util.List;
import java.util.Map;

@Controller
public class ResultController {

    private final ApiRequestService apiRequestService;
    private final CourseService courseService;
    private final MyUserService myUserService;

    @Autowired
    public ResultController(ApiRequestService apiRequestService,
                            CourseService courseService,
                            MyUserService myUserService) {
        this.apiRequestService = apiRequestService;
        this.courseService = courseService;
        this.myUserService = myUserService;
    }


    @RequestMapping(value = "/result", method = RequestMethod.GET)
    public String result(Model model, @AuthenticationPrincipal OAuth2User principal) throws JsonProcessingException {
        final boolean isLogin = !(principal == null || ("anonymousUser").equals(principal.getName()));
        model.addAttribute("isLogin", isLogin);

        if(!isLogin){
            return "main";
        }

        Predict data = apiRequestService.sendUserRequest(principal);
        List<Course> courses = courseService.findAllByName(data.getProfession());
        List<Map<String, Double>> pairs = apiRequestService.getPairs(data.getTopProbabilities(), data.getTopProfessions());

        model.addAttribute("predict", data);
        model.addAttribute("courses_list", courses);
        model.addAttribute("prof_list", pairs);

        System.out.println(pairs);
        myUserService.addProfession(principal, data.getProfession());
        return "result";
    }
}
