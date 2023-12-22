package com.example.demo.services;

import com.example.demo.entitys.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.minidev.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service("apiRequestService")
public class ApiRequestService {
    @Value("${spring.fatum.api.url}")
    String url;

    private RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    private final MyUserService myUserService;

    @Autowired
    public ApiRequestService(MyUserService myUserService){
        this.myUserService = myUserService;
        objectMapper = new ObjectMapper();
    }

    public Predict sendNullRequest(){

        return new Predict();
    }

    public Predict sendTestRequest() throws JsonProcessingException {
        List<String> topProfessions = new ArrayList<>();
        List<Double> tmp0 = new ArrayList<>();
        topProfessions.add("Бизнес-аналитик");
        topProfessions.add("Маркетолог");
        topProfessions.add("Менеджер по продажам");

        tmp0.add(0.43177417315906574);
        tmp0.add(0.3685113924098826);
        tmp0.add(0.1234701364854289);

        YtLike video;
        List<YtLike> ytImpactfulLikes = new ArrayList<>();
        video = new YtLike("✅ Что такое ERP-система? Система управления предприятием", "G2Hbi9FtDxw");
        ytImpactfulLikes.add(video);
        video = new YtLike("10 ошибок руководителя / Менеджмент и управление персоналом", "y_XA-JXCxx4");
        ytImpactfulLikes.add(video);
        video = new YtLike("Оргсхема в современном бизнесе. Основы организационной структуры предприятия простыми словами", "e0c15ypw-Rg");
        ytImpactfulLikes.add(video);
        video = new YtLike("А.М.Рощин. Курс \"Основы менеджмента\". Первая лекция", "ixKCwQan810");
        ytImpactfulLikes.add(video);

        YtChannel channel;
        List<YtChannel> ytImpactfulChannels = new ArrayList<>();
        channel = new YtChannel("ITViar", "UC79Qh_C7hOgd_cYJOL82DWw");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("амоБлог", "UC03-38aILdlkFAAc8lE6MQg");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("ЮЛИЯ ТРУС ПРО БИЗНЕС", "UCgVJE-ez4bCEj8ILrM7g5sQ");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("СНИТКО", "UC-t7InyZm_DrmQZtnBMa00g");
        ytImpactfulChannels.add(channel);

        VkImpactfulGroup group;
        List<VkImpactfulGroup> vkImpactfulGroups = new ArrayList<>();
        group = new VkImpactfulGroup("Бизнес-школа МФТИ", "204334252");
        vkImpactfulGroups.add(group);
        group = new VkImpactfulGroup("Максим Чирков | Бизнес Блог", "87335115");
        vkImpactfulGroups.add(group);
        group = new VkImpactfulGroup("ЭКВИУМ | Бизнес-сообщество", "211200230");
        vkImpactfulGroups.add(group);


        List<Integer> topProbabilities = new ArrayList<>();
        List<String> colors = new ArrayList<>();
        String profession = "";

        Predict predict = new Predict();

        if(tmp0.size() > 0) {
            double max = tmp0.get(0);
            int index = 0;
            for (int i = 0; i < tmp0.size(); i++) {
                topProbabilities.add((int) (tmp0.get(i)*1000));
                //rgba(245, 37, 158, 0.9)
                int pram = (int)(tmp0.get(i)*2550);
                System.out.println(pram);
                colors.add(String.format("rgba(%d, %d, %d, 0.5)", pram, (int)(255-(pram*0.8)), (int)(pram/2)));

                if (tmp0.get(i) > max) {
                    max = tmp0.get(i);
                    index = i;
                }
            }
            profession = topProfessions.get(index);
        }

        predict.setTopProbabilities(topProbabilities);
        predict.setTopProfessions(topProfessions);
        predict.setColors(colors);
        predict.setYtImpactfulLikes(ytImpactfulLikes);
        predict.setYtImpactfulChannels(ytImpactfulChannels);
        predict.setVkImpactfulGroups(vkImpactfulGroups);
        predict.setProfession(profession);

        if( !(profession.isEmpty() || profession.isBlank()) )
            predict.setIsValid(true);

        return predict;
    }

    public Predict sendUserRequest(OAuth2User user) throws JsonProcessingException {
        MyUser myUser = myUserService.getUserById(user);
        System.out.println(myUser.toString());

        return sendRequest("", myUser.getGoogleToken(), "", "", "");
    }

    public List<Map<String, Double>> getPairs(List<Integer> prob, List<String> professions){
        List<Map<String, Double>> list = new ArrayList<>();
        for(int i = 0; i < professions.size(); ++i){
            Map<String, Double> tmp = new HashMap<>();
            tmp.put(professions.get(i), ((double)prob.get(i))/1000.0);
            list.add(tmp);
        }
        return list;
    }

    private Predict Json2PRedict(JsonNode root){
        Predict predict = new Predict();
        List<String> topProfessions = objectMapper.convertValue(root.get("top_professions"), List.class);
        List<Double> tmp0 = objectMapper.convertValue(root.get("top_probabilities"), List.class);
        List<Map<String, String>> preYtImpactfulLikes = objectMapper.convertValue(root.get("yt_impactful_likes"), List.class);
        List<Map<String, String>> preYtImpactfulChannels = objectMapper.convertValue(root.get("yt_impactful_channels"), List.class);
        List<YtLike> ytImpactfulLikes = new ArrayList<>();
        List<YtChannel> ytImpactfulChannels = new ArrayList<>();
        List<Integer> topProbabilities = new ArrayList<>();
        List<String> colors = new ArrayList<>();
        String profession = "";

        if(preYtImpactfulLikes != null)
            for(int i = 0; i < preYtImpactfulLikes.size(); ++i){
                ytImpactfulLikes.add(new YtLike(preYtImpactfulLikes.get(i).get("name"), preYtImpactfulLikes.get(i).get("id")));
            }
        if(preYtImpactfulChannels != null)
            for(int i = 0; i < preYtImpactfulChannels.size(); ++i){
                ytImpactfulChannels.add(new YtChannel(preYtImpactfulChannels.get(i).get("name"), preYtImpactfulChannels.get(i).get("id")));
            }

        System.out.println(root);
        System.out.println(ytImpactfulLikes);
        System.out.println(ytImpactfulChannels);

        if(tmp0.size() > 0) {
            double max = tmp0.get(0);
            int index = 0;
            for (int i = 0; i < tmp0.size(); i++) {
                topProbabilities.add((int) (tmp0.get(i)*1000));
                //rgba(245, 37, 158, 0.9)
                int pram = (int)(tmp0.get(i)*2550);
                System.out.println(pram);
                colors.add(String.format("rgba(%d, %d, %d, 0.5)", pram, (int)(255-(pram*0.8)), (int)(pram/2)));

                if (tmp0.get(i) > max) {
                    max = tmp0.get(i);
                    index = i;
                }
            }
            profession = topProfessions.get(index);
        }

        predict.setColors(colors);
        predict.setYtImpactfulChannels(ytImpactfulChannels);
        predict.setYtImpactfulLikes(ytImpactfulLikes);
        predict.setTopProfessions(topProfessions);
        predict.setTopProbabilities(topProbabilities);
        predict.setProfession(profession);

        if( !(profession.isEmpty() || profession.isBlank()) )
            predict.setIsValid(true);

        return predict;
    }

    private Predict sendRequest(String debugText, String ytToken, String vkToken, String tgToken, String tgPost) throws JsonProcessingException {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        JSONObject personJsonObject = new JSONObject();

        personJsonObject.put("yt_token", ytToken);
        personJsonObject.put("vk_token", vkToken);
        personJsonObject.put("tg_token", tgToken);
        String[] tg = {};
        personJsonObject.put("tg_posts", tg);

        HttpEntity<String> request =
                new HttpEntity<String>(personJsonObject.toString(), headers);
        String personResultAsJsonStr =
                restTemplate.postForObject(url, request, String.class);
        JsonNode root = objectMapper.readTree(personResultAsJsonStr);

        System.out.println(root);

        return Json2PRedict(root);
    }
}
