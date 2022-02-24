FROM node:current-alpine as builder
WORKDIR /opt/app
COPY react/package*.json ./
RUN npm install

FROM node:lts-alpine
RUN rm /usr/local/bin/yarn /usr/local/bin/yarnpkg \
    && rm -r /opt/yarn-v${YARN_VERSION}

WORKDIR /opt/app/
COPY --from=builder /opt/app/package.json \
    /opt/app/package-lock.json /opt/app/node_modules ./

CMD npx webpack