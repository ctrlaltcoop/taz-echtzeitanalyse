from rest_framework import serializers


class HistogramDataSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    hits = serializers.IntegerField()


class HistogramSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = HistogramDataSerializer(many=True)


class ReferrerDataSerializer(serializers.Serializer):
    referrerclass = serializers.DateTimeField()
    hits = serializers.IntegerField()
    hits_previous = serializers.IntegerField()


class ReferrerSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_previous = serializers.IntegerField()
    data = ReferrerDataSerializer(many=True)


class ToplistDataSerializer(serializers.Serializer):
    headline = serializers.CharField()
    kicker = serializers.CharField()
    hits = serializers.IntegerField()
    hits_previous = serializers.IntegerField()
    referrers = ReferrerDataSerializer(many=True)


class ToplistSerializer(serializers.Serializer):
    data = ToplistDataSerializer(many=True)
