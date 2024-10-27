import json

from django.shortcuts import render
# from .models import DeliveryPersons
# from .serializers import DeliveryPersonSeiralizer
# import logging
# logger = logging.getLogger(__name__)
#
# from django.conf import settings
# from django.core.mail import send_mail

from datetime import datetime, date, timedelta
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .deliveryperson import delivery_action
from .orders import run_function
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .autozad_grpc_client import get_example_data

####AutoZod Modules######
from .Dashboard import active_tasks_list,  dashboard_map, dashboard_agent_list
from .Task_Requests import task_request
from .tasks import Tasks_Section, task_list_daterange
from .Agents import Agent, Agent_display, Agent_update, Agent_delete, Agent_create, agent_action
from .countrycodes import country_codes
from .settings import AutoZodSettings
from .create_team import create_new_team, create_team_settings

# Create your views here.
class DeliveryView(APIView):
    def get(self,request):
        # orders = self.request.query_params.get('orders')
        # result = delivery_action(orders)
        result = run_function()
        return Response({'status':result})



def fetch_data_from_delivery_api():
    # Code to fetch data from your API or another source
    response = requests.get('http://localhost:8005/api/delivery/')
    # return response.json()['data']
    result = response.json()['status']
    print(f'#######{result}')
    return str(result)
@api_view(['GET'])
def example_view(request):
    # Fetch some data from your API
    # api_data = fetch_data_from_delivery_api()
    try:
        api_data = fetch_data_from_delivery_api()
        # Pass this data to your gRPC function
        data = get_example_data(api_data)
        # Return the response from the gRPC service as a JSON response
        return JsonResponse({'response_data': data})

    except Exception:
        return JsonResponse({'response_data':'details not available'})



class Delivery_acceptace_view(APIView):
    def post(self,request):
        # response = request.data.get('response')
        # resp = request.GET.get('resp')
        data = request.data
        print(data)
        json_data = json.dumps(data)
        print(json_data)
        print(type(json_data))
        return HttpResponse(json_data, content_type='application/json')
        # return JsonResponse(json_data, content_type='application/json', safe = False)
        # return Response(json_data, content_type='application/json')
        # resp = str(json_data["resp"])
        # if resp == "yes":
        #     return HttpResponse({'status':'assigned'})
        #     # break
        #
        # elif resp == 'no':
        #     return HttpResponse({'status':'clear the dpartner details'})


#+++++++++++++++++++++++++++AutoZod views code +++++++++++++++++++++++++++

# +++++Dashboard section +++++++++++++++
#dashboard page active_task_view
@api_view(['GET'])
def active_tasks_view(request):

    end_date = date.today()
    start_date = end_date - timedelta(days = 20)
    # print(start_date)
    # print(type(start_date))
    # result = active_tasks_list('2024-09-26', '2024-07-20') #convert datetime format into string format usint str() built in function.
    result = active_tasks_list(str(start_date), str(end_date)) #convert datetime format into string format usint str() built in function.
    print(len(result))
    return Response({'ActivetasksList':result})

#dashboard maps view
@api_view(['GET'])
def dashboard_map_view(request,merchant_id):
    result = dashboard_map(merchant_id)
    return Response({'dashboard_map_list': result})

#dashboard agent list view
@api_view(['GET'])
def dashboard_agent_view(request):
    result = dashboard_agent_list()
    print(len(result))
    return Response({'dashboard_agent_list': result})




# +++++Task Requests Section +++++++++++++++++++++++
class Task_Request_View(APIView):

    def get(self, request):
        result = task_request()
        if result:
            return Response({'task_request_result': result})
        return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data available'})


# +++++++++++++++tasks section +++++++++++++++


@api_view(['GET'])
def tasks_list_view(request):
    result = Tasks_Section()
    if result:
        return Response({'tasks_list': result})
    return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data available'})
@api_view(['GET'])
def task_list_by_daterange_view(request):
    data = request.data
    from_date = data['from_date']
    end_date = data['end_date']
    # print('data:', data)
    # from_date = request.query_params.get('from_date')
    # end_date = request.query_params.get('end_date')

    # result = task_list_daterange('2024-08-08T06:48:32.438+00:00', '2024-08-14T06:07:47.503+00:00')
    # result = task_list_daterange('2024-08-08', '2024-08-14')
    result = task_list_daterange(from_date,end_date)
    print(len(result))
    if result:
        return Response({'tasklist_by_daterange': result})
    return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data available'})



#+++++Agents section ++++++++++++++++++++
@api_view(['GET','PUT','DELETE','POST'])
def Agent_details(request, phone=None):

    if request.method == 'GET':
        if phone is None:
            result = Agent()
            # print(result)
            if result:
                return Response({'agents': result})
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message':'No data available'})
        else:
            result = Agent_display(phone)
            if result:
                return Response({'single_agent_details': result})
            return Response({'status': status.HTTP_204_NO_CONTENT, 'message':'No data available'})
    elif request.method == 'PUT':
        data = request.data
        result = Agent_update(phone,data)
        if result:
            return Response({'result': result})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'details are not updated'})
    #
    elif request.method == 'DELETE':
        result = Agent_delete(phone)
        if result:
            return Response({'result': result})
        return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'details are not available'})

    elif request.method == 'POST':
        data = request.data
        print('data:', data)
        # data = {'firstName': 'ravindra', 'lastName': 'reddy', 'email': 'Ravindra.S@silversnakeit.com',
        #         'phone': '7204273233'}
        result = Agent_create(data)
        if result:
            return Response({'status': status.HTTP_201_CREATED, 'message': result})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'resource not created'})

@api_view(['PATCH'])
def Agent_action(request):
    data = request.data
    result = agent_action(data)
    if result:
        return Response({'status': status.HTTP_200_OK, 'message': result})
    return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Details not available'})

#++++++++countrycode get api+++++++++++++
@api_view(['GET'])
def countrycodes_view(request):
    result = country_codes()
    if result:
        return Response({'status': status.HTTP_200_OK, 'data': result})
    return Response({'status': status.HTTP_204_NO_CONTENT, 'message': 'No data available'})



#+++++++++++++create new team +++++++++++++

@api_view(['POST'])
def create_team_view(request):
    data = request.data
    print('data:', data)
    result = create_new_team(data)
    if result:
        return Response({'status': status.HTTP_201_CREATED, 'message': result})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'resource not created'})

def team_settings_view(request):
    data = request.data
    result = create_team_settings(data)
    if result:
        return Response({'status': status.HTTP_201_CREATED, 'message': result})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'resource not created'})



#+++++++++++++settings section++++++++++++++++

@api_view(['POST'])
def settings_view(request):
    data = request.data
    result = AutoZodSettings(data)
    if result:
        return Response({'status': status.HTTP_201_CREATED, 'message': result})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'resource not created'})

#+++++++++++dpartner getting notification either accept/decline then return back send data like orderId, dpartnerId, notification_status

def dpartner_notification_response(data):
    orderId = data['orderId']
    dpartnerId = data['dpartnerId']
    notification_status = data['notification_status']
    # return {"orderId": orderId, "dpartnerId": dpartnerId, "notification_status": notification_status}
    payload = {'orderId': orderId, 'dpartnerId': dpartnerId}
    response = requests.post(url='https://zhzmlspf-9080.inc1.devtunnels.ms/api/admin/orders/assign', json=payload,headers={"Content-Type": "application/json"})
    print('dresponse:', response)
    return response

@api_view(['POST'])
def get_dpartner_notification_view(request):
    data = request.data
    print(f'data: {data}')
    result = dpartner_notification_response(data)
    if result:  #I think these details not necessary for my assumption
        # return Response({'status': status.HTTP_200_OK, 'message': 'order assigned'})
        return Response({'status': status.HTTP_200_OK, 'message': result})
    return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'resource not created'})





