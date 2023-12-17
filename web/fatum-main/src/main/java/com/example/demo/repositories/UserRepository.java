package com.example.demo.repositories;

import com.example.demo.entitys.MyUser;
import com.example.demo.services.MyUserService;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<MyUser, Long> {
    MyUser findByVkId(String id);
    MyUser findByToken(String token);
    MyUser findByMail(String mail);
    MyUser findByGoogleToken(String googleToken);
    MyUser findByGoogleId(String id);
}
