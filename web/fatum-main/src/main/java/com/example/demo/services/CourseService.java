package com.example.demo.services;


import com.example.demo.entitys.Course;
import com.example.demo.repositories.MyCourseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class CourseService {
    private final MyCourseRepository courseRepository;

    @Autowired
    public CourseService(MyCourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    public List<Course> findAllByName(String name){
        return courseRepository.findAllByProfessionName(name);
    }

    public void fillDb(){
        courseRepository.deleteAll();
        String name;
        ArrayList<String> list;

        list = new ArrayList<>();
        name = "Агроном";
        list.add("Агрономия - Институт непрерывного образования Волгоградского государственного аграрного университета");
        list.add("Агрономия - Отделение среднего профессионального образования Кузбасской государственной сельскохозяйственной академии");
        list.add("Агрономия - Агротехнический колледж Бурятской государственной сельскохозяйственной академии имени В.Р. Филиппова");
        list.add("Экологическое проектирование - Ярославская ГСХА");
        list.add("Экозащита и экоаналитика - Орловский ГАУ");
        list.add("Генетическая и агроэкологическая оценка почв - РГАУ-МСХА им. К.А. Тимирязева");
        list.add("Виноградарство и виноделие - СевГУ");
        list.add("Плодоовощеводство и декоративное садоводство - Горский ГАУ");
        list.add("Селекция, генетика и биотехнология садовых культур - РГАУ-МСХА им. К.А. Тимирязева");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Маркшейдер";
        list.add("Геология - Уфимский государственный нефтяной технический университет");
        list.add("Геофизические методы поисков и разведки минеральных ресурсов - ВГУ");
        list.add("Нефтегазовая геофизика - Саратовский национальный исследовательский государственный университет имени Н.Г. Чернышевского");
        list.add("Горно-геологические информационные системы - Университет МИСИС");
        list.add("Мехатроника и робототехника промышленных комплексов - УГГУ");
        list.add("Маркшейдерское дело - Российский университет дружбы народов имени Патриса Лумумбы");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Реставратор";
        list.add("BIM-проектирование - Калининградский бизнес-колледж");
        list.add("Дизайн интерьера - КАС № 7");
        list.add("Дизайн архитектурной среды - Калининградский бизнес-колледж");
        list.add("Реставрация - Колледж Архитектуры, Дизайна и Реинжиниринга № 26");
        list.add("Реставрация, консервация и хранение произведений станковой живописи - Санкт-Петербургское художественное училище имени Н.К. Рериха");
        list.add("Живопись - Санкт-Петербургский реставрационно-строительный институт");
        list.add("Художник кино и телевидения по костюму - Санкт-Петербургский государственный университет");
        list.add("Станковая живопись - Уральский государственный архитектурно-художественный университет имени Н.С. Алферова");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Слесарь по ремонту строительных машин";
        list.add("Техническое обслуживание и ремонт автомобильного транспорта - Автомобильный, правовой техникум");
        list.add("Техническая эксплуатация подъемно-транспортных, строительных, дорожных машин и оборудования - Хабаровский автомеханический колледж");
        list.add("Техническое обслуживание и ремонт двигателей, систем и агрегатов автомобилей - Краснодарский торгово-экономический колледж");
        list.add("Слесарь по ремонту строительных машин - Краснодарский машиностроительный колледж");
        fillIntoProfession(name, list);


        list = new ArrayList<>();
        name = "Монтажник санитарно-технических систем и оборудования";
        list.add("Мастер по ремонту и обслуживанию инженерных систем жилищно-коммунального хозяйства - Казанский колледж строительства, архитектуры и городского хозяйства");
        list.add("Монтажник санитарно-технических, вентиляционных систем и оборудования - Лужский агропромышленный техникум");
        list.add("Монтаж и эксплуатация внутренних сантехнических устройств, кондиционирования воздуха и вентиляции - Алтайский архитектурно-строительный колледж");
        list.add("Мастер жилищно-коммунального хозяйства - Красноярский монтажный колледж");
        list.add("Мастер по ремонту и обслуживанию инженерных систем жилищно-коммунального хозяйства - Колледж Архитектуры, Дизайна и Реинжиниринга № 26");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Военнослужащий";
        list.add("Наземные транспортные комплексы ракетной техники - МАДИ");
        list.add("Проектирование, производство и эксплуатация ракет и ракетно-космических комплексов - Балтийский государственный технический университет ВОЕНМЕХ им. Д.Ф. Устинова");
        list.add("Оптические телекоммуникационные системы - СПбПУ");
        list.add("Применение и эксплуатация автоматизированных систем специального назначения - Санкт-Петербургский государственный университет аэрокосмического приборостроения");
        list.add("Стрелково-пушечное, артиллерийское и ракетное оружие - БГТУ ВОЕНМЕХ им. Д.Ф. Устинова");
        list.add("Военная журналистика - ВГУ");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Бизнес-аналитик";
        list.add("Международный бизнес и предпринимательство - Санкт-Петербургский государственный университет промышленных технологий и дизайна");
        list.add("Менеджмент в строительстве - Университет Синергия");
        list.add("Цифровая экономика - Университет науки и технологий МИСИС");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Маркетолог";
        list.add("Реклама в сфере СМИ и массовых коммуникаций - Гуманитарный колледж РГГУ");
        list.add("Технологическое предпринимательство - Колледж Университета Синергия");
        list.add("Спортивная журналистика и медиакоммуникации в спорте - МГПУ");
        list.add("Социология рекламы и связей с общественностью - Российский государственный университет им. А.Н. Косыгина (Технологии. Дизайн. Искусство)");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Менеджер по продажам";
        list.add("Товароведение и экспертиза товаров во внутренней и внешней торговле - Сибирский федеральный университет");
        list.add("Маркетинг, торговая и закупочная деятельность - КФУ им. В.И. Вернадского");
        list.add("Предпринимательство и управление малым бизнесом - Московский финансово-промышленный университет Синергия");
        list.add("Интернет-маркетинг - Колледж Международного института дизайна и сервиса");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Digital-маркетолог";
        list.add("Медиа обеспечение государственных интересов и национальной безопасности (иновещание и новые медиа) - РАНХиГС");
        list.add("Финансовая математика и управление рисками - РАНХиГС");
        list.add("Социология рекламы и связей с общественностью - Российский государственный университет им. А.Н. Косыгина (Технологии. Дизайн. Искусство)");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Контент-менеджер";
        list.add("Лингвистика - Российский университет дружбы народов имени Патриса Лумумбы");
        list.add("Начальное образование и русский язык - Московский городской педагогический университет");
        list.add("Классическая филология - Санкт-Петербургский государственный университет");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Медсестра | Медбрат";
        list.add("Сестринское дело - Санкт-Петербургский государственный университет");
        list.add("Лечебное дело - Академия управления городской средой, градостроительства и печати");
        list.add("Акушерское дело - Ставропольский базовый медицинский колледж");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Врач";
        list.add("Педиатрия - Крымский федеральный университет имени В.И. Вернадского");
        list.add("Стоматология - Санкт-Петербургский государственный университет");
        list.add("Медицинская биофизика - УрФУ им. Б.Н. Ельцина");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Реабилитолог";
        list.add("Лабораторная диагностика - Пермский базовый медицинский колледж");
        list.add("Адаптивная физическая культура - Тольяттинский социально-педагогический колледж");
        list.add("Педиатрия - КФУ им. В.И. Вернадского");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Фельдшер";
        list.add("Медико-профилактическое дело - Свердловский областной медицинский колледж");
        list.add("Лечебное дело - Колледж Московского финансово-промышленного университета \"Синергия\"");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "AI-тренер";
        list.add("Издательские процессы в медиасфере - СПбГУПТД");
        list.add("Медиаиндустрия - КФУ им. В.И. Вернадского");
        list.add("Газетно-журнальное издательское дело - Московский Политех");
        fillIntoProfession(name, list);

        list = new ArrayList<>();
        name = "Гейм-дизайнер";
        list.add("Курс 1");
        list.add("Курс 2");
        list.add("Курс 3");
        fillIntoProfession(name, list);
    }


    private void fillIntoProfession(String name, List<String> list){
        for(int i = 0; i < list.size(); ++i){
            Course course = new Course();
            course.setProfessionName(name);
            course.setInfo(list.get(i));

            courseRepository.save(course);
        }
    }
}
