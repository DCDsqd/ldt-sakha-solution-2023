package com.example.demo.entitys;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class YtChannel {
    String name;
    String id;

    public YtChannel(String name, String id){
        this.name = name;
        this.id = id;
    }
}
