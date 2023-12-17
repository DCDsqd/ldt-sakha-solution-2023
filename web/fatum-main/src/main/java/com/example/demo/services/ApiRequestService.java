package com.example.demo.services;

import com.example.demo.entitys.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import net.minidev.json.JSONObject;
import org.antlr.v4.runtime.misc.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.lang.reflect.Array;
import java.util.*;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@Service
public class ApiRequestService {
    @Value("${fatum.api.url}")
    String url;

    private RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    private final MyUserService myUserService;

    @Autowired
    public ApiRequestService(MyUserService myUserService){
        this.myUserService = myUserService;
        objectMapper = new ObjectMapper();
    }

    public Predict sendTestRequest() throws JsonProcessingException {
        List<String> topProfessions = new ArrayList<>();
        List<Double> tmp0 = new ArrayList<>();
        topProfessions.add("Гейм-дизайнер");
        topProfessions.add("Астроном");
        topProfessions.add("Кинооператор");
        tmp0.add(0.043177417315906574);
        tmp0.add(0.02185113924098826);
        tmp0.add(0.01634701364854289);

        YtLike video;
        List<YtLike> ytImpactfulLikes = new ArrayList<>();
        video = new YtLike("[RU/ENG] Siberian Game Jam - Itch.io Day #55", "bMLTdSgW7ew");
        ytImpactfulLikes.add(video);
        video = new YtLike("The Last Night Gameplay Footage from E3 2017 PC Gaming show", "6GsZG1t3v-Y");
        ytImpactfulLikes.add(video);
        video = new YtLike("SIREN. Великий хоррор, прошедший незаметно [Страшно, вырубай!]", "w29y5cXjkH4");
        ytImpactfulLikes.add(video);
        video = new YtLike("КУОК – CORRIDA (Music Video)", "HablFXGUZq4");
        ytImpactfulLikes.add(video);

        YtChannel channel;
        List<YtChannel> ytImpactfulChannels = new ArrayList<>();
        channel = new YtChannel("Meeponegeroi", "UCvbHR1AuYOnJTAO2SJGVDgA");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("БУЛДЖАТь", "UCOxQWb-OuyCSZadzWqrKTCQ");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("Obsidian Time", "UCNV-mYw3hlPc9D6EmaStw2w");
        ytImpactfulChannels.add(channel);
        channel = new YtChannel("Utopia Show", "UC8M5YVWQan_3Elm-URehz9w");
        ytImpactfulChannels.add(channel);

        VkImpactfulGroup group;
        List<VkImpactfulGroup> vkImpactfulGroups = new ArrayList<>();
        group = new VkImpactfulGroup("!internet!", "108531402");
        vkImpactfulGroups.add(group);
        group = new VkImpactfulGroup("kind of death", "206434816");
        vkImpactfulGroups.add(group);
        group = new VkImpactfulGroup("DTF", "22781583");
        vkImpactfulGroups.add(group);


        List<Integer> topProbabilities = new ArrayList<>();
        List<String> colors = new ArrayList<>();

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
            predict.setProfession(topProfessions.get(index));
        }

        predict.setTopProbabilities(topProbabilities);
        predict.setTopProfessions(topProfessions);
        predict.setColors(colors);
        predict.setYtImpactfulLikes(ytImpactfulLikes);
        predict.setYtImpactfulChannels(ytImpactfulChannels);
        predict.setVkImpactfulGroups(vkImpactfulGroups);

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

        for(int i = 0; i < preYtImpactfulLikes.size(); ++i){
            ytImpactfulLikes.add(new YtLike(preYtImpactfulLikes.get(i).get("name"), preYtImpactfulLikes.get(i).get("id")));
        }
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
            predict.setProfession(topProfessions.get(index));
        }

        predict.setColors(colors);
        predict.setYtImpactfulChannels(ytImpactfulChannels);
        predict.setYtImpactfulLikes(ytImpactfulLikes);
        predict.setTopProfessions(topProfessions);
        predict.setTopProbabilities(topProbabilities);

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
