import xml.etree.ElementTree as ET
from datetime import datetime
import math
import getopt
import json
import sys


class Point:
    def __init__(self, time: datetime, longitude: float, latitude: float, elevation: float):
        self.time = time
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation


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


def get_distance_tuple(coord1: object, coord2: object):
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

    return longitude, latitude, elevation


def parse_data_js(times: list, dist_list: list, velocities: list, elevation_list: list):
    parsed = """var timestamp = {a};
var distance = {b};
var velocity = {c};
var elevation = {d};""".format(a=json.dumps(times, default=str), b=json.dumps(dist_list), c=json.dumps(velocities),
                               d=json.dumps(elevation_list))

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
        single_obj = {'type': 'Feature', 'id': ind + 2, 'properties': {'popupContent': f'{ind + 1} km'},
                      'geometry': {'type': 'Point', 'coordinates': [kilometer_stone[ind][0], kilometer_stone[ind][1]]}}
        feature_list.append(single_obj)

    result = {"type": "FeatureCollection", 'features': feature_list}

    return result


def parse_trail_js_point(point_list: list, milestone: list):
    feature_list = list()
    trail_obj = {'type': 'Feature', 'id': 1, 'properties': {'underConstruction': False},
                 'geometry': {'type': 'LineString', 'coordinates':
                     [[point.longitude, point.latitude] for point in point_list]}}
    feature_list.append(trail_obj)

    for ind in range(len(milestone)):
        single_obj = {'type': 'Feature', 'id': ind + 2, 'properties': {'popupContent': f'{ind + 1} km'},
                      'geometry': {'type': 'Point', 'coordinates': [milestone[ind][0], milestone[ind][1]]}}
        feature_list.append(single_obj)

    result = {"type": "FeatureCollection", 'features': feature_list}

    return result


def parse_points_js(point_list: list):
    feature_list = list()
    for ind in range(len(point_list)):
        point = point_list[ind]
        # time_string = point.time.split("T")[1].split("Z")[0]
        time_string = point.time.strftime("%H:%M:%S")
        feature_list.append({'type': 'Feature', 'id': ind + 1,
                             'properties': {'popupContent': time_string},
                             'geometry': {'type': 'Point', 'coordinates': [point.longitude, point.latitude]}})

    result = {'type': 'FeatureCollection', 'features': feature_list}

    return result


def get_elevation(element: ET.Element):
    return float(element[0].text)


def get_time(element: ET.Element):
    try:
        dt_parsed = datetime.strptime(element[1].text, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        try:
            dt_parsed = datetime.strptime(element[1].text, '%Y-%m-%dT%H:%M:%S')
        except:
            try:
                dt_parsed = datetime.strptime(element[1].text, '%Y-%m-%dT%H:%M:%SZ')
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


def get_distance(point1: Point, point2: Point):
    baseline = haversine((point1.latitude, point1.longitude), (point2.latitude, point2.longitude))
    dist = math.sqrt(baseline ** 2 + (point2.elevation - point1.elevation) ** 2)
    dist = round(dist, 6)

    return dist


class GpxParser:
    def __init__(self):
        pass

    def parse(self, text: str, output_js_path: str):
        tree = ET.ElementTree(ET.fromstring(text))

        root = tree.getroot()

        for elem in root.iter():
            if elem.tag.strip().endswith('gpx'):
                gpx = elem
                break

        if not 'gpx' in locals():
            gpx = root

        for elem in gpx.iter():
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

        point_list = list()

        for gpx_point in data:
            coordinates = elem_to_coord(gpx_point)
            elev = get_elevation(gpx_point)
            timepoint = get_time(gpx_point)
            point_list.append(Point(timepoint, coordinates[0], coordinates[1], elev))

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
        moving_time = 0
        elevation_gained = float(0.0)

        for i in range(1, len(point_list)):
            timedelta = point_list[i].time - point_list[i - 1].time
            if timedelta.total_seconds() >= 20.0:
                print(point_list[i-1].time)
                print(point_list[i].time)
                print(timedelta.total_seconds())
                pass
            else:
                dist = get_distance(point_list[i], point_list[i - 1])
                timedelta_float = timedelta.seconds + 0.000001 * timedelta.microseconds

                total_dist += dist
                dist_margin += dist

                moving_time += timedelta_float
                velocity.append(3.6 * dist / timedelta_float)

                if velocity[-1] >= 90.0:
                    print("=================================")
                    print(point_list[i].time)
                    print(velocity[-1])
                    print(dist)
                    print(timedelta_float)
                    print(point_list[i].latitude)
                    print(point_list[i].longitude)
                    print(point_list[i-1].latitude)
                    print(point_list[i - 1].longitude)
                    print("=================================")

                timestamps.append(point_list[i].time)
                elevations.append(point_list[i].elevation)
                dist_covered.append(round(total_dist / 1000, 4))

                if len(elevations) > 1 and elevations[-1] > elevations[-2]:
                    elevation_gained += (elevations[-1] - elevations[-2])

                if dist_margin > 1000:
                    dist_margin = dist_margin - 1000
                    r = (dist - dist_margin) / dist
                    x_1 = point_list[i - 1].longitude
                    x_2 = point_list[i].longitude
                    y_1 = point_list[i - 1].latitude
                    y_2 = point_list[i].latitude
                    x = x_1 + r * (x_2 - x_1)
                    y = y_1 + r * (y_2 - y_1)
                    kilometer_stone.append([x, y])

        # for i in range(1, len(data)):
        #     timedelta = get_time(data[i]) - get_time(data[i - 1])
        #     start = elem_to_coord(data[i - 1])
        #     end = elem_to_coord(data[i])
        #     dist = get_distance_tuple(end, start)
        #
        #     if not dist > 100:
        #         total_dist += dist
        #         dist_margin += dist
        #         total_seconds += (timedelta.seconds + 0.000001 * timedelta.microseconds)
        #         velocity.append(3.6 * dist / (timedelta.seconds + 0.000001 * timedelta.microseconds))
        #         timestamps.append(get_time(data[i]))
        #         elevations.append(get_elevation(data[i]))
        #         dist_covered.append(round(total_dist / 1000, 4))
        #         if len(elevations) > 1 and elevations[-1] > elevations[-2]:
        #             elevation_gained += (elevations[-1] - elevations[-2])
        #
        #         single_point = Point(get_time(data[i]), )
        #         single_point = pb2.Point()
        #         single_point.time.CopyFrom(pb_dt)
        #         single_point.latitude = end[0]
        #         single_point.longitude = end[1]
        #         single_point.elevation = end[2]
        #         single_point.speed = dist / (timedelta.seconds + 0.000001 * timedelta.microseconds)
        #         single_point.distance = dist
        #         point_list.append(single_point)
        #
        #     if dist_margin > 1000:
        #         dist_margin = dist_margin - 1000
        #         r = (dist - dist_margin) / dist
        #         x_1 = start[1]
        #         x_2 = end[1]
        #         y_1 = start[0]
        #         y_2 = end[0]
        #         x = x_1 + r * (x_2 - x_1)
        #         y = y_1 + r * (y_2 - y_1)
        #         kilometer_stone.append([x, y])

        max_vel = max(velocity)
        max_elev = max(elevations)
        moving_time = int(moving_time)
        total_time = int((timestamps[-1] - timestamps[0]).total_seconds())

        print(f'Total distance covered: {round(total_dist)} m')
        print(f'Total elapsed time: {total_time} s')
        print(f'Actual moving time: {moving_time} s')
        print(f'\tAverage speed (km/h): {round(3.6 * total_dist / moving_time, 1)}')
        print(f'\tMaximum speed (km/h): {round(max_vel, 1)}')
        print(f'\tMaximum elevation (m): {round(max_elev, 1)}')
        print(f'\tTotal elevation gained (m): {round(elevation_gained, 1)}')

        trail_dict = parse_trail_js_point(point_list, kilometer_stone)
        point_dict = parse_points_js(point_list)

        ## Write json objects to render graphs
        f = open(output_js_path, 'wb')
        date = timestamps[0].strftime('%A, %B %d, %Y')
        f.write(bytes(
            f'var titleString = "Workout on {date}";\n\n' +
            f'{parse_data_js(timestamps, dist_covered, velocity, elevations)}\n\n' +
            f'var trail = {json.dumps(trail_dict)};\n\n' +
            # f'var trail = {json.dumps(parse_trail_js(lats, lons, kilometer_stone))};\n\n' +
            f'var points = {json.dumps(point_dict)};\n\n' +
            'redrawMap();\n\nredrawMarker();\n\n' +
            'redrawMap();\n\nredrawMarker();\n\n' +
            'document.getElementById("plotAxisToggle").click();\n\n' +
            'document.getElementById("plotAxisToggle").click();', encoding='utf-8'))
        f.close()

        result_dict = dict()
        result_dict['titleString'] = date
        result_dict['timestamp'] = list(map(lambda x: str(x), timestamps))
        result_dict['distance'] = dist_covered
        result_dict['velocity'] = velocity
        result_dict['elevation'] = elevations

        result_dict['trail'] = trail_dict
        result_dict['points'] = point_dict

        return result_dict
