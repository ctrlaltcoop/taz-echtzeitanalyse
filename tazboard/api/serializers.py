from rest_framework import serializers


class HistogramDataSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    hits = serializers.IntegerField()


class HistogramSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = HistogramDataSerializer(many=True)


class ReferrerDataSerializer(serializers.Serializer):
    referrerclass = serializers.CharField()
    referrertag = serializers.CharField()
    hits = serializers.IntegerField()
    hits_previous = serializers.IntegerField()
    percentage = serializers.FloatField()
    percentage_previous = serializers.FloatField()


class ReferrerSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_previous = serializers.IntegerField()
    data = ReferrerDataSerializer(many=True)


class DevicesDataSerializer(serializers.Serializer):
    deviceclass = serializers.CharField()
    value = serializers.IntegerField()


class DevicesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = DevicesDataSerializer(many=True)


class ToplistDataSerializer(serializers.Serializer):
    headline = serializers.CharField()
    kicker = serializers.CharField(required=False, allow_null=True)
    pubdate = serializers.DateTimeField(required=False, allow_null=True)
    hits = serializers.IntegerField()
    hits_previous = serializers.IntegerField()
    referrers = ReferrerSerializer()


class ToplistSerializer(serializers.Serializer):
    data = ToplistDataSerializer(many=True)
