from datetime import timedelta


def round_to_seconds(datetime_obj):
    if datetime_obj.microsecond >= 500000:
        datetime_obj = datetime_obj + timedelta(seconds=1)

    return datetime_obj.replace(microsecond=0)
