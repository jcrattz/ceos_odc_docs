import folium
import itertools
import math
import numpy as np
import pandas as pd
from typing import List

def _degree_to_zoom_level(l1, l2, margin = 0.0):

    degree = abs(l1 - l2) * (1 + margin)
    zoom_level_int = 0
    if degree != 0:
        zoom_level_float = math.log(360/degree)/math.log(2)
        zoom_level_int = int(zoom_level_float)
    else:
        zoom_level_int = 18
    return zoom_level_int

def display_map(latitude = None, longitude = None, resolution = None):
    """
    Generates a Folium map with a latlon bounded rectangle drawn on it.

    Parameters
    ----------
    latitude: tuple
        A 2-tuple of latitude bounds (floats) in (min,max) format.
    longitude: tuple
        A 2-tuple of longitude bounds (floats) in (min,max) format.
    resolution: tuple
        A 2-tuple of floats in (lat,lon) format used to draw a grid on your map. 
        Values denote spacing of latitude and longitude lines.  
        Gridding starts at the top left corner. 
        By default, displays no grid.

    Returns
    -------
    map: folium.Map
        A map centered on the lat lon bounds. 
        A rectangle is drawn on this map detailing the 
        perimeter of the lat,lon bounds. 
        A zoom level is calculated such that the resulting 
        viewport is the closest it can possibly get to the 
        centered bounding rectangle without clipping it. 
        An optional grid can be overlaid with primitive interpolation.
    """

    assert latitude is not None
    assert longitude is not None

    ###### ###### ######   CALC ZOOM LEVEL     ###### ###### ######

    margin = -0.5
    zoom_bias = 0

    lat_zoom_level = _degree_to_zoom_level(margin = margin, *latitude ) + zoom_bias
    lon_zoom_level = _degree_to_zoom_level(margin = margin, *longitude) + zoom_bias
    zoom_level = min(lat_zoom_level, lon_zoom_level)

    ###### ###### ######   CENTER POINT        ###### ###### ######

    center = [np.mean(latitude), np.mean(longitude)]

    ###### ###### ######   CREATE MAP         ###### ###### ######

    map_hybrid = folium.Map(
        tiles=None,
        location=center,
        zoom_start=zoom_level,
    )
    feat_group = folium.FeatureGroup(name='ESRI World Imagery',
                                     overlay=False)
    feat_group.add_child(folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/'
                                                'services/World_Imagery/MapServer/'
                                                'tile/{z}/{y}/{x}',
                                          attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, '
                                               'USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, '
                                               'IGN, IGP, UPR-EGP, and the GIS User Community',
                                          name='ESRI World Imagery'))
    feat_group.add_child(folium.TileLayer(tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/'
                                                'toner-labels/{z}/{x}/{y}{r}.png',
                                          attr='Map tiles by <a href="http://stamen.com">'
                                               'Stamen Design</a>, <a href="http://'
                                               'creativecommons.org/licenses/by/3.0">CC BY 3.0'
                                               '</a> &mdash; Map data &copy; <a href="https://'
                                               'www.openstreetmap.org/copyright">'
                                               'OpenStreetMap</a> contributors',
                                          subdomains='abcd',
                                          min_zoom=0,
                                          max_zoom=20))
    feat_group.add_child(folium.TileLayer(tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/'
                                                'toner-lines/{z}/{x}/{y}{r}.png',
                                          attr='Map tiles by <a href="http://stamen.com">'
                                               'Stamen Design</a>, <a href="http://'
                                               'creativecommons.org/licenses/by/3.0">CC BY 3.0'
                                               '</a> &mdash; Map data &copy; <a href="https://'
                                               'www.openstreetmap.org/copyright">'
                                               'OpenStreetMap</a> contributors',
                                          subdomains='abcd',
                                          min_zoom=0,
                                          max_zoom=20,
                                          opacity=0.4))
    map_hybrid.add_child(feat_group)

    ###### ###### ######   RESOLUTION GRID    ###### ###### ######

    if resolution is not None:
        res_lat, res_lon = resolution

        lats = np.arange(*latitude, abs(res_lat))
        lons = np.arange(*longitude, abs(res_lon))

        vertical_grid   = map(lambda x :([x[0][0],x[1]],[x[0][1],x[1]]),itertools.product([latitude],lons))
        horizontal_grid = map(lambda x :([x[1],x[0][0]],[x[1],x[0][1]]),itertools.product([longitude],lats))

        for segment in vertical_grid:
            folium.features.PolyLine(segment, color = 'white', opacity = 0.3).add_to(map_hybrid)

        for segment in horizontal_grid:
            folium.features.PolyLine(segment, color = 'white', opacity = 0.3).add_to(map_hybrid)

    ###### ###### ######     BOUNDING BOX     ###### ###### ######

    line_segments = [(latitude[0],longitude[0]),
                     (latitude[0],longitude[1]),
                     (latitude[1],longitude[1]),
                     (latitude[1],longitude[0]),
                     (latitude[0],longitude[0])
                    ]



    map_hybrid.add_child(
        folium.features.PolyLine(
            locations=line_segments,
            color='red',
            opacity=0.8)
    )

    map_hybrid.add_child(folium.features.LatLngPopup())

    return map_hybrid


def generate_n_visually_distinct_colors(n: int) -> List[str]:
    colors = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
              "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
              "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
              "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
              "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
              "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
              "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
              "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

              "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
              "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
              "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
              "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
              "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
              "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
              "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
              "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58"]

    if n > len(colors):
        raise Exception("Can not generate more than {} distinct colors.".format(str(len(colors))))
    return colors[:n]


def display_grouped_pandas_rows_as_pins(data_frame: pd.DataFrame,
                                        group_name: str = "LandUse",
                                        folium_map=None) -> folium.Map:
    '''Groups pandas rows by values in a selected column and renders them as annotated circles on a folium.Map'''
    group_column_name = group_name

    center = (data_frame.Latitude.mean(),
              data_frame.Longitude.mean())

    zoom_level = _degree_to_zoom_level(data_frame.Latitude.min(),
                                       data_frame.Latitude.max())

    labels = list(pd.unique(data_frame[group_column_name]))
    pallete = generate_n_visually_distinct_colors(n=len(labels))

    colors = {_label: _color for _label, _color in zip(labels, pallete)}

    m = folium_map
    if m == None:
        m = folium.Map(
            tiles=None,
            location=center,
            zoom_start=zoom_level
            )
        f = folium.FeatureGroup(name='ESRI World Imagery',
                                overlay=False)
        f.add_child(folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/'
                                           'World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                     attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, '
                                          'USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, '
                                          'IGP, UPR-EGP, and the GIS User Community',
                                     name='ESRI World Imagery'))
        f.add_child(folium.TileLayer(tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-labels/'
                                           '{z}/{x}/{y}{r}.png',
                                     attr='Map tiles by <a href="http://stamen.com">'
                                          'Stamen Design</a>, <a href="http://creativecommons.org/'
                                          'licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; '
                                          '<a href="https://www.openstreetmap.org/copyright">'
                                          'OpenStreetMap</a> contributors',
                                     subdomains='abcd',
                                     min_zoom=0,
                                     max_zoom=20))
        f.add_child(folium.TileLayer(tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/'
                                           '{z}/{x}/{y}{r}.png',
                                     attr='Map tiles by <a href="http://stamen.com">'
                                          'Stamen Design</a>, <a href="http://creativecommons.org/'
                                          'licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; '
                                          '<a href="https://www.openstreetmap.org/copyright">'
                                          'OpenStreetMap</a> contributors',
                                     subdomains='abcd',
                                     min_zoom=0,
                                     max_zoom=20,
                                     opacity=0.4))
        m.add_child(f)

    for i in range(0, len(data_frame)):
        land_cover = data_frame.iloc[i][group_column_name]
        index = labels.index(land_cover)
        _color = colors[land_cover]

        folium.vector_layers.CircleMarker(
            location=[data_frame.iloc[i]['Latitude'], data_frame.iloc[i]['Longitude']],
            radius=5,
            popup=land_cover,
            color=_color,
            fill=True,
            fill_color=_color
        ).add_to(m)

    m.add_child(folium.features.LatLngPopup())
    return m
