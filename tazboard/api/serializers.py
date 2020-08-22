from rest_framework import serializers


class HistogramDataSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    hits = serializers.IntegerField()


class HistogramSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = HistogramDataSerializer(many=True)


class ReferrerDataSerializer(serializers.Serializer):
    referrer = serializers.CharField(allow_blank=True)
    hits = serializers.IntegerField()
    percentage = serializers.FloatField()


class ReferrerSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = ReferrerDataSerializer(many=True)


class DevicesDataSerializer(serializers.Serializer):
    deviceclass = serializers.CharField()
    hits = serializers.IntegerField()


class DevicesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = DevicesDataSerializer(many=True)


class ArticleDataSerializer(serializers.Serializer):
    headline = serializers.CharField()
    url = serializers.CharField(required=False, allow_null=True)
    kicker = serializers.CharField(required=False, allow_null=True)
    pubdate = serializers.DateTimeField(required=False, allow_null=True)
    hits = serializers.IntegerField()
    hits_previous = serializers.IntegerField()
    referrers = ReferrerDataSerializer(many=True)
    devices = DevicesDataSerializer(many=True)
    msid = serializers.IntegerField()
    bid = serializers.IntegerField(required=False, allow_null=True)
    frontpage = serializers.BooleanField(default=False)
    archive = serializers.BooleanField(default=False)


class ToplistSerializer(serializers.Serializer):
    data = ArticleDataSerializer(many=True)


class FireplaceSerializer(serializers.Serializer):
    data = ArticleDataSerializer(many=True)


class TotalSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_previous = serializers.IntegerField()


class SubjectDataSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    article_count = serializers.IntegerField()
    hits = serializers.IntegerField()
    referrers = ReferrerDataSerializer(many=True)
    devices = DevicesDataSerializer(many=True)


class SubjectSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = SubjectDataSerializer(many=True)
