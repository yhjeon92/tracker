package yhjeon.model;

import java.util.ArrayList;

public class PointGeometryModel extends GeometryModel {
    public PointGeometryModel() {
        super.setType("Point");
        coordinates = new ArrayList<>();
    }

    public void setPoint(Double latitude, Double longitude) {
        coordinates.add(latitude);
        coordinates.add(longitude);
    }
}
