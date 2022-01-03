package yhjeon.model;

import java.util.ArrayList;
import java.util.List;

public class LineStringGeometryModel extends GeometryModel {
    public LineStringGeometryModel() {
        super.setType("LineString");
        coordinates = new ArrayList<>();
    }

    public void addPoint(Double latitude, Double longitude) {
        List<Double> singlePoint = new ArrayList<>();
        singlePoint.add(latitude);
        singlePoint.add(longitude);
        coordinates.add(singlePoint);
    }
}
