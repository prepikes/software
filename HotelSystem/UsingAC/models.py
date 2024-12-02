from django.db import models
from datetime import datetime,timedelta
import threading
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
current_temp = 25.0
def get_current_temp():
    global current_temp
    return current_temp
# 房间类，表示酒店中的一个房间
class Room(models.Model):
    room_id = models.IntegerField(unique=True)
    id = models.AutoField(primary_key=True)  # 自动生成房间ID
    room_number = models.CharField(max_length=10)  # 房间号
    target_temp = models.FloatField(null=True)  # 目标温度
    fan_speed = models.IntegerField(null=True)  # 风速

# 在文件开头添加全局变量
air_conditioner_list = {}  # 使用字典存储，key是room_id，value是AirConditioner实例

# 空调类，表示房间内的空调设备
class AirConditioner:
    def __init__(self, room, target_temp=25.0, fan_speed=1):
        self.room = room
        self.target_temp = target_temp
        self.fan_speed = fan_speed
        self.service_time = 0
        self.is_on = False
        self.current_temp = target_temp  # 将当前温度设置为目标温度
        self.active = False
        self.AC_id = room.id  # 使用 room.id 作为 AC_id
        # 创建实例时自动添加到全局列表
        air_conditioner_list[room.id] = self
        print(f"空调创建 - 房间号：{self.room.room_number}, 当前温度：{self.current_temp}°C, 目标温度：{self.target_temp}°C")

    def set_target_temp(self, target_temp):
        self.target_temp = target_temp

    def set_fan_speed(self, fan_speed):
        self.fan_speed = fan_speed

    def turn_on(self):
        """开机操作"""
        if not self.is_on:
            self.is_on = True
            self.active = True
            print(f"空调开启，房间号：{self.room.room_number}")

    def power_off(self):
        """关机操作"""
        if self.is_on:
            self.is_on = False
            self.active = False
            # 关机时从全局列表中移除
            if self.room.id in air_conditioner_list:
                del air_conditioner_list[self.room.id]
            print(f"空调关闭，房间号：{self.room.room_number}")

    def get_current_fee(self):
        """计算当前费用"""
        return 0.1 * (self.target_temp - self.current_temp)

    def get_total_fee(self):
        """计算总费用"""
        return self.get_current_fee() * 10

    def create_detailed_list(self, start_time, end_time, mode):
        """创建详单"""
        detailed_list = DetailedList.objects.create(
            start_time=start_time,
            end_time=end_time,
            mode=mode,
            target_temp=self.target_temp,
            fan_speed=self.fan_speed,
            rate=0.5,
            fee=self.get_current_fee(),
            room=self.room.id
        )
        return detailed_list

# 详单类，记录每次空调服务的详情
class DetailedList(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)  # 服务开始时间
    end_time = models.DateTimeField(null=True)  # 服务结束时间
    target_temp = models.FloatField()  # 目标温度
    mode = models.CharField(max_length=20)  # 空调模式
    fan_speed = models.IntegerField()  # 风速
    rate = models.FloatField()  # 费率
    fee = models.FloatField()  # 费用
    room = models.IntegerField(default=1)  # 房间号

class ServiceQueue:
    @staticmethod
    def add_request(room_id, ac_id, fan_speed, service_duration):
        """添加服务请求到服务队列"""
        service_obj = {
            "room_id": room_id,
            "ac_id": ac_id,
            "fan_speed": fan_speed,
            "service_duration": service_duration,
            "timer": None  # 计时器
        }
        global service_queue  # 使用全局变量
        service_queue.append(service_obj)

        # 创建计时器
        timer = Timer(service_obj, service_duration)
        service_obj["timer"] = timer
        timer.start()

    @staticmethod
    def remove_request(room_id):
        """从服务队列中移除请求"""
        global service_queue
        service_queue = [sq for sq in service_queue if sq["room_id"] != room_id]

    @staticmethod
    def contains(room_id):
        """检查房间是否在服务队列中"""
        global service_queue  # 使用全局变量
        return any(sq["room_id"] == room_id for sq in service_queue)

    @staticmethod
    def get_service_object(room_id):
        """获取房间对应的服务对象"""
        global service_queue  # 使用全局变量
        for sq in service_queue:
            if sq["room_id"] == room_id:
                return sq
        return None

    @staticmethod
    def clear_request(room_id):
        """清除服务请求并终止定时器"""
        service_obj = ServiceQueue.get_service_object(room_id)
        if service_obj and service_obj["timer"]:
            service_obj["timer"].stop_and_clear()
        ServiceQueue.remove_request(room_id)
        print(f"房间 {room_id} 的服务请求已清除")

class WaitingQueue:
    def __init__(self):
        self.room_id = 1003  # 默认房间号
        self.fan_speed = 1  # 风速
        self.service_duration = 120  # 服务时长（秒），默认2分钟

    @staticmethod
    def add_request(room_id, fan_speed,service_duration):
        """添加等待请求到等待队列"""
        wait_obj = WaitingQueue()
        wait_obj.room_id = room_id
        wait_obj.fan_speed = fan_speed
        wait_obj.service_duration = service_duration
        waiting_queue.append(wait_obj)

    @staticmethod
    def remove_request(room_id):
        """从等待队列中移除请求"""
        global waiting_queue
        waiting_queue = [wq for wq in waiting_queue if wq.room_id != room_id]

    @staticmethod
    def contains(room_id):
        """检查房间是否在等待队列中"""
        return any(wq.room_id == room_id for wq in waiting_queue)

    @staticmethod
    def update_fan_speed(room_id, fan_speed):
        """更新等待队列中的风速"""
        for wq in waiting_queue:
            if wq.room_id == room_id:
                wq.fan_speed = fan_speed
                break

    @staticmethod
    def clear_request(room_id):
        """清除等待请求"""
        if WaitingQueue.contains(room_id):
            WaitingQueue.remove_request(room_id)
            print(f"房间 {room_id} 的等待请求已清除")

# 创建全局队列（列表）
service_queue = []  # 服务队列列表
waiting_queue = []  # 等待队列列表
service_request = ServiceQueue()
waiting_request = WaitingQueue()
# 调度器类，负责调度服务请求
class Scheduler:
    global current_temp
    def __init__(self):
        self.max_service_objects = 3  # 服务对象上限

    def schedule(self, room, fan_speed, target_temp):
        # 检查房间是否已经在服务队列中
        print("----schedule开始----")
        if ServiceQueue.contains(room.id):
            print(f"服务队列：{service_queue}")
            print(f"房间 {room.id} 已经在服务中")
            print("----schedule结束----")
            return

        # 检查服务队列长度
        if len(service_queue) < self.max_service_objects:
            # 服务对象数小于上限，直接分配服务对象
            self.assign_service_object(room, fan_speed, target_temp)
        else:
            # 服务对象数达到上限，添加到等待队列
            print(f"服务对象数已达上限，房间 {room.id} 将被添加到等待队列")
            if not waiting_request.contains(room.id):
                waiting_request.add_request(room.id, fan_speed, 2)  # 120秒的默认服务时间
                print(f"房间 {room.id} 已添加到等待队列")
        print("----schedule结束----")

    def calculate_time(self, current_temp_, target_temp, fan_speed):
        """计算达到目标温度所需时间（分钟）"""
        temp_diff = abs(target_temp - current_temp_)
        
        # 根据风速确定温度变化率（度/分钟）
        if fan_speed == 3:  # 高风速
            rate = 1.0
        elif fan_speed == 2:  # 中风速
            rate = 0.5
        else:  # 低风速
            rate = 1/3
            
        time_needed = temp_diff / rate  # 计算所需分钟数
        print(f"达到目标温度需要 {time_needed:.2f} 分钟")
        time_needed = time_needed / 40
        # 保底3秒（转换为分钟）
        min_time = 3/60  # 3秒 = 0.05分钟
        return max(time_needed, min_time)  # 返回计算时间和最小时间中的较大值

    def assign_service_object(self, room, fan_speed, target_temp):
        """分配服务对象"""
        global current_temp  # 添加全局变量声明
        
        print("----assign_service_object开始----")
        if room.id in air_conditioner_list:
            air_conditioner = air_conditioner_list[room.id]
            
            print(f"当前房间温度：{current_temp}")
            print(f"当前房间风速：{air_conditioner.fan_speed}")
            print(f"目标温度：{target_temp}")
            print(f"目标风速：{fan_speed}")
            time_needed = self.calculate_time(current_temp, target_temp, air_conditioner.fan_speed)
            
            # 再更新空调状态
            air_conditioner.target_temp = target_temp
            air_conditioner.fan_speed = fan_speed
            air_conditioner.is_on = True
            air_conditioner.active = True
            
            # 更新服务队列
            if not service_request.contains(room.id):
                service_request.add_request(room.id, room.id, fan_speed, time_needed)
                
            # 创建新的详单
            detailed_list = air_conditioner.create_detailed_list(
                datetime.now(), 
                datetime.now()+timedelta(minutes=time_needed), 
                "温度调节"
            )
        else:
            # 创建新的空调实例
            air_conditioner = AirConditioner(
                room=room,
                target_temp=target_temp,
                fan_speed=fan_speed
            )
            air_conditioner.is_on = True
            air_conditioner.active = True

            # 更新服务队列，使用1秒作为开机时间
            if not service_request.contains(room.id):
                service_request.add_request(room.id, room.id, fan_speed, 1/60)  # 1秒 = 1/60分钟
            
            # 创建新的详单
            detailed_list = air_conditioner.create_detailed_list(
                datetime.now(), 
                datetime.now()+timedelta(seconds=1),  # 使用1秒
                "开机"
            )

            print(f"房间 {room.id} 被分配了一个服务对象")
            print(f"服务对象ID：{air_conditioner.AC_id}")
            print(f"服务对象目标风速：{air_conditioner.fan_speed}")
            print(f"服务对象目标温度：{air_conditioner.target_temp}")
        print(f"详单id：{detailed_list.id}")
        print(f"详单开始时间：{detailed_list.start_time}")
        print("----assign_service_object结束----")
    def ChangeTemp(self, room_id, target_temp):
        """改变温度"""
        # 检查房间是否有空调实例
        if room_id in air_conditioner_list:
            # 调用 schedule 函数
            room = Room.objects.get(id=room_id)
            air_conditioner = air_conditioner_list[room_id]
            self.schedule(room, air_conditioner.fan_speed, target_temp)
            return True
            
        else:
            print(f"房间 {room_id} 没有空调实例")
            return True
            
        return False
    
    def ChangeWind(self, room_id, fan_speed):
        """改变风速"""
        # 检查房间是否有空调实例
        if room_id in air_conditioner_list:
            # 获取空调实例和房间
            air_conditioner = air_conditioner_list[room_id]
            room = Room.objects.get(id=room_id)
            
            # 先计算达到目标温度所需时间
            current_temp = air_conditioner.current_temp
            target_temp = air_conditioner.target_temp
            print(f"三秒后，风速将变为 {fan_speed}")
            
            # 调用 schedule 函数
            self.schedule(room, fan_speed, target_temp)
            return True
            
        else:
            print(f"房间 {room_id} 没有空调实例")
            return True
            
        return False

class Timer:
    global current_temp
    def __init__(self, service_obj, duration_minutes=2):
        self.service_obj = service_obj  # 服务对象
        self.duration_minutes = duration_minutes  # 时间片时长（分钟）
        self.timer = None  # 用于存储定时器对象


    def start(self):
        """启动计时器"""
        self.timer = threading.Timer(self.duration_minutes * 60, self._on_time_up)  # 转换秒
        self.timer.start()

    def cancel(self):
        """取消计时器"""
        if self.timer:
            self.timer.cancel()

    def _on_time_up(self):
        global current_temp
        """时间到达后触发的回调函数"""
        print("----_on_time_up开始----")
        print(f"时间到达！请求超时，房间号{self.service_obj['room_id']}")
        # 从服务队列中移除该请求
        air_conditioner = air_conditioner_list[self.service_obj["room_id"]]
        ServiceQueue.remove_request(self.service_obj["room_id"])
        # 记录服务结束
        detailed_list = DetailedList.objects.filter(
            room=self.service_obj["room_id"]
        ).last()
        if detailed_list:
            detailed_list.end_time = datetime.now()
            detailed_list.save()
        current_temp = air_conditioner.target_temp
        print(f"房间 {self.service_obj['room_id']} 的服务已完成，详单已更新")
        print(f"温度{air_conditioner.target_temp}")
        print("----_on_time_up结束----")

    def stop_and_clear(self):
        """终止定时器并打印信息"""
        if self.timer:
            self.timer.cancel()
            print(f"定时器已终止，房间号：{self.service_obj['room_id']}")
