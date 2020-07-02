from rest_framework import serializers


class HistogramDataSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    value = serializers.IntegerField()


class HistogramSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = HistogramDataSerializer(many=True)


class ReferrerDataSerializer(serializers.Serializer):
    referrerclass = serializers.DateTimeField()
    value = serializers.IntegerField()


class ReferrerSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = ReferrerDataSerializer(many=True)
