package com.example.demo.entitys;


import lombok.Getter;
import lombok.Setter;
import org.springframework.data.util.Pair;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Getter
@Setter
public class Predict implements Serializable {
    List<String> topProfessions = new ArrayList<>();
    List<Integer> topProbabilities = new ArrayList<>();
    String profession = "";
    List<String> colors = new ArrayList<>();
    List<YtLike> ytImpactfulLikes = new ArrayList<>();
    List<YtChannel> ytImpactfulChannels = new ArrayList<>();
    List<Map<String, String>> vkImpactfulLikes = new ArrayList<>();
    List<VkImpactfulGroup> vkImpactfulGroups = new ArrayList<>();
}
