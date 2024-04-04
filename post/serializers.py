from rest_framework import serializers

from post.models import PostComment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"
