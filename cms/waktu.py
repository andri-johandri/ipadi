from dateutil import tz

def indonesia_time(args, with_time=False):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Jakarta')
    wib = args.replace(tzinfo=from_zone)
    wib = wib.astimezone(to_zone)
    if with_time:
        return f"{wib.strftime('%d-%B-%Y %H:%M')} WIB"
    return wib.strftime('%d-%B-%Y')



