from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from rest_framework.authentication import TokenAuthentication ,BasicAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serial import *
from .models import *
from django.contrib.auth import authenticate
from django.utils.timezone import now

def DicttoQDict(dataa,request):
    if type(dataa)==dict:
        o_dataa = dataa
        dataa = QueryDict('',mutable=True)
        dataa.update(o_dataa)
    else:
        request.data._mutable =True


@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return Response(data='DATA is here')
    

@api_view(['GET','POST'])
def sign_up(request):
    if request.method == "GET":
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Please Add user_name , user_pass1 and user_pass2 to sign up"
            }        
        )
    if request.method == "POST":
        dataa = request.data 
        user_name = dataa['user_name']
        user_pass1 = dataa['user_pass1']
        user_pass2 = dataa['user_pass2']
        try:
            user = User.objects.get(username=user_name)
            if user is not None:
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "message":"User already exit",
                    }
                )
        except User.DoesNotExist:
            pass
        if user_pass1 != user_pass2:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Password and confirm password not Matched...",
                }
            )
        user = User.objects.create_user(username=user_name,password=user_pass1)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"You have succssfully signed up"
            }
        )

@api_view(['POST','GET'])
def sign_in(request):
    if request.method == "GET":
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Please Add signin_user and signin_pass to sing in"
            }        
        )
    if request.method == "POST":
        dataa = request.data 
        signin_user = dataa['signin_user']
        signin_pass = dataa['signin_pass']
        try:
            user = authenticate(username=signin_user,password=signin_pass)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Username or password not corect",
                }
            )
        # print(user)
        if user is None:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Username or password not corect",
                }
            )

        token , created = Token.objects.get_or_create(user=user)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"User Found",
                'data':{               
                'username':str(user),
                'token':str(token.key),
                }
            }
        )



# Function based view
@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profilee(request):   
    if request.method == "GET":
        print("herere i  am")
        user = request.user
        print(user)
        print("________________")
        
        try:
            snippet = Profile.objects.filter(pro_user=user.id)
            print(snippet)
            serialize = ProfileSerial(snippet).data
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile",
                    'data':{    
                        serialize
                    }
                }
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile not found",

                }
            )

@api_view(['GET','POST','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        user = request.user
        print(user)
        print(user.id)
        try:
            snippet = Profile.objects.get(pro_user=user.id)
            print(snippet)
            serialize = ProfileSerial(snippet).data
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile",
                    'data':{    
                        "Profie":serialize
                    }
                }
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile not found",

                }
            )
    if request.method == "POST":
        dataa = request.data
        user = request.user
        DicttoQDict(dataa, request)
        dataa['pro_user'] = user.id
        print(dataa)
        serialize = ProfileSerial(data=dataa)
        # print(serialize.data)
        if serialize.is_valid():
            serialize.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile created",
                    "data":serialize.data
                }
            )
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Invalid input",
            }
        )
        
    if request.method == "PUT":
        user = request.user
        print(user)
        print(user.id)
        try:
            snippet = Profile.objects.get(pro_user=user.id)
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile not found",

                }
            )
        dataa = request.data
        DicttoQDict(dataa, request)
        key = dataa.keys()
        for k in key:
            setattr(snippet,k,dataa[k])
            snippet.save()
        serialize = ProfileSerial(snippet)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Profile Updated",
                "data":serialize.data
            }
        )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def otherprofile(request,id):

    if request.method == "GET":
        # user = request.user
        # print(id)
        # print(user)
        # print(user.id)
        try:
            snippet = Profile.objects.get(pro_user=id)
            print(snippet)
            serialize = ProfileSerial(snippet).data
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile",
                    'data':{    
                        "Profie":serialize
                    }
                }
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile not found",

                }
            )


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def conservation(request):
    if request.method == "GET":
        user = request.user
        print(user)
        print(user.id)
        try:
            snippet = Conservation.objects.filter(cons_first=user.id)
            snippet = snippet.union(Conservation.objects.filter(cons_second=user.id))
            print(snippet)
            serialize = ConservationSerial(snippet,many=True).data
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Conservation",
                    'data':{    
                        "Profie":serialize
                    }
                }
            )
        except Conservation.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Conservation not found",

                }
            )
    if request.method == "POST":
        dataa = request.data
        user = request.user
        DicttoQDict(dataa, request)
        dataa['cons_first'] = user.id
        print(dataa)
        serialize = ConservationSerial(data=dataa)
        # print(serialize.data)
        if serialize.is_valid():
            serialize.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Profile created",
                    "data":serialize.data
                }
            )
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Invalid input",
            }
        )


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat(request,id):
    if request.method == "GET":
        user = request.user
        print(user)
        print(user.id)
        try:
            snippet = Chat.objects.filter(chat_conservation=id)
            print(snippet)
            serialize = ChatSerial(snippet,many=True).data
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Chat",
                    'data':{    
                        "Profie":serialize
                    }
                }
            )
        except Chat.DoesNotExist:
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Chat not found",

                }
            )
    if request.method == "POST":
        dataa = request.data
        user = request.user
        DicttoQDict(dataa, request)
        dataa['chat_sender'] = user.id
        dataa['chat_conservation'] = id
        print(dataa)
        serialize = ChatSerial(data=dataa)
        # print(serialize.data)
        if serialize.is_valid():
            serialize.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message":"Chat created",
                    "data":serialize.data
                }
            )
        
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message":"Invalid input",
            }
        )

