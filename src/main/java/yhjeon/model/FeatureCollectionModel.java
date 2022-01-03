package yhjeon.model;

import java.util.ArrayList;
import java.util.List;

public class FeatureCollectionModel {
    private String type = "FeatureCollection";
    private List<FeatureModel> features;

    public FeatureCollectionModel() {
        this.features = new ArrayList<FeatureModel>();
    }

    public String getType() { return this.type; }

    public List<FeatureModel> getFeatures() { return this.features; }
    public void setFeatures(List<FeatureModel> features) { this.features = features; }

    public void addFeature(FeatureModel featureModel) { this.features.add(featureModel); }
}
