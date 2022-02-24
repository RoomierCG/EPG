FROM nginx:mainline-alpine as builder

ARG ENABLED_MODULES

RUN set -ex \
    && apk add --update --no-cache --virtual build-deps abuild autoconf automake byacc curl-dev flex g++ gcc geoip-dev \
        git libc-dev libmaxminddb-dev libstdc++ libtool libxml2-dev libxml2-utils libxslt linux-headers lmdb-dev make \
        mercurial musl-dev openssl openssl-dev pcre-dev unzip xz yajl-dev zlib-dev \
    # allow abuild as a root user
    && printf "#!/bin/sh\\nSETFATTR=true /usr/bin/abuild -F \"\$@\"\\n" > /usr/local/bin/abuild \
    && chmod +x /usr/local/bin/abuild \
    && hg clone -r ${NGINX_VERSION}-${PKG_RELEASE} https://hg.nginx.org/pkg-oss/ /opt/pkg-oss \
    && cd /opt/pkg-oss \
    && mkdir /tmp/packages \
    && for module in $ENABLED_MODULES; do \
        echo "Building $module for nginx-$NGINX_VERSION"; \
        if make -C /opt/pkg-oss/alpine list | grep -E "^$module\s+\d+" > /dev/null; then \
            echo "Building $module from pkg-oss sources"; \
            cd /opt/pkg-oss/alpine; \
            make abuild-module-$module BASE_VERSION=$NGINX_VERSION NGINX_VERSION=$NGINX_VERSION; \
            apk add $(. ./abuild-module-$module/APKBUILD; echo $makedepends;); \
            make module-$module BASE_VERSION=$NGINX_VERSION NGINX_VERSION=$NGINX_VERSION; \
            find ~/packages -type f -name "*.apk" -exec mv -v {} /tmp/packages/ \;; \
        else \
            echo "Don't know how to build $module module, exiting"; \
            exit 1; \
        fi; \
    done \
    # installing ModSecurity library
    && git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity /opt/ModSecurity \
    && cd /opt/ModSecurity \
    && git submodule init \
    && git submodule update \
    && ./build.sh \
    && ./configure \
    && make \
    && make install \
    # adding OWASP rules in ModSecurity
    && git clone --depth 1 -b v3.3/master --single-branch https://github.com/coreruleset/coreruleset /opt/coreruleset \
    && mv /opt/coreruleset/crs-setup.conf.example /usr/local/modsecurity/crs-setup.conf \
    && mv /opt/coreruleset/rules /usr/local/modsecurity/rules \
    # cleaning
    && apk del build-deps \
    && rm -rf /opt/*

FROM nginx:mainline-alpine

COPY --from=builder /usr/local/modsecurity /usr/local/modsecurity
COPY --from=builder /tmp/packages /tmp/packages
COPY 40-check-log-files.sh /docker-entrypoint.d

RUN set -ex \
    && apk add --update --no-cache --allow-untrusted /tmp/packages/nginx-module-*.apk \
    # the default rules return a 403 response code, they are changed to 444
    && sed -i 's/phase:1,log,auditlog,pass/phase:1,log,auditlog,pass,status:444/' /usr/local/modsecurity/crs-setup.conf \
    && sed -i 's/phase:2,log,auditlog,pass/phase:2,log,auditlog,pass,status:444/' /usr/local/modsecurity/crs-setup.conf \
    # enable ModSecurity
    && sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf \
    # disable ModSecurity logging
    && sed -i 's/SecAuditEngine RelevantOnly/SecAuditEngine Off/' /etc/nginx/modsec/modsecurity.conf \
    # generate main file that include the default rules and OWASP rules
    && printf '%s\n' 'Include "/etc/nginx/modsec/modsecurity.conf"' \
        'Include "/usr/local/modsecurity/crs-setup.conf"' \
        'Include "/usr/local/modsecurity/rules/*.conf"' > /etc/nginx/modsec/main.conf \
    # implement changes required to run Nginx as an unprivileged user
    && sed -i 's,listen       80;,listen       8080;,' /etc/nginx/conf.d/default.conf \
    && sed -i '/user  nginx;/d' /etc/nginx/nginx.conf \
    && sed -i 's,/var/run/nginx.pid,/tmp/nginx.pid,' /etc/nginx/nginx.conf \
    && sed -i "/^http {/a \    proxy_temp_path /tmp/proxy_temp;\n    client_body_temp_path /tmp/client_temp;\n    fastcgi_temp_path /tmp/fastcgi_temp;\n    uwsgi_temp_path /tmp/uwsgi_temp;\n    scgi_temp_path /tmp/scgi_temp;\n" /etc/nginx/nginx.conf \
    # nginx user must own the cache and etc directory to write cache and tweak the nginx config
    && chown -R nginx:nginx /var/cache/nginx \
    && chmod -R g+w /var/cache/nginx \
    && chown -R nginx:nginx /etc/nginx \
    && chmod -R g+w /etc/nginx \
    && chown -R nginx:nginx /var/log/nginx \
    && chmod -R g+w /var/log/nginx \
    # cleaning
    && rm -rf /tmp/packages /usr/share/nginx

HEALTHCHECK --interval=1m30s --timeout=10s --start-period=30s --retries=3 \
    CMD if [ -e /tmp/nginx.pid ]; then echo "Nginx is running"; else echo "Nginx isn't running"; exit 1; fi

VOLUME /etc/nginx/ssl

USER nginx

EXPOSE 8080 8443