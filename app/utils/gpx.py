"""Utility functions for processing GPX files."""

from __future__ import annotations

from typing import IO, Tuple

import gpxpy
from shapely.geometry import LineString


def process_gpx_file(file_obj: IO[str]) -> Tuple[str, float, int]:
    """Return geometry, distance in km and elevation gain from a GPX file.

    Args:
        file_obj: File-like object containing GPX data.

    Returns:
        A tuple of (WKT geometry string, distance in km, elevation gain in m).
    """

    gpx = gpxpy.parse(file_obj)

    points = []
    distance = 0.0
    elevation_gain = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(
                (
                    point.longitude,
                    point.latitude,
                )
                for point in segment.points
                if point.longitude is not None and point.latitude is not None
            )
            distance += segment.length_3d() or 0.0
            uphill, _ = segment.get_uphill_downhill()
            if uphill:
                elevation_gain += uphill

    if not points:
        raise ValueError("GPX file contains no track points")

    geometry = LineString(points).wkt
    distance_km = round(distance / 1000.0, 3)
    elevation_gain_m = int(round(elevation_gain))

    return geometry, distance_km, elevation_gain_m
