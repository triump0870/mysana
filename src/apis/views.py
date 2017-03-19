from apis.serializers import GoalSerailizer
from goals.models import Goal
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apis.permissions import IsOwnerOrModerator


# Create your views here.

class ListCreateGoals(ListCreateAPIView):
    serializer_class = GoalSerailizer
    queryset = Goal.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super(ListCreateGoals, self).get_queryset()
        return queryset.filter(user=self.request.user)


class DetailUpdateGoal(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerailizer
    queryset = Goal.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrModerator,)

    def patch(self, request, *args, **kwargs):
        goal = self.get_object()

        if not goal.completed:
            goal.completed = True
            goal.save()
        serializer = self.get_serializer(goal)

        return Response(serializer.data, status=204)
