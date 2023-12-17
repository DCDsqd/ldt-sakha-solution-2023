<#import "parts/common.ftlh" as common>
<#import "parts/navbar.ftlh" as navbar>
<#import "parts/header.ftlh" as header>
<@common.page>
<@navbar.navbar isLogin=isLogin/>
<@header.header />
<section class="page-section" id="contact">
    <div class="container">
        <!-- Privacy Policy -->
        <div>
            <p class="text-center">
                Регистрируясь на сайте вы подтверждаете, что согласны с <a class="" href="/policy">
                    политикой в отношении обработки персональных данных
                </a>
            </p>
        </div>
        <!--Login-->
        <h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">Войдите с помощью соцсетей</h2>
        <!-- Icon Divider-->
        <div class="divider-custom">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>
        <!-- Button for auth -->
        <div class="row justify-content-center">
            <div class="col-lg-8 col-xl-7">
                <div class="text-center mt-4">
                    <a class="btn btn-xl btn-outline-primary" href="/oauth2/authorization/google">
                        Google!
                    </a>
                </div>
                <div class="text-center mt-4">
                    <a class="btn btn-xl btn-outline-primary" href="/oauth2/authorization/vk">
                        Vk!
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
</@common.page>