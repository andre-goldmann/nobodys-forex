package jdg.digital.forexbackend.config;

import org.matomo.java.tracking.TrackerConfiguration;
import org.springframework.lang.NonNull;

/**
 * Allows to customize the {@link TrackerConfiguration.TrackerConfigurationBuilder} with additional properties.
 *
 * <p>Implementations of this interface are detected automatically by the {@link MatomoTrackerAutoConfiguration}.
 *
 * @see MatomoTrackerAutoConfiguration
 * @see TrackerConfiguration
 * @see TrackerConfiguration.TrackerConfigurationBuilder
 */
@FunctionalInterface
public interface TrackerConfigurationBuilderCustomizer {

    /**
     * Customize the {@link TrackerConfiguration.TrackerConfigurationBuilder}.
     *
     * @param builder the {@link TrackerConfiguration.TrackerConfigurationBuilder} instance (never {@code null})
     * @see TrackerConfiguration#builder()
     * @see MatomoTrackerProperties
     */
    void customize(@NonNull TrackerConfiguration.TrackerConfigurationBuilder builder);
}
