package jdg.digital.forexbackend;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.data.r2dbc.config.EnableR2dbcAuditing;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableConfigurationProperties
@EnableR2dbcAuditing
@EnableScheduling
@Slf4j
public class ForexBackendJavaApplication implements CommandLineRunner {

    //@Autowired
    //TrackerConfiguration trackerConfiguration;

    //@Autowired
    //MatomoTracker matomoTracker;

    @Override
    public void run(String... args) throws Exception {
        //web-1     | 172.22.0.1 - - [30/Jan/2024:00:52:49 +0000] "GET /matomo.php?idsite=2&rec=1 HTTP/1.1" 200 54 "http://172.17.134.42/auth/login" "Mozilla/
        //5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "-"
        /*MatomoRequest request = MatomoRequest.request()
                .actionUrl("http://172.17.134.42/dashboard")
                .debug(true)
                //.eventName("login")
                //.eventAction("login")
                .siteId(2)
                //.userId("anonymous")
                //.actionName("My Action")
                //.event("Training","Workout completed","Bench press",60.0)
                .eventAction("login")
                // Wichtig ist das hier
                .visitorId(VisitorId.fromString("anonymous@example.org"))
                .build();
        matomoTracker.sendBulkRequestAsync(request);*/
        //matomoTracker.sendRequest(request);

    }

    public static void main(String[] args) {
        new SpringApplicationBuilder(ForexBackendJavaApplication.class).run(args);
    }

}
