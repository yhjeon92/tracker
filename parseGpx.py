import xml.etree.ElementTree as ET
from datetime import datetime as dt
from google.protobuf.timestamp_pb2 import Timestamp
import math
import getopt
import json
import sys

import gpx_pb2 as pb2


def haversine(coord1: object, coord2: object):
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 6)

    return meters


def get_distance(coord1: object, coord2: object):
    lat1, lon1, ele1 = coord1
    lat2, lon2, ele2 = coord2

    baseline = haversine((lat1, lon1), (lat2, lon2))
    height = abs(ele2 - ele1)
    dist = math.sqrt(baseline ** 2 + (ele2 - ele1) ** 2)
    dist = round(dist, 6)

    return dist


def elem_to_coord(element: ET.Element):
    latitude = float(element.get('lat'))
    longitude = float(element.get('lon'))
    elevation = float(element[0].text)
    time = element[1].text

    return latitude, longitude, elevation


def parse_data_js(times: list, dist_list: list, velocities: list, elevation_list: list):
    parsed = """var timestamp = {a};
var distance = {b};
var velocity = {c};
var elevation = {d};""".format(a=json.dumps(times, default=str), b=json.dumps(dist_list), c=json.dumps(velocities), d=json.dumps(elevation_list))

    return parsed


def parse_trail_js(latitude: list, longitude: list, kilometer_stone: list):
    if len(latitude) != len(longitude):
        print("Two arguments must be lists of same length!")
        return ""

    coordinate_list = list()
    for ind in range(len(latitude)):
        coordinate_list.append([longitude[ind], latitude[ind]])

    feature_list = list()
    trail_obj = {'type': 'Feature', 'id': 1, 'properties': {'underConstruction': False},
                 'geometry': {'type': 'LineString', 'coordinates': coordinate_list}}

    feature_list.append(trail_obj)

    for ind in range(len(kilometer_stone)):
        single_obj = {'type': 'Feature', 'id': ind + 2, 'properties': {'popupContent': f'{ind+1} km'},
                      'geometry': {'type': 'Point', 'coordinates': [kilometer_stone[ind][0], kilometer_stone[ind][1]]}}
        feature_list.append(single_obj)

    result = {"type": "FeatureCollection", 'features': feature_list}

    return "var trail = " + json.dumps(result) + ";"


def parse_points_js(pb2_point_list: list) -> str:
    feature_list = list()
    for ind in range(len(pb2_point_list)):
        pb2_point = pb2_point_list[ind]
        time_string = pb2_point.time.ToJsonString().split("T")[1].split("Z")[0]
        feature_list.append({'type': 'Feature', 'id': ind+1,
                             'properties': {'popupContent': time_string},
                             'geometry': {'type': 'Point', 'coordinates': [pb2_point.longitude, pb2_point.latitude]}})

    result = {'type': 'FeatureCollection', 'features': feature_list}

    return "var points = " + json.dumps(result) + ";"


def get_elevation(element: ET.Element):
    return float(element[0].text)


def get_time(element: ET.Element):
    try:
        dt_parsed = dt.strptime(element[1].text, '%Y-%m-%dT%H:%M:%S')
    except:
        try:
            dt_parsed = dt.strptime(element[1].text, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return None

    return dt_parsed


def parse_argv(argv):
    try:
        opts, args = getopt.getopt(argv, "o:", ["output="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-o':
            return arg

    return ""


class GpxParser:
    def __init__(self):
        pass

    def parse(self, text: str, output_js_path: str):
        tree = ET.ElementTree(ET.fromstring(text))

        root = tree.getroot()

        for elem in root.iter():
            if elem.tag.strip().endswith('trk'):
                trk = elem
                break

        if not 'trk' in locals():
            print("Ill-formatted gpx file: failed to find element with tag 'trk'")
            return

        for elem in trk.iter():
            if elem.tag.strip().endswith('trkseg'):
                data = elem
                break

        if not 'data' in locals():
            print("Ill-formatted gpx file: failed to find element with tag 'trkseg'")
            return

        lats = list()
        lons = list()

        for point in data:
            coordinates = elem_to_coord(point)
            lats.append(coordinates[0])
            lons.append(coordinates[1])

        velocity = list()
        timestamps = list()
        elevations = list()
        ## in km
        dist_covered = list()
        ## in m
        total_dist = 0
        dist_margin = 0

        kilometer_stone = list()
        ## in second
        total_seconds = 0
        elevation_gained = float(0.0)
        point_list = list()

        for i in range(1, len(data)):
            timedelta = get_time(data[i]) - get_time(data[i - 1])
            start = elem_to_coord(data[i - 1])
            end = elem_to_coord(data[i])
            dist = get_distance(end, start)

            if not dist > 100:
                total_dist += dist
                dist_margin += dist
                total_seconds += timedelta.seconds
                velocity.append(3.6 * dist / timedelta.seconds)
                timestamps.append(get_time(data[i]))
                elevations.append(get_elevation(data[i]))
                dist_covered.append(round(total_dist / 1000, 2))
                if len(elevations) > 1 and elevations[-1] > elevations[-2]:
                    elevation_gained += (elevations[-1] - elevations[-2])
                single_point = pb2.Point()
                pb_dt = Timestamp()
                pb_dt.FromDatetime(get_time(data[i]))
                single_point.time.CopyFrom(pb_dt)
                single_point.latitude = end[0]
                single_point.longitude = end[1]
                single_point.elevation = end[2]
                single_point.speed = dist / timedelta.seconds
                single_point.distance = dist
                point_list.append(single_point)

            if dist_margin > 1000:
                dist_margin = dist_margin - 1000
                r = (dist - dist_margin) / dist
                x_1 = start[1]
                x_2 = end[1]
                y_1 = start[0]
                y_2 = end[0]
                x = x_1 + r * (x_2 - x_1)
                y = y_1 + r * (y_2 - y_1)
                kilometer_stone.append([x, y])

        max_vel = max(velocity)

        print(f'Total distance covered: {round(total_dist)} m')
        print(f'Total elapsed time(s): {total_seconds} s')
        print(f'\tAverage speed (km/h): {round(3.6 * total_dist / total_seconds, 1)}')
        print(f'\tMaximum speed (km/h): {round(max_vel, 1)}')
        print(f'\tTotal elevation (m): {round(elevation_gained, 1)}')

        result = pb2.Workout()
        result.data.extend(point_list)
        result.name = "MyWorkout"
        pb_dt2 = Timestamp()
        pb_dt2.FromDatetime(timestamps[-1])
        result.time.CopyFrom(pb_dt2)
        result.elapsed = total_seconds
        result.total_distance = int(round(total_dist, 0))

        ## Write proto binaries
        # f = open('C:\\Users\\DST02\\Documents\\workout1_proto.txt', 'wb')
        # f.write(result.SerializeToString())
        # f.close()

        ## Write json objects to render graphs
        f = open(output_js_path, 'wb')
        date = timestamps[0].strftime('%A, %B %d, %Y')
        f.write(bytes(
            f'var titleString = "Workout on {date}";\n\n' +
            f'{parse_data_js(timestamps, dist_covered, velocity, elevations)}\n\n' +
            f'{parse_trail_js(lats, lons, kilometer_stone)}\n\n' +
            f'{parse_points_js(point_list)}\n\n' +
            'redrawMap();\n\nredrawMarker();\n\n' +
            'redrawMap();\n\nredrawMarker();\n\n' +
            'document.getElementById("plotAxisToggle").click();\n\n' +
            'document.getElementById("plotAxisToggle").click();', encoding='utf-8'))
        f.close()


