package yhjeon.controller;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import yhjeon.config.DataConfig;

@RestController
@RequestMapping("/workout")
public class GeneralController {

  @Autowired
  private DataConfig dataConfig;

  @RequestMapping(path="/list", method= RequestMethod.GET)
  public ResponseEntity<?> listWorkouts() {
    File filePath = new File(dataConfig.getGpxroot());
    String[] gpxFiles = filePath.list();

    return new ResponseEntity<>(gpxFiles, HttpStatus.OK);
  }
}
