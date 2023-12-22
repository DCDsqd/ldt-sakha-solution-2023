package com.example.demo.entitys;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "UsersAccounts")
public class MyUser {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String mail;
    private String lastName;
    private String firstName;
    private String vkId;
    private String token;
    private String googleToken;
    private String googleId;
    private String lastProfession;

    @Override
    public String toString(){
        return (id.toString() + ","+firstName+","+lastName);
    }

    public boolean vkLogin(){
        return firstName != null && lastName != null && vkId != null;
    }

    public boolean ytLogin(){
        return googleId != null && mail != null;
    }
}
