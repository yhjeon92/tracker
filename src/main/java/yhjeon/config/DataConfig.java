package yhjeon.config;

import javax.validation.constraints.NotEmpty;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix="data")
public class DataConfig {
  @NotEmpty
  private String gpxroot;

  public String getGpxroot() { return this.gpxroot; }
  public void setGpxroot(String gpxroot) { this.gpxroot = gpxroot; }
}
