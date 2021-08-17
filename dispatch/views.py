from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dispatch.serializers import DispatchLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customer_dashboard.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from dispatch.query import ( get_dispatches, get_dispatch_details, get_dispatch_parts,
                             get_dispatch_invoices, check_note_availability)
from customer_dashboard.custom_exception import NotFoundError, ConnectionError, ESCDataNotFetchingError
from rest_framework import status
from dispatch.constants import INTERNAL_SERVER_ERROR_500_MESSAGE
# Create your views here.



class DispatchLoginView(TokenObtainPairView):
    serializer_class = DispatchLoginSerializer



class DispatchListView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request, emp_no):
        try:
            dispatches = get_dispatches(emp_no)
            return Response(dispatches)
        except NotFoundError:
            return Response({
                'error': True,
                'status': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {emp_no} Employee Number/Employee Number'
            })
        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except ESCDataNotFetchingError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })


class DispatchDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, disp_no):
        try:
            context = get_dispatch_details(disp_no)
            return Response(context)
        except NotFoundError:
            return Response({
                'error': True,
                'status': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {disp_no} Dispatch Number/Dispatch Number'
            })
        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except ESCDataNotFetchingError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })



class DispatchPartsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, disp_no):
        try:
            context = get_dispatch_parts(disp_no)
            return Response(context)
        except NotFoundError:
            return Response({
                'error': True,
                'status': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {disp_no} Dispatch Number/Dispatch Number'
            })
        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except ESCDataNotFetchingError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })


class DispatchHistoryView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, cust_no):
        try:
            context = get_dispatch_invoices(cust_no)
            return Response(context)
        except NotFoundError:
            return Response({
                'error': True,
                'status': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {cust_no} Customer Number/Customer Number'
            })

        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except ESCDataNotFetchingError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })


class DispatchAddNotesView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, disp_no):
        try:
            taken = check_note_availability(disp_no)
            if taken:
                response = {"Taken": True,
                            "Message": "The Note field is being Edited by other user \
                            please wait until they are done editing it."}
            else:
                response = {
                    "Taken": False,
                    "Message": "The note field is free."
                }
            return Response(response)
        except ESCDataNotFetchingError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })



        
