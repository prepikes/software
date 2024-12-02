from django.db import models
from datetime import datetime

    
# 房间类，表示酒店中的一个房间
class Room(models.Model):
    room_id = models.IntegerField(unique=True)
    id = models.AutoField(primary_key=True)  # 自动生成房间ID
    room_number = models.CharField(max_length=10)  # 房间号
    target_temp = models.FloatField(null=True)  # 目标温度
    fan_speed = models.IntegerField(null=True)  # 风速

# 空调类，表示房间内的空调设备
class AirConditioner(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    target_temp = models.FloatField(default=25.0)
    fan_speed = models.IntegerField(default=1)
    service_time = models.FloatField(default=0)
    is_on = models.BooleanField(default=False)  # 表示空调是否开机
    current_temp = models.FloatField(default=25.0)
    active = models.BooleanField(default=False)  # 是否正在工作

    def set_target_temp(self, target_temp):
        self.target_temp = target_temp

    def set_fan_speed(self, fan_speed):
        self.fan_speed = fan_speed

    def turn_on(self):
        """开机操作"""
        if not self.is_on:
            self.is_on = True  # 开启空调
            self.active = True  # 空调正在工作
            self.save()  # 保存更改
            print(f"空调开启，房间号：{self.room.room_number}")

    def turn_off(self):
        """关机操作"""
        if self.is_on:
            self.is_on = False  # 关闭空调
            self.active = False  # 空调不再工作
            self.save()  # 保存更改
            print(f"空调关闭，房间号：{self.room.room_number}")

    def get_current_fee(self):
        """计算当前费用"""
        return 0.1 * (self.target_temp - self.current_temp)  # 示例费用计算方式

    def get_total_fee(self):
        """计算总费用"""
        return self.get_current_fee() * 10  # 示例费用计算方式

# 详单类，记录每次空调服务的详情
class DetailedList(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)  # 服务开始时间
    end_time = models.DateTimeField(null=True)  # 服务结束时间
    mode = models.CharField(max_length=20)  # 空调模式
    target_temp = models.FloatField()  # 目标温度
    fan_speed = models.IntegerField()  # 风速
    rate = models.FloatField()  # 费率
    fee = models.FloatField()  # 费用
    air_conditioner = models.ForeignKey(AirConditioner, on_delete=models.CASCADE)  # 关联空调

# 账单类，记录每次入住的总费用
class Bill(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # 关联房间
    total_fee = models.FloatField()  # 总费用
    check_in = models.DateTimeField(auto_now_add=True)  # 入住时间
    check_out = models.DateTimeField(null=True)  # 退房时间

    def calculate_total_fee(self):
        # 计算总费用
        total_fee = 0
        for detailed in DetailedList.objects.filter(air_conditioner__room=self.room):
            total_fee += detailed.fee
        self.total_fee = total_fee
        self.save()

# 服务队列类，管理正在进行中的服务请求
class ServiceQueue:
    def __init__(self):
        self.queue = []

    def add_request(self, room, ac):
        self.queue.append((room, ac))

    def contains(self, room):
        return any(r == room for r, _ in self.queue)

    def get_service_object(self, room):
        for r, ac in self.queue:
            if r == room:
                return ac
        return None

# 等待队列类，管理等待服务的请求
class WaitingQueue:
    def __init__(self):
        self.queue = []

    def add_request(self, room):
        self.queue.append(room)

    def contains(self, room):
        return room in self.queue

    def update_target_temp(self, room, target_temp):
        for r in self.queue:
            if r == room:
                r.target_temp = target_temp
                break

    def update_fan_speed(self, room, fan_speed):
        for r in self.queue:
            if r == room:
                r.fan_speed = fan_speed
                break

# 服务对象类
class ServiceObject(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # 关联房间
    fan_speed = models.IntegerField()  # 风速
    target_temp = models.FloatField()  # 目标温度
    service_time = models.DateTimeField(auto_now_add=True)  # 服务开始时间

    def is_time_out(self, time_limit_minutes=2):
        # 判断服务是否超时
        current_time = timezone.now()
        if current_time - self.service_time > timedelta(minutes=time_limit_minutes):
            return True
        return False

# 调度器类，负责调度服务请求
class Scheduler:
    def __init__(self):
        # 服务队列和等待队列
        self.service_queue = []  # 当前服务的队列
        self.waiting_queue = []  # 等待队列
        self.max_service_objects = 3  # 服务对象上限

    def schedule(self, room, fan_speed, target_temp):
        # 查找空调对象
        air_conditioner = AirConditioner.objects.get(room=room)
        current_fan_speed = air_conditioner.fan_speed

        if len(self.service_queue) < self.max_service_objects:
            # 服务对象数小于上限，直接分配服务对象
            self.assign_service_object(room, fan_speed, target_temp)
        else:
            # 服务对象数达到上限，进行调度
            self.handle_priority_and_time_slice(room, fan_speed, target_temp)

    def assign_service_object(self, room, fan_speed, target_temp):
        # 创建服务对象并分配给房间
        service_obj = ServiceObject(room=room, fan_speed=fan_speed, target_temp=target_temp)
        self.service_queue.append(service_obj)
        print(f"房间 {room.id} 被分配了一个服务对象")

    def handle_priority_and_time_slice(self, room, fan_speed, target_temp):
        # 优先级调度：首先根据风速判断
        low_priority_objs = [obj for obj in self.service_queue if obj.fan_speed < fan_speed]

        if len(low_priority_objs) == 0:
            # 风速都不低于请求风速，使用时间片调度
            self.time_slice_schedule(room, fan_speed, target_temp)
        else:
            # 风速较低的服务对象处理
            self.priority_schedule(room, fan_speed, target_temp, low_priority_objs)

    def priority_schedule(self, room, fan_speed, target_temp, low_priority_objs):
        # 如果有风速较低的服务对象，进行优先级调度
        if len(low_priority_objs) == 1:
            # 只有一个风速低于请求风速的服务对象
            self.move_to_waiting_queue(low_priority_objs[0], room, fan_speed, target_temp)
        else:
            # 处理多个风速较低的对象
            max_service_time_obj = max(low_priority_objs, key=lambda obj: obj.service_time)
            self.move_to_waiting_queue(max_service_time_obj, room, fan_speed, target_temp)

    def time_slice_schedule(self, room, fan_speed, target_temp):
        # 时间片调度，优先级相同的情况下
        self.waiting_queue.append((room, fan_speed, target_temp))
        print(f"房间 {room.id} 被放置到等待队列，等待服务")

    def move_to_waiting_queue(self, service_obj, room, fan_speed, target_temp):
        # 将服务对象移到等待队列
        self.service_queue.remove(service_obj)
        self.waiting_queue.append((room, fan_speed, target_temp))
        print(f"服务对象 {service_obj.id} 被释放，房间 {room.id} 被放置到等待队列")

     # 打开空调
    def PowerOn(self, room_id, current_room_temp):
        room = Room.objects.get(id=room_id)
        if AirConditioner.objects.filter(room=room).count() < 3:
            ac = AirConditioner(room=room)
            ac.save()
            timer = Timer(ac)
            timer.save()
            detailed_list = DetailedList(
                start_time=datetime.now(),
                mode="Auto",  # 示例模式
                target_temp=current_room_temp,
                rate=0.1,  # 示例费率
                fee=0,
                air_conditioner=ac
            )
            detailed_list.save()
            self.service_queue.add_request(room, ac)
            return {"Mode": "Auto", "TargetTemp": current_room_temp, "CurrentFee": 0, "TotalFee": 0}
        return {"error": "Service object limit reached"}
     
     # 改变温度
    def ChangeTemp(self, room_id, target_temp):
        room = Room.objects.get(id=room_id)
        if self.service_queue.contains(room):
            ac = self.service_queue.get_service_object(room)
            ac.set_target_temp(target_temp)
            detailed_list = ac.get_detailed_list()
            detailed_list.target_temp = target_temp
            detailed_list.save()
            return True
        elif self.waiting_queue.contains(room):
            self.waiting_queue.update_target_temp(room, target_temp)
            return True
        return False

     # 改变风速
    def ChangeSpeed(self, room_id, fan_speed):
        room = Room.objects.get(id=room_id)
        if self.service_queue.contains(room):
            ac = self.service_queue.get_service_object(room)
            ac.set_fan_speed(fan_speed)
            detailed_list = ac.get_detailed_list()
            detailed_list.fan_speed = fan_speed
            detailed_list.save()
            return True
        elif self.waiting_queue.contains(room):
            self.waiting_queue.update_fan_speed(room, fan_speed)
            return True
        return False
     
     # 关闭空调
    def PowerOff(self, room_id):
        room = Room.objects.get(id=room_id)
        if self.service_queue.contains(room):
            ac = self.service_queue.get_service_object(room)
            ac.power_off()
            detailed_list = ac.get_detailed_list()
            detailed_list.end_time = datetime.now()
            detailed_list.save()
            return {"State": "Off", "CurrentFee": ac.get_current_fee(), "TotalFee": ac.get_total_fee()}
        return {"error": "No active service found"}
    
    
    def RequestState(self, room_id):
        room = Room.objects.get(id=room_id)
        if self.service_queue.contains(room):
            ac = self.service_queue.get_service_object(room)
            return {"CurrentFee": ac.get_current_fee(), "TotalFee": ac.get_total_fee()}
        return {"error": "No active service found"}
