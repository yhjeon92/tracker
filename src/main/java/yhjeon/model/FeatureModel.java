package yhjeon.model;

import java.util.HashMap;
import java.util.Map;

public class FeatureModel {
    private Integer id;
    private Map<String, Object> properties = new HashMap<String, Object>();
    private String type;
    private GeometryModel geometry;

    public FeatureModel() { this.type = "Feature"; }

    public Integer getId() { return this.id; }
    public void setId(Integer id) { this.id = id; }
    public Map<String, Object> getProperties() { return this.properties; }
    public void setProperties(Map<String, Object> properties) { this.properties = properties; }
    public String getType() { return this.type; }
    public void setType(String type) { this.type = type; }
    public GeometryModel getGeometry() { return this.geometry; }
    public void setGeometry(GeometryModel geometry) { this.geometry = geometry; }
}
