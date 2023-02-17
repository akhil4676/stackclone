from django.shortcuts import render
from stack.models import Answer, Questions

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication,permissions
from stackapi.serializers import QuestionSerializers,AnswerSerializers
from rest_framework.decorators import action
from rest_framework import mixins,generics,serializers
# Create your views here.
class QuestionsView(viewsets.ModelViewSet):
    serializer_class=QuestionSerializers
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=["get","post","put"]




    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

    def add_answer(self,request,*args,**kw):
        question=self.get_object()
        user=request.user
        serializer=AnswerSerializers(data=request.data,context={"user":user,"questions":question})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class QuestionDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Questions.objects.all()
    serializer_class=QuestionSerializers
    def delete(self,request,*args,**kw):
        return self.destroy(request,*args,**kw)

class AnswersView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    # authentication_classes=[authentication.TokenAuthentication]

    @action(methods=["POST"],detail=True)
    def up_vote(self,request,*args,**kw):
        id=kw.get("pk")
        answer=Answer.objects.get(id=id)
        user=request.user
        answer.up_vote.add(user)
        answer.save()
        return Response(data="you upvoted ")

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        object=Answer.objects.get(id=id)
        if object.user==request.user:

            Answer.objects.filter(id=id).delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("you dont have permissions")



    

    # def get_queryset(self):
    #     return Questions.objects.filter(user=self.request.user)

   
    # def create(self,request,*args,**kw):
    #     user=request.user
    #     serializer=QuestionSerializers(data=request.data,context={"user":user})
    #     if serializer.is_valid():
    #         serializer.save()
           
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.error)