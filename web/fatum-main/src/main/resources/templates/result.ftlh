<#import "parts/common.ftlh" as common>
<#import "parts/navbar.ftlh" as navbar>
<#import "parts/header.ftlh" as header>
<#import "parts/resultPart.ftlh" as result>
<#import "parts/error.ftlh" as error>
<@common.page>
<@navbar.navbar isLogin=isLogin/>
<@header.header />
<section class="answer">
    <#if predict.isValid>
        <@result.result predict=predict prof_list=prof_list courses_list=courses_list/>
    <#else >
        <@error.error/>
    </#if>
</section>
</@common.page>