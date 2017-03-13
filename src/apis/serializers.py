from rest_framework import serializers
from goals.models import Goal
from datetime import datetime
from rest_framework.exceptions import ValidationError


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

    def validate_end_date(self, value):
        if value < datetime.now().date():
            raise ValidationError("End date should not be in past")
        return value
