# src/utils/geo_utils.py
import numpy as np
from math import radians, cos, sin, asin, sqrt, atan2, degrees

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Args:
        lat1, lon1: Latitude and longitude of point 1
        lat2, lon2: Latitude and longitude of point 2
        
    Returns:
        float: Distance in nautical miles
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in nautical miles
    r = 3440.0
    
    # Return distance in nautical miles
    return c * r

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the bearing between two points
    
    Args:
        lat1, lon1: Latitude and longitude of point 1
        lat2, lon2: Latitude and longitude of point 2
        
    Returns:
        float: Bearing in degrees (0-360)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Calculate bearing
    dlon = lon2 - lon1
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    bearing = atan2(y, x)
    
    # Convert to degrees
    bearing = degrees(bearing)
    
    # Normalize to 0-360
    bearing = (bearing + 360) % 360
    
    return bearing

def calculate_cpa(lat1, lon1, course1, speed1, lat2, lon2, course2, speed2):
    """
    Calculate the Closest Point of Approach (CPA) between two vessels
    
    Args:
        lat1, lon1: Position of vessel 1
        course1, speed1: Course (degrees) and speed (knots) of vessel 1
        lat2, lon2: Position of vessel 2
        course2, speed2: Course (degrees) and speed (knots) of vessel 2
        
    Returns:
        tuple: (distance at CPA in nm, time to CPA in hours)
    """
    # Convert to radians
    course1_rad = radians(course1)
    course2_rad = radians(course2)
    
    # Calculate velocity components (nm/hour)
    v1x = speed1 * sin(course1_rad)
    v1y = speed1 * cos(course1_rad)
    
    v2x = speed2 * sin(course2_rad)
    v2y = speed2 * cos(course2_rad)
    
    # Approximate positions to Cartesian
    nm_per_lat = 60.0  # 1 degree latitude = 60 nm
    nm_per_lon = 60.0 * cos(radians((lat1 + lat2) / 2))  # Approximate at average latitude
    
    # Convert positions to NM
    x1 = 0
    y1 = 0
    x2 = (lon2 - lon1) * nm_per_lon
    y2 = (lat2 - lat1) * nm_per_lat
    
    # Relative velocity
    vrx = v2x - v1x
    vry = v2y - v1y
    
    # Relative position
    rx = x2 - x1
    ry = y2 - y1
    
    # Time to CPA
    dot_product = rx * vrx + ry * vry
    v_square = vrx**2 + vry**2
    
    if v_square < 0.0001:  # Nearly stationary relative motion
        tcpa = 0
    else:
        tcpa = -dot_product / v_square
    
    # If tcpa is negative, vessels are moving apart
    if tcpa < 0:
        tcpa = 0
    
    # Distance at CPA
    dcp_x = rx + tcpa * vrx
    dcp_y = ry + tcpa * vry
    dcpa = sqrt(dcp_x**2 + dcp_y**2)
    
    return (dcpa, tcpa)