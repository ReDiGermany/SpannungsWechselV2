# Notes

Start lidar: Startet über einen ROS2 Treiber.\
Basis: [Lslidar/Lslidar_ROS2_driver](https://github.com/Lslidar/Lslidar_ROS2_driver/tree/C16_V4.0)

```bash
$ cd Desktop/ && ./lidar.ros
```

## Usage

Wir nutzen ros2 topic echo zur wiedergabe von Nachrichten.\
Alternative Idee wäre, den Treiber umzuschreiben, um die Daten direkt auswerten zu können.\
Potentielle TODO für später!

```bash
usage: ros2 topic echo  [-h]
                        [--qos-profile {unknown,system_default,sensor_data,services_default,parameters,parameter_events,action_status_default}]
                        [--qos-depth N]
                        [--qos-history {system_default,keep_last,keep_all,unknown}]
                        [--qos-reliability {system_default,reliable,best_effort,unknown}]
                        [--qos-durability {system_default,transient_local,volatile,unknown}]
                        [--csv]
                        [--full-length]
                        [--truncate-length TRUNCATE_LENGTH]
                        [--no-arr]
                        [--no-str]
                        topic_name [message_type]
```

## Kommandos & Return

```bash
$ ros2 topic echo /c16/lslidar_point_cloud --csv --full-length --no-arr

> 1683053472,886221000,laser_link,1,15603,<sequence type: sensor_msgs/msg/PointField, length: 6>,False,32,499296,<sequence type: uint8, length: 499296>,True
```

Wenn man dann die Daten einsetzt, bekommt man z.B. das raus:
1683054031,89890000,laser_link,1,15676,x,0,7,1,y,4,7,1,z,8,7,1,intensity,16,7,1,ring,20,4,1,time,24,8,1,False,32,501632, ... , True

Die `<sequence type: sensor_msgs/msg/PointField, length: 6>` besteht also aus:
```
x,0,7,1,y,4,7,1,z,8,7,1,intensity,16,7,1,ring,20,4,1,time,24,8,1
```

[DOKUMENTATION] Raw Message Definition PointField:\
http://docs.ros.org/en/api/sensor_msgs/html/msg/PointField.html

Wenn man das Zerlegt, sieht man schnell, dass wir mehrere Felder haben:
```
1683054031,89890000,laser_link,1,15676,
    x,0,7,1,
    y,4,7,1,
    z,8,7,1,
    intensity,16,7,1,
    ring,20,4,1,
    time,24,8,1,
False,32,501632, ... , True
```

Übersetzt heißt das folgendes:
* Feld `x`: Offset = `0`; Datatype = `FLOAT32`; Count = `1`
* Feld `y`: Offset = `4`; Datatype = `FLOAT32`; Count = `1`
* Feld `z`: Offset = `8`; Datatype = `FLOAT32`; Count = `1`
* Feld `intensity`: Offset = `16`; Datatype = `FLOAT32`; Count = `1`
* Feld `ring`: Offset = `20`; Datatype = `UINT16`; Count = `1`
* Feld `time`: Offset = `24`; Datatype = `FLOAT64`; Count = `1`

Laut [diesem Beispiel](https://python.hotexamples.com/de/examples/sensor_msgs.msg/PointField/count/python-pointfield-count-method-examples.html) besteht der content dann aus folgenden Daten:

```python
points = []
for i in range(num_points):
    alpha = (clouds[i][0]/180.0) * math.pi
    lamda = (clouds[i][1]/180.0) * math.pi
    distance = clouds[i][2]
    intensity = clouds[i][3]
    #not for sure if coordinate is right
    zz = distance * math.sin(lamda)
    yy = distance * math.cos(lamda) * math.cos(alpha)
    xx = distance * math.cos(lamda) * math.cos(alpha)
    points.append([xx,yy,zz,intensity])
```

Bei 501.632 werten wären wir bei 501632/4 = 125.408 Datensätzen.

Um nachrichten zu loggen, einfach über folgendes kommando gehen:
$ ros2 topic echo /c16/lslidar_point_cloud --csv --full-length > ros.out.echo.lidar.log

usage: ros2 topic echo  [-h]
                        [--qos-profile {unknown,system_default,sensor_data,services_default,parameters,parameter_events,action_status_default}]
                        [--qos-depth N]
                        [--qos-history {system_default,keep_last,keep_all,unknown}]
                        [--qos-reliability {system_default,reliable,best_effort,unknown}]
                        [--qos-durability {system_default,transient_local,volatile,unknown}]
                        [--csv]
                        [--full-length]
                        [--truncate-length TRUNCATE_LENGTH]
                        [--no-arr]
                        [--no-str]
                        topic_name [message_type]
