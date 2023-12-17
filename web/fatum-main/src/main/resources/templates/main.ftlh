<#import "parts/common.ftlh" as common>
<#import "parts/navbar.ftlh" as navbar>
<#import "parts/header.ftlh" as header>
<@common.page>
<@navbar.navbar isLogin=isLogin/>
<@header.header />
    <section class="page-section portfolio" id="portfolio">
        <div class="container">
            <h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">Начать сейчас</h2>
            <!-- Icon Divider-->
            <div class="divider-custom">
                <div class="divider-custom-line"></div>
                <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
                <div class="divider-custom-line"></div>
            </div>
        </div>
        <section class="page-section bg-primary text-white mb-0" id="about">
            <div class="text-center mb-0">
                <div class="ms-auto">
                    <p class="lead">
                        Для начала рекомендуем вам авторизировать все доступные аккаунты, чтобы получить более точные результаты.
                    </p>
                    <div class="text-center mt-4">
                        <a class="btn btn-xl btn-outline-primary" href="/account">
                            Аккаунт
                        </a>
                    </div>
                </div>
            </div>
        </section>
        <section class="page-section bg-white text-primary mb-0" id="about">
            <div class="text-center mb-0">
                <div class="ms-auto">
                    <p class="lead">
                        Если вы хотите воспользоваться сервисом, просто нажмите сюда, придется немного подождать, пока происходит анализ.
                    </p>
                    <div class="text-center mt-4">
                        <a class="btn btn-xl btn-outline-primary" href="/result">
                            Получить результаты
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </section>

</@common.page>