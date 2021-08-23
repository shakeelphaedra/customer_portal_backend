from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dispatch.serializers import DispatchLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customer_dashboard.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

from dispatch.query import ( get_dispatches, get_dispatch_details, get_dispatch_parts,
                             get_dispatch_invoices, check_note_availability, search_parts,
                             update_dispatch_status)

from customer_dashboard.custom_exception import NotFoundError, ConnectionError, ESCDataNotFetchingError
from dispatch.custom_exception import DispatchUpdateError
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


class DispatchNotesAvailabilityView(APIView):
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



class SearchPartsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, disp_no, part_name):
        try:
            response = search_parts(part_name)
            return Response(response)
        except NotFoundError:
            return Response({
                'error': True,
                'status': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {part_name} in Parts.'
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



class UpdateDispatchStatus(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request, disp_no, **kwargs):
        try:
            status =  request.data['status'].upper()
            valid_status = ['OFF', 'TRAVEL', 'WORKING']
            if status and  status in valid_status:
                
                context = update_dispatch_status(status, disp_no)
                return Response({'status': status,
                                'dispatch': disp_no})
            else:
                return Response({
                    'error': True,
                    'message': 'Your status is not valid'
                })

        except ConnectionError:
            return Response({
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': INTERNAL_SERVER_ERROR_500_MESSAGE
            })
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Error occured while updating status'
            })




        
