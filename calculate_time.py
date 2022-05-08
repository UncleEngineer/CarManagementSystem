from datetime import datetime

def calculate_car_hour(dt='2022-05-08 12:27:18',first_hour=20,next_hour=10):
    # only hour and minute
    convert = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    delta = now - convert
    hour = delta.seconds // 3600
    minute = (delta.seconds % 3600) // 60
    print('Parking time: {} Hours {} minutes'.format(hour,minute))
    total = []
    if hour > 1:
        # ชั่วโมงแรก
        total.append(first_hour) # ชั่วโมงแรก 20
        total.append((hour - 1) * next_hour) # ชั่วโมงถัดไป
    elif hour == 1:
        total.append(first_hour)

    if minute > 15 and hour >= 1:
        total.append(next_hour)
    elif minute > 15 and hour == 0:
        total.append(first_hour)
    elif minute < 15:
        pass

    cal = sum(total)
    print('Car park fee: {} baht'.format(cal))

    
calculate_car_hour('2022-05-08 8:27:18')