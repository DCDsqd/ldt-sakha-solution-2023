<#import "parts/common.ftlh" as common>
<#import "parts/navbar.ftlh" as navbar>
<#import "parts/header.ftlh" as header>
<@common.page>
<@navbar.navbar isLogin=isLogin/>
<@header.header />
<section class="answer">
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'></script>
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.bundle.min.js'></script>

    <section class="page-section portfolio" id="portfolio">
        <div class="col-xs-12 text-center text-primary">
            <h2 class="page-section-heading text-center text-uppercase text-primary">Вам отлично подходит: ${bestProfession}</h2>
            <div class="divider-custom">
                <div class="divider-custom-line"></div>
                <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
                <div class="divider-custom-line"></div>
            </div>
        </div>
        <div class="container">
            <h2 class="text-center text-uppercase text-primary">Подходящие курсы</h2>
            <div class="padding">
                <div class="row justify-content-center">
                    <#list courses_list as course>
                        <div class="col-md-6 col-lg-4 mb-5">
                            <h4 class="text-primary">Название</h4>
                            <div class="ms-auto" data-bs-toggle="modal" data-bs-target="#portfolioModal2">
                                <a class="" href="#">
                                    ${course.getInfo()}
                                </a>
                            </div>
                        </div>
                    </#list>
                </div>
            </div>
        </div>
        <div class="container">
            <h3 class="text-center text-uppercase text-primary">Другие подхолящие професии</h3>
            <div class="padding">
                <#list prof_list as profession>
                    <div class="">
                        <#list profession as key, value>
                            <h5 class="text-primary">${key}= ${value}</h5>
                        </#list>
                    </div>
                </#list>
            </div>
        </div>

        <h3 class="text-center text-uppercase text-primary">Информация о выборе</h3>

        <div id="donut-chart"></div>
        <script>
            $(document).ready(function() {
                var ctx = $("#chart-line");
                var probabilityData = [<#list topProbabilities as probability>${probability?number},</#list>];
                var professionData = [<#list topProfessions as profession>"${profession}",</#list>];
                var colorData = [<#list colorProfessions as color>"${color}",</#list>];
                var myLineChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: professionData,
                        datasets: [{
                            data: probabilityData,
                            backgroundColor: colorData
                        }]
                    },
                    options: {
                        title: {
                            display: true,
                            text: 'Диаграмма подходящих'
                        }
                    }
                });
            });
        </script>
        <div class="container">
            <div class="padding">
                <div class="row justify-content-center">
                    <div class="col-md-6 col-lg-6 mb-5">
                        <h2 class="text-primary text-center">Диаграмма</h2>
                        <canvas id="chart-line" width="299" height="200" class="chartjs-render-monitor" style="display: block; width: 299px; height: 200px;"></canvas>
                    </div>
                    <div class="col-md-6 col-lg-6 mb-5">
                        <h2 class="text-primary">Видео, которые больше всего повлияли на результат</h2>
                        <#list yt_impactful_likes as like>
                            <div class="ms-auto" data-bs-toggle="modal" data-bs-target="#portfolioModal2">
                                <h6 class="text-success">${like.getName()}</h6>
                                <a class="" href="https://www.youtube.com/watch?v=${like.getId()}">
                                    Ссылка
                                </a>
                            </div>
                        </#list>
                    </div>
                </div>
                <div class="row justify-content-center">
                    <div class="col-md-6 col-lg-4 mb-5 mb-lg-0">
                        <h2 class="text-primary">Каналы, которые больше всего повлияли на результат</h2>
                        <#list yt_impactful_channels as channel>
                            <div class="ms-auto" data-bs-toggle="modal" data-bs-target="#portfolioModal2">
                                <h4 class="text-success">${channel.getName()}</h4>
                                <a class="" href="https://www.youtube.com/channel/${channel.getId()}">
                                    Ссылка
                                </a>
                            </div>
                        </#list>
                    </div>
                    <div class="col-md-6 col-lg-4 mb-5 mb-lg-0">
                        <h2 class="text-primary">Группы, которые больше всего повлияли на результат</h2>
                        <#list vk_groups as group>
                            <div class="ms-auto" data-bs-toggle="modal" data-bs-target="#portfolioModal2">
                                <h4 class="text-success">${group.getName()}</h4>
                                <a class="" href="https://vk.com/public${group.getId()}">
                                    Ссылка
                                </a>
                            </div>
                        </#list>
                    </div>
                </div>
            </div>
        </div>
    </section>
</section>
</@common.page>