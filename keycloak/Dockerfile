# Documentation:
# https://www.keycloak.org/server/containers
ARG KEYCLOAK_VERSION

FROM quay.io/keycloak/keycloak:$KEYCLOAK_VERSION as builder

ENV KC_FEATURES="token-exchange,scripts,preview"

WORKDIR /opt/keycloak

# If run the image in kubernetes, switch and active below line.
# RUN /opt/keycloak/bin/kc.sh build --cache=ispn --cache-stack=kubernetes --health-enabled=true --metrics-enabled=true
RUN /opt/keycloak/bin/kc.sh build --cache=ispn --health-enabled=true --metrics-enabled=true --spi-x509cert-lookup-provider=apache

FROM quay.io/keycloak/keycloak:$KEYCLOAK_VERSION

LABEL image.version=$KEYCLOAK_VERSION

#https://www.keycloak.org/server/all-config
ENV KC_DB=${DB_VENDOR}
ENV KC_DB_URL_PORT=${DB_PORT}
ENV KC_DB_SCHEMA=${DB_DATABASE}
ENV KC_DB_USERNAME=${DB_USER}
ENV KC_DB_PASSWORD=${DB_PASSWORD}
ENV KEYCLOAK_ADMIN=${KEYCLOAK_ADMIN}
ENV KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD}
ENV KEYCLOAK_HEALTH_ENABLED=${KEYCLOAK_HEALTH_ENABLED}
ENV KEYCLOAK_METRICS_ENABLED=${KEYCLOAK_METRICS_ENABLED}
ENV KEYCLOAK_SPI_THEME_DEFAULT=${KEYCLOAK_SPI_THEME_DEFAULT}
ENV KC_HTTPS_CERTIFICATE_FILE=${KC_HTTPS_CERTIFICATE_FILE}
ENV KC_HTTPS_CERTIFICATE_KEY_FILE=${KC_HTTPS_CERTIFICATE_KEY_FILE}
ENV KC_HOSTNAME_URL=${KC_HOSTNAME_URL}
ENV KC_HEALTH_ENABLED=${KC_HEALTH_ENABLED}

COPY --from=builder /opt/keycloak/ /opt/keycloak/

# If any themes
# COPY themes/<nice-themes> /opt/keycloak/themes/<nice-themes>
# https://github.com/keycloak/keycloak/issues/19185#issuecomment-1480763024
USER root
RUN sed -i '/disabledAlgorithms/ s/ SHA1,//' /etc/crypto-policies/back-ends/java.config
USER keycloak

RUN /opt/keycloak/bin/kc.sh show-config

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start", "--optimized"]