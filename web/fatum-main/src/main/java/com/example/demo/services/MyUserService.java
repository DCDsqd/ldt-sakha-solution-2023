package com.example.demo.services;

import com.example.demo.entitys.MyUser;
import com.example.demo.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.oauth2.core.OAuth2AccessToken;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.Objects;

@Service("myUserService")
public class MyUserService {
    private UserRepository userRepository;

    @Autowired
    public MyUserService(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    public void oauth2MyUserVk(DefaultOAuth2User defaultOAuth2User, OAuth2AccessToken token){
        MyUser user = userRepository.findByVkId(defaultOAuth2User.getName());
        if(user != null){
            System.out.println("User founded");
            user.setId(user.getId());
            user.setToken(token.getTokenValue());
            userRepository.save(user);
            return;
        }
        user = registrationVk(defaultOAuth2User, token);
        userRepository.save(user);
    }

    public void oauth2MyUserGoogle(OidcUser oidcUser, OAuth2AccessToken token){
        MyUser user = userRepository.findByMail(oidcUser.getEmail());
        if(user != null){
            System.out.println("User founded");
            user.setId(user.getId());
            user.setGoogleToken(token.getTokenValue());
            userRepository.save(user);
            return;
        }
        user = registrationGoogle(oidcUser, token);
        userRepository.save(user);
    }

    public void connectVkAccount(DefaultOAuth2User oldOauthUser, DefaultOAuth2User defaultOAuth2User, OAuth2AccessToken token){
        MyUser oldUser = getUserById(oldOauthUser);
        if(oldUser == null){
            System.out.println("Not Found");
            System.out.println(Objects.requireNonNull(oldOauthUser.getAttribute("email")).toString());
            userRepository.save(registrationVk(defaultOAuth2User, token));
            return;
        }

        oldUser.setId(oldUser.getId());
        oldUser.setToken(token.getTokenValue());
        oldUser.setVkId(defaultOAuth2User.getName());
        oldUser.setFirstName(defaultOAuth2User.getAttribute("first_name"));
        oldUser.setLastName(defaultOAuth2User.getAttribute("last_name"));

        userRepository.save(oldUser);
    }

    public void connectGoogleAccount(DefaultOAuth2User oldOauthUser, OidcUser oidcUser, OAuth2AccessToken token){
        MyUser oldUser = getUserById(oldOauthUser);
        if(oldUser == null){
            userRepository.save(registrationGoogle(oidcUser, token));
            return;
        }
        oldUser.setGoogleId(oidcUser.getName());
        oldUser.setId(oldUser.getId());
        oldUser.setGoogleToken(token.getTokenValue());
        oldUser.setMail(oidcUser.getEmail());

        userRepository.save(oldUser);
    }

    public void addProfession(OAuth2User user, String profession){
        MyUser myUser = getUserById(user);

        if(myUser != null) {
            myUser.setId(myUser.getId());
            myUser.setLastProfession(profession);

            userRepository.save(myUser);
        }
    }

    public MyUser getUserById(OAuth2User user){
        MyUser myUser = null;

        if(user.getAttributes().containsKey("given_name")){
            myUser = userRepository.findByGoogleId(user.getName());
        } else if (user.getAttributes().containsKey("first_name")) {
            myUser = userRepository.findByVkId(user.getName());
        }

        return myUser;
    }

    private MyUser registrationVk(DefaultOAuth2User defaultOAuth2User, OAuth2AccessToken token){
        System.out.println("new User registration");
        MyUser user = new MyUser();
        user.setVkId(defaultOAuth2User.getName());
        user.setFirstName(defaultOAuth2User.getAttribute("first_name"));
        user.setLastName(defaultOAuth2User.getAttribute("last_name"));
        user.setToken(token.getTokenValue());

        return user;
    }

    private MyUser registrationGoogle(OidcUser oidcUser, OAuth2AccessToken token){
        System.out.println("new User registration");
        MyUser user = new MyUser();
        user.setGoogleId(oidcUser.getName());
        user.setMail(oidcUser.getEmail());
        user.setGoogleToken(token.getTokenValue());

        return user;
    }
}
