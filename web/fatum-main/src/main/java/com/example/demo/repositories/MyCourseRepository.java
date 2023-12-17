package com.example.demo.repositories;

import com.example.demo.entitys.Course;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public interface MyCourseRepository extends JpaRepository<Course, Long> {
    ArrayList<Course> findAllByProfessionName(String name);
}
