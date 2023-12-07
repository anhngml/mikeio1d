import pytest
import random

import shapely

from mikeio1d.result_network.geometry import geometry_from_node
from mikeio1d.result_network.geometry import geometry_from_catchment
from mikeio1d.result_network.geometry import ReachGeometry
from mikeio1d.result_network.geometry import ReachPoint
from mikeio1d.result_network.geometry import ReachPointType


class TestReachPoint:
    def test_reach_point_basic(self):
        p1 = ReachPoint(ReachPointType.DIGIPOINT, 0, 0, 0, 0)
        p2 = ReachPoint(ReachPointType.GRIDPOINT, 0, 0, 0, 0)
        p3 = ReachPoint(ReachPointType.GRIDPOINT, 10, 0, 0, 0)
        assert p1 == p2, "Should be equal if chainage and coordinates are equal"
        assert p3 > p1, "Should be greater if chainage is greater"
        assert p1 < p3, "Should be less if chainage is less"
        points = [p3, p1, p2]
        assert sorted(points) == [p1, p2, p3], "Should sort by chainage."
        assert sorted(list(set(points))) == [p1, p3], "Should remove duplicates."

    def test_reach_point_to_shapely(self):
        p = ReachPoint(ReachPointType.DIGIPOINT, 0, 0, 0, 0)
        g = p.to_shapely()
        assert isinstance(g, shapely.Point)
        assert g.x == 0
        assert g.y == 0


class TestReachGeometry:
    @pytest.fixture
    def reach_geometry(self):
        points = [
            ReachPoint(ReachPointType.DIGIPOINT, 0, 0, 0, 0),
            ReachPoint(ReachPointType.GRIDPOINT, 0, 0, 0, 0),
            ReachPoint(ReachPointType.GRIDPOINT, 5, 0.5, 0.5, 0.5),
            ReachPoint(ReachPointType.GRIDPOINT, 10, 1, 1, 1),
            ReachPoint(ReachPointType.DIGIPOINT, 10, 1, 1, 1),
        ]
        random.shuffle(points)
        return ReachGeometry(points)

    def test_reach_geometry_basic(self, reach_geometry):
        assert len(reach_geometry.points) == 5
        assert len(reach_geometry.digipoints) == 2
        assert len(reach_geometry.gridpoints) == 3
        assert reach_geometry.chainages == [0, 5, 10]
        assert reach_geometry.length == 10
        prev_chainage = reach_geometry.points[0].chainage
        for p in reach_geometry.points:
            assert p.chainage >= prev_chainage, "Chainages should be sorted in ascending order."
            prev_chainage = p.chainage

    def test_reach_geometry_to_shapely(self, reach_geometry):
        g = reach_geometry.to_shapely()
        assert isinstance(g, shapely.LineString)
        assert len(g.coords) == 3, "Should only be 3 unique points"
        assert g.coords[0] == (0, 0)
        assert g.coords[1] == (0.5, 0.5)
        assert g.coords[2] == (1, 1)
        assert g.length == pytest.approx(2**0.5)

    def test_reach_geometry_chainage_to_geometric_distance(self, reach_geometry):
        assert reach_geometry.chainage_to_geometric_distance(0) == 0
        assert reach_geometry.chainage_to_geometric_distance(5) == pytest.approx(
            (0.5**2 + 0.5**2) ** 0.5
        )
        assert reach_geometry.chainage_to_geometric_distance(10) == pytest.approx(
            (1**2 + 1**2) ** 0.5
        )

    def test_reach_chainage_from_geometric_distance(self, reach_geometry):
        assert reach_geometry.chainage_from_geometric_distance(0) == 0
        assert reach_geometry.chainage_from_geometric_distance((0.5**2 + 0.5**2) ** 0.5) == 5
        assert reach_geometry.chainage_from_geometric_distance((1**2 + 1**2) ** 0.5) == 10

    def test_from_dotnet_reaches(self, river_reach):
        g = ReachGeometry.from_dotnet_reaches(river_reach.reaches)
        expected_n_gridpoints = sum([reach.GridPoints.Count for reach in river_reach.reaches])
        assert len(g.gridpoints) == expected_n_gridpoints
        expected_n_digipoints = sum([reach.DigiPoints.Count for reach in river_reach.reaches])
        assert len(g.digipoints) == expected_n_digipoints
        assert len(g.points) == expected_n_gridpoints + expected_n_digipoints
        dotnet_gp_start = river_reach.reaches[0].GridPoints[0]
        assert g.gridpoints[0].x == pytest.approx(dotnet_gp_start.X)
        assert g.gridpoints[0].y == pytest.approx(dotnet_gp_start.Y)
        assert g.gridpoints[0].z == pytest.approx(dotnet_gp_start.Z)
        assert g.gridpoints[0].chainage == pytest.approx(dotnet_gp_start.Chainage)
        dotnet_dp_start = river_reach.reaches[0].DigiPoints[0]
        assert g.digipoints[0].x == pytest.approx(dotnet_dp_start.X)
        assert g.digipoints[0].y == pytest.approx(dotnet_dp_start.Y)
        assert g.digipoints[0].z == pytest.approx(dotnet_dp_start.Z)
        assert g.digipoints[0].chainage == pytest.approx(dotnet_dp_start.M)
        dotnet_gp_end = list(river_reach.reaches[-1].GridPoints)[-1]
        assert g.gridpoints[-1].x == pytest.approx(dotnet_gp_end.X)
        assert g.gridpoints[-1].y == pytest.approx(dotnet_gp_end.Y)
        assert g.gridpoints[-1].z == pytest.approx(dotnet_gp_end.Z)
        assert g.gridpoints[-1].chainage == pytest.approx(dotnet_gp_end.Chainage)
        dotnet_dp_end = list(river_reach.reaches[-1].DigiPoints)[-1]
        assert g.digipoints[-1].x == pytest.approx(dotnet_dp_end.X)
        assert g.digipoints[-1].y == pytest.approx(dotnet_dp_end.Y)
        assert g.digipoints[-1].z == pytest.approx(dotnet_dp_end.Z)
        assert g.digipoints[-1].chainage == pytest.approx(dotnet_dp_end.M)
        prev_chainage = g.points[0].chainage
        for p in g.points:
            assert p.chainage >= prev_chainage, "Chainages should be sorted in ascending order."
            prev_chainage = p.chainage
        assert g.length == pytest.approx(2024.2276598819008)

    def test_reaches_point_interpolation_matches_mikeplus(self, river_reach):
        g = ReachGeometry.from_dotnet_reaches(river_reach.reaches)
        shape = g.to_shapely()
        # from MIKE+ chainage_points
        expected_coords = {
            53100: (385711.47339682, 5716561.25558023),
            54809.23: (386779.521238822, 5715252.98133197),
            54811.75: (386781.208762897, 5715251.10743646),
            55124.2276598819: (386997.40643911, 5715025.5383054),
        }
        for expected_chainage, expected_xy in expected_coords.items():
            distance = g.chainage_to_geometric_distance(expected_chainage)
            interp_point = shape.interpolate(distance)
            assert (interp_point.x, interp_point.y) == pytest.approx(expected_xy)


def test_geometry_from_node(node):
    node = node._node  # dotnet node
    g = geometry_from_node(node)
    assert isinstance(g, shapely.Point)
    assert g.x == pytest.approx(-687934.6000976562)
    assert g.y == pytest.approx(-1056500.69921875)


def test_geometry_from_catchment(many_catchments):
    for catchment in many_catchments:
        catchment = catchment._catchment  # dotnet catchment
        g = geometry_from_catchment(catchment)
        assert isinstance(g, shapely.Polygon)
        assert (g.centroid.x, g.centroid.y) == pytest.approx(
            (catchment.CenterPoint.X, catchment.CenterPoint.Y)
        )


def test_geometry_from_nodes_runs(many_nodes):
    for node in many_nodes:
        g = geometry_from_node(node._node)
        assert isinstance(g, shapely.Point)


def test_geometry_from_reaches_runs(many_reaches):
    for reach in many_reaches:
        g = ReachGeometry.from_dotnet_reaches(reach.reaches).to_shapely()
        assert isinstance(g, shapely.LineString)


def test_geometry_from_catchments_runs(many_catchments):
    for catchment in many_catchments:
        g = geometry_from_catchment(catchment._catchment)
        assert isinstance(g, shapely.Polygon)
