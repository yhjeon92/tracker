package yhjeon.model;

import java.util.List;

public abstract class GeometryModel {
    private String type;
    protected List<Object> coordinates;

    public String getType() { return this.type; }
    public void setType(String type) { this.type = type; }
    public List<Object> getCoordinates() { return this.coordinates; }
    public void setCoordinates(List<Object> coordinates) { this.coordinates = coordinates; }
}
