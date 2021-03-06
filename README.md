# HTTPServer

## Класс HttpGetHandler:
Клас отвечает за обработку GET-запросов.

### Запросы
- 127.0.0.1:8000/geonameid/"geonameid" - выводит информацию о городе по geonameid;
- 127.0.0.1:8000/page/"pageNumber+citiesNumber" - выводит информацию о citiesNumber городах, которые находятся на pageNumber странице;
- 127.0.0.1:8000/ru/"cityName1+cityName2" - выводит информацию о городах cityName1 и cityName2, которые вводятся на русском, а также информацию о том, 
какой город находится севернее и разницу в часовых поясах.

## Метод get_city_data(geonameid)
На вход подаётся id города, в файле ищется город с выбранным id, возвращает массив данных о найденном городе.

## Метод get_page_cites_data(pageNum, citiesNum)
На вход подаются номер страницы и количество городов на этой странице. Считается количество городов в файле, считается номер строки, с которой будет начинаться страница, 
проверяются границы файла, считываются найденные строки с файла, возвращает двумерный массив с данными о городах.

## Метод get_data_ru(city1, city2)
На вход подаются названия городов на русском, находятся все города с данными названиями, вызывается функция search_max_pop(city). На выход функции search_max_pop(city) подаётся 
массив городов, для поиска города с самым большим населением и возврата ширины, долготы и временной зоны. Генерируется строка, которая хранит информацию о том, какой город 
находится севернее и на сколько отличается часовой пояс. Возвращает строку с информацией о местонахождениях городов и разницей часовых поясов, двумерный массив с данными 
о городах.
