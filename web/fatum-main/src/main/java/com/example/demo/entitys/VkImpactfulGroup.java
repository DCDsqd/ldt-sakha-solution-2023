package com.example.demo.entitys;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class VkImpactfulGroup {
    private String name;
    private String id;

    public VkImpactfulGroup(String name, String id){
        this.name = name;
        this.id = id;
    }
}
