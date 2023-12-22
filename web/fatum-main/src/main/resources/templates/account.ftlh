<#import "parts/common.ftlh" as common>
<#import "parts/navbar.ftlh" as navbar>
<#import "parts/header.ftlh" as header>
<@common.page>
    <@navbar.navbar isLogin=isLogin/>
    <@header.header />
    <section class="page-section portfolio" id="portfolio">
        <div class="col-xs-12 text-center text-primary">
            <h2 class="page-section-heading text-center text-uppercase text-primary">Ваш аккаунт</h2>
            <div class="divider-custom">
                <div class="divider-custom-line"></div>
                <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
                <div class="divider-custom-line"></div>
            </div>
        </div>
        <div class="col-xs-12 text-center text-primary">
            <h4 class="text-primary">Vk</h4>
            <#if user.vkLogin()>
            <h6 class="text-secondary">${user.firstName}</h6>
            <h6 class="text-secondary">${user.lastName}</h6>
            <h6 class="text-secondary">${user.vkId}</h6>
            </#if>
            <div class="text-center mt-4">
                <a class="btn btn-xl btn-outline-primary" href="/oauth2/authorization/vk">
                    Сгенерировать токен Vk
                </a>
            </div>
        </div>
        <div class="divider-custom">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>
        <div class="col-xs-12 text-center text-primary">
            <h4 class="text-primary">Google</h4>
            <#if user.ytLogin()>
            <h6 class="text-secondary">${user.mail}</h6>
            <h6 class="text-secondary">${user.googleId}</h6>
            </#if>
            <div class="text-center mt-4">
                <a class="btn btn-xl btn-outline-primary" href="/oauth2/authorization/google">
                    Сгенерировать токен Google
                </a>
            </div>
        </div>

    </section>
</@common.page>