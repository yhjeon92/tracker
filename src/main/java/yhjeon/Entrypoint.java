package yhjeon;

import java.io.FileReader;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.core.JsonParser;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import yhjeon.model.FeatureCollectionModel;
import yhjeon.model.FeatureModel;
import yhjeon.model.LineStringGeometryModel;
import yhjeon.model.PointGeometryModel;
import yhjeon.util.ResponseUtil;

@SpringBootApplication
public class Entrypoint {
  public static void main(String[] args) {
    String path = "/home/yhjeon/workspace/tracker-main/static/gpx_data/2021-07-17T15_32_00_Zeopoxa_Cycling.gpx";
    parseGpxToJsonString(path);
    SpringApplication.run(Entrypoint.class, args);
  }

  private static String parseGpxToJsonString(String filePath) {
    Document xml = null;
    try {
      InputSource inputSource = new InputSource(new FileReader(filePath));
      xml = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(inputSource);

      Element element  = xml.getDocumentElement();
      NodeList children = element.getChildNodes();

      Node trkseg = null;

      for (int i = 0; i < children.getLength(); i++) {
        if (children.item(i).getNodeName().equals("trk")) {
          Node trkNode = children.item(i);
          NodeList trkChildren = trkNode.getChildNodes();
          printNodeNames(trkChildren);
          for (int j = 0; j < trkChildren.getLength(); j++) {
            if (trkChildren.item(j).getNodeName().equals("trkseg")) {
              trkseg = trkChildren.item(j);
              break;
            }
          }
          break;
        }
      }

      if (trkseg == null) {
        System.out.println("ERROR: No node with name 'trkseg' was found. Exiting.");
        return "";
      }

      FeatureCollectionModel lineString = new FeatureCollectionModel();
      FeatureModel lineStringFeature = new FeatureModel();
      lineStringFeature.setId(1);
      lineStringFeature.setProperties(new HashMap<String, Object>());
      lineStringFeature.getProperties().put("popupContent", "This is a free bus line that will take you...");
      lineStringFeature.getProperties().put("underConstruction", false);
      lineString.addFeature(lineStringFeature);

      LineStringGeometryModel lineStringGeometryModel = new LineStringGeometryModel();
      lineStringFeature.setGeometry(lineStringGeometryModel);

      FeatureCollectionModel points = new FeatureCollectionModel();

      int idCount = 61;

      NodeList trkpts = trkseg.getChildNodes();
      for (int i = 0; i < trkpts.getLength(); i++) {
        if (trkpts.item(i).getNodeName().equals("trkpt")) {
          Double latitude = Double.parseDouble(trkpts.item(i).getAttributes().getNamedItem("lat").getNodeValue());
          Double longitude = Double.parseDouble(trkpts.item(i).getAttributes().getNamedItem("lon").getNodeValue());

          lineStringGeometryModel.addPoint(latitude, longitude);

          String ele = "";
          String time = "";

          NodeList trkptsChildren = trkpts.item(i).getChildNodes();

          for (int j = 0; j < trkptsChildren.getLength(); j++) {
            Node trkptsChild = trkptsChildren.item(j);
            if (trkptsChild.getNodeName().equals("ele")) {
              ele = trkptsChild.getTextContent();
            } else if (trkptsChild.getNodeName().equals("time")) {
              time = trkptsChild.getTextContent();
            }
          }

          if (!ele.isEmpty() && !time.isEmpty()) {
            FeatureModel singleFeature = new FeatureModel();
            singleFeature.setId(idCount++);
            Map<String, Object> property = new HashMap<>();
            property.put("popupContent", String.format("Elevation %sm, @%s", ele, time));
            singleFeature.setProperties(property);
            PointGeometryModel point = new PointGeometryModel();
            point.setPoint(latitude, longitude);
            singleFeature.setGeometry(point);
            points.addFeature(singleFeature);
          }
        }
      }

      System.out.println(ResponseUtil.convertToJson(lineString));
      System.out.println(ResponseUtil.convertToJson(points));

      return ResponseUtil.convertToJson(lineString);
    } catch (Exception exception) {
      exception.printStackTrace();
      return "";
    }
  }

  /**
   *
   * @param filePath Path of .gpx file to parse into GeoJSON data
   */
  private static void parseGpx(String filePath) {
    String outputFilePath = "C:\\Users\\Jeon Yeonghun\\Desktop\\MyOutput.txt";

    Document xml = null;
    try {
      InputSource inputSource = new InputSource(new FileReader(filePath));
      xml = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(inputSource);

      Element element  = xml.getDocumentElement();
      NodeList children = element.getChildNodes();

      Node trkseg = null;

      for (int i = 0; i < children.getLength(); i++) {
        if (children.item(i).getNodeName().equals("trk")) {
          Node trkNode = children.item(i);
          NodeList trkChildren = trkNode.getChildNodes();
          printNodeNames(trkChildren);
          for (int j = 0; j < trkChildren.getLength(); j++) {
            if (trkChildren.item(j).getNodeName().equals("trkseg")) {
              trkseg = trkChildren.item(j);
              break;
            }
          }
          break;
        }
      }

      if (trkseg == null) {
        System.out.println("ERROR: No node with name 'trkseg' was found. Exiting.");
        return;
      }

      FileOutputStream os = new FileOutputStream(outputFilePath);

      int idCount = 61;

      NodeList trkpts = trkseg.getChildNodes();
      for (int i = 0; i < trkpts.getLength(); i++) {
        if (trkpts.item(i).getNodeName().equals("trkpt")) {
          String latitude = trkpts.item(i).getAttributes().getNamedItem("lat").getNodeValue();
          String longitude = trkpts.item(i).getAttributes().getNamedItem("lon").getNodeValue();

          System.out.println(
              String.format("                    [%s, %s],", longitude, latitude)
          );

          String ele = "";
          String time = "";

          NodeList trkptsChildren = trkpts.item(i).getChildNodes();

          for (int j = 0; j < trkptsChildren.getLength(); j++) {
            Node trkptsChild = trkptsChildren.item(j);
            if (trkptsChild.getNodeName().equals("ele")) {
              ele = trkptsChild.getTextContent();
            } else if (trkptsChild.getNodeName().equals("time")) {
              time = trkptsChild.getTextContent();
            }
          }

          if (!ele.isEmpty() && !time.isEmpty()) {
            String jsonObject =
                "        {\n" +
                    "            \"type\": \"Feature\",\n" +
                    "            \"properties\": {\n" +
                    "                \"popupContent\": \"Elevation " + ele + "m, @" + time + "\"\n" +
                    "            },\n" +
                    "            \"geometry\": {\n" +
                    "                \"type\": \"Point\",\n" +
                    "                \"coordinates\": [" + longitude + ", " + latitude + "]" + "\n" +
                    "            },\n" +
                    "            \"id\": " + idCount++ + "\n" +
                    "        },";
            os.write(jsonObject.getBytes());
          }
        }
      }

      os.close();

    } catch (Exception exception) {
      exception.printStackTrace();
    }
  }

  private static void printNodeNames(NodeList nodeList) {
    for (int i = 0; i < nodeList.getLength(); i++) {
      System.out.println(nodeList.item(i).getNodeName());
    }
  }
}