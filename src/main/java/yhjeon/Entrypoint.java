package yhjeon;

import java.io.FileReader;
import java.io.FileOutputStream;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

@SpringBootApplication
public class Entrypoint {
  public static void main(String[] args) {
    SpringApplication.run(Entrypoint.class, args);
  }

  private static void parseGpx(String filePath) {
    filePath = "C:\\Users\\Jeon Yeonghun\\Desktop\\2021-07-17T15_32_00_Zeopoxa_Cycling.gpx";
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