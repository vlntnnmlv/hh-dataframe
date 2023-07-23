# hh-dataframe

# English

Python script to collect vacancies data from [hh.ru](https://www.hh.ru/)

Generates *.csv* file with `;` as separtor which contains gathered data.
You can load it with `pandas.read_csv()` to use in tour scripts.

___

## Run

 - `python main.py <area> <backstep>`

`area` - string, name of a region.
`backstep` - amount of days to step back from today while gathering data from hh.ru

___

## Dependencies

 - [windscribe](https://windscribe.com/download)

 VPN Client. Used for IP changing when requests limit is reached.
 
# Русский

Скрипт для сбора данных с [hh.ru](https://www.hh.ru/) на Python3.

Генерирует *.csv* файл с разделителем `;`, который содержит собранные данные.
Для использование в своих скриптах, Вы можете использовать `pandas.read_csv()`.

___

## Запуск

 - `python main.py <area> <backstep>`

`area` - строка, название региона. Регион должен быть доступен через справочник регионов [hh.ru](https://www.hh.ru/).
`backstep` - количество последних дней, за которые нужно собрать данные.

___

## Зависимости

 - [windscribe](https://windscribe.com/download)

 VPN клиент, использованный для виртуальной смены IP-адреса.
