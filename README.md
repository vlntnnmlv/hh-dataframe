# hh-dataframe

Python script to collect vacancies data from [hh.ru](https://www.hh.ru/)

Generates *.csv* file with `;` as separtor which contains gathered data.
You can load it with `pandas.read_csv()` to use in tour scripts.
Run:
 - python main.py `area` `backstep`

`area` - string, name of a region.
`backstep` - amount of days to step back from today while gathering data from hh.ru

___

## Dependencies

 - [windscribe](https://windscribe.com/download)

 VPN Client. Used for IP changing when requests limit is reached.
