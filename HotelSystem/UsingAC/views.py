from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Room, DetailedList, Scheduler, air_conditioner_list, service_request, waiting_request,get_current_temp

scheduler = Scheduler()  # 创建 Scheduler 实例 (单例，只创建一次)

def TestRoom():
    room = Room.objects.get(room_id=1003)
    print(f"房间ID：{room.id}")
    return room

def add_cors_headers(response):
    """添加CORS头部的辅助函数"""
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def handle_temperature(request):
    """处理温度调节（升温/降温）请求"""
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({'status': 'ok'}))

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get('action')
            new_temp = data.get('currentTemp')
            if action == 'increaseTemp':
                print(f"收到升温请求{new_temp}")
            elif action == 'decreaseTemp':
                print(f"收到降温请求{new_temp}")

            room = TestRoom()  # 限定房间

            # 调用调度器的温度变化方法
            scheduler.ChangeTemp(room.id, new_temp)



            return add_cors_headers(JsonResponse({'status': 'success'}))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def handle_power(request):
    """处理开关机请求"""
    global current_temp
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({'status': 'ok'}))

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            power_status = data.get('isOn')
            room = TestRoom()
            print(f"收到开关机请求，当前状态：{'开' if power_status else '关'}")
            if power_status:
                # 开机操作 - 使用全局变量 current_temp
                current_temp = get_current_temp()
                scheduler.schedule(room, 3, current_temp)  # 修改这里
            else:
                # 关机操作
                if room.id in air_conditioner_list:
                    air_conditioner = air_conditioner_list[room.id]
                    service_request.clear_request(room.id)
                    waiting_request.clear_request(room.id)
                    air_conditioner.power_off()

            
            return add_cors_headers(JsonResponse({'status': 'success'}))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def handle_fan_speed(request):
    """处理风速调节请求"""
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({'status': 'ok'}))
    
    if request.method == "POST":
        try:
            
            data = json.loads(request.body)
            speed = data.get('fanSpeed')
            room = TestRoom()
            print(f"收到调节风速请求，目标风速：{speed}")
            # 调用调度器的风速调节方法
            scheduler.ChangeWind(room.id, speed)
            
            
            return add_cors_headers(JsonResponse({'status': 'success'}))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)


