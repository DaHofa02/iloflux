import ilo
import influx
import yml

config = yml.get_config()

for name in config:
    url = config[name]['url']

    host = ilo.get_hostname(url)

    temp = ilo.get_temperature(url)
    influx.export_temps(temp, host)

    watts = ilo.get_watts(url)
    influx.export_watts(watts, host)

    fans = ilo.get_fans(url)
    influx.export_fans(fans, host)