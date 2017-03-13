from apis.serializers import GoalSerailizer
from goals.models import Goal
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class ListCreateGoals(ListCreateAPIView):
    serializer_class = GoalSerailizer
    queryset = Goal.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailUpdateGoal(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerailizer
    queryset = Goal.objects.all()
    permission_classes = (IsAuthenticated,)

    # def patch(self, request, *args, **kwargs):
    #     goal = self.get_object()
    #     if not goal.completed:
    #         goal.completed = True
    #     serializer = self.get_serializer()
    #
    #     return Response(serializer(goal).data, status=204)