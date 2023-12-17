# Решение 4 кейса ЛЦТ Якутия для Профилум

[Функционал и интерфейс](#Функционал) <br>
[Датасет](#Датасет) <br>
[Модель](#Модель) <br>
[Предсказание и данные пользователя для него](#Предсказание) <br>
[Архитектура](#Архитектура) <br>
[Как развернуть решение](#Деплой) <br><br>
[ОЧЕНЬ ВАЖНО К ПРОЧТЕНИЮ ПЕРЕД ТЕСТИРОВАНИЕМ!](#ВАЖНО!) <br><br>

# Деплой
Ниже подробно описывается процесс развертывания данного решения и всего, что для этого пригодится:

## Регистрация и настройка приложения в VK <br>
Приложение в VK нужно для получения веб-сервисом доступа к функционалу авторизации через интерфейс VK ID. <br>
Управлять и создавать приложения можно [отсюда](https://vk.com/apps?act=manage) <br>
Про OAuth авторизацию с помощью VK ID [здесь](https://dev.vk.com/ru/api/access-token/getting-started) <br>
Ваше приложение должно запрашивать доступ к личным данным, а именно - группам, в которых пользователь состоит, его стене и понравившемся записям. <br>

## Регистрация и настройка приложения в Google Cloud API & Services <br>
Приложение Google необходимо для авторизации пользователя через Google аккаунт и для использования YouTube API. <br>
Первым делом нужно создать проект на официальном сайте [Google Cloud API & Services](https://console.cloud.google.com/apis). <br> Затем, в интерфейсе нужно нажать кнопку **+Enable APIs and services** <br><br>
![image](https://github.com/DCDsqd/ldt-sakha-solution-2023/assets/89082426/9dbcc917-9931-4985-9d03-be35b7dcb55b)
В поиске по библиотеке найти YouTube Data API v3 и активировать данное API для своего проекта ![image](https://github.com/DCDsqd/ldt-sakha-solution-2023/assets/89082426/a4668663-3492-4123-97c1-ee7dc87a3a3e)
Затем, во вкладке OAuth consent screen нужно зарегестрировать и настроить Ваше приложение. Из важного на данном этапе - не забыть добавить **auth/youtube.readonly** на шаге **Scopes** и список тестировщиков на последующем шаге. 
**ВАЖНО:** до верификации приложения Google пользоваться им смогут только те пользователи, которые указаны в списке тестировщиков! Поэтому, добавляйте туда всех, кто будет пользоваться сервисом (даже если Вы - владелец проекта)
![image](https://github.com/DCDsqd/ldt-sakha-solution-2023/assets/89082426/d81b42c6-a399-4f47-a319-bdfed2dbf2ae)
Последний шаг - создание Credentials. Эти данные позволят непосредственно веб-сервису использование API от лица вашего Google Cloud приложения. Для этого заходим во вкладку Credentials и создаем (обязательно!) Credentials для OAuth 2.0 Client IDs
![image](https://github.com/DCDsqd/ldt-sakha-solution-2023/assets/89082426/f54ce701-eb99-4d1f-b2ac-c0c1905cd2a6)
Далее скачиваем файл с Credentials в формате JSON и размещаем его по пути ```backend/api_server/secrets/google_project_secret.apps.googleusercontent.com.json``` для корректной работоспособности ML-сервиса. <br>

## Развертка, конфигурация и установка зависимостей для сервисов <br>
На данном этапе будем считать, что все виртуальные машины для подсервисов запущены и развернуты на сервере(ах) в соответствии с [архитектурой](#Архитектура), и на каждой из них есть исходный код. <br><br>
Теперь, нужно настроить конфигурации ML и Web сервисов для их корректного общения через REST API, а также для коннекта с базами данных. <br>
**Для ML-сервиса:**
* Создать виртуальное окружение
* Установить зависимости через `pip install backend/api_service/requirements.txt`
* ~~Молиться, что все зависимости установились~~
* 

## Запуск сервисов <br>
**Для ML-сервиса**: Из папки ```backend/api_server``` запустите ```python main.py```, чтобы запустить сервис с конфигурацией из конфига, либо можно указать `host` и `port` напрямую, выполнив `uvicorn main:app --host [host] --port [port]`.



# ВАЖНО
К сожалению, VK и Google в целях безопасности не позволяют непроверенным приложениям получать доступ ко многим данным пользователя. Поэтому, до верификации этих приложений VK API работать не будет вообще, а Google будет работать только для тех пользователей, которые числятся как тестировщики (см. **Регистрация и настройка приложения в Google Cloud API & Services**) <br>
Другого обходного легального пути для получения данных из этих сервисов нет. <br>
### **Приложения, через которые работает сервис, запущенный на хосте для демонстрации на момент дедлайна НЕ ВЕРИФИЦИРОВАНЫ -> функционал серъезно ограничен!** <br>
### **Если у вас не работает авторизация или некоторые запросы - дело в этом!** <br>
Мы оставили заявки на верификацию наших приложений, но так и не дождались её :(

**Ещё одно важное замечание по поводу квоты YouTube API:** Для неверефицированного приложения квота - 10000 токенов в день. На обслуживание одного пользователя за счёт наших внутренних оптимизаций уходит примерно 200-250 токенов, однако этого все равно может не хватить. Можно зарегестрировать несколько приложений (вроде как это не противоречит правилам Google), однако автоматического способа это делать у нас нет. После верификации приложения квота значительно увеличивается. К тому же, можно запросить бесплатное повышение квоты, подробно описав свою задачу и планы на использование в заявке.
