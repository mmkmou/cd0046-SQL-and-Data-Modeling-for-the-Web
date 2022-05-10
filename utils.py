import dateutil.parser
import babel


def format_datetime(value, _format='medium'):
    if (value.__class__.__name__ == "datetime"):
        value = value.strftime("%Y-%m-%dT%H:%M:%S.%jZ")
    date = dateutil.parser.parse(value)
    if _format == 'full':
        _format="EEEE MMMM, d, y 'at' h:mma"
    elif _format == 'medium':
        _format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, _format, locale='en')


def format_boolean(value):
    
    if value == 'y': 
        return True
    else:
        return False