from rest_framework import serializers
from goals.models import Goal


class GoalSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'slug', 'title', 'description', 'end_date')
        read_only_fields = ('id', 'slug')

    def to_representation(self, instance):
        goal = super(GoalSerailizer, self).to_representation(instance)
        goal['slug'] = instance.slug
        goal['is_completed'] = instance.completed
        return goal
