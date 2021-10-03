FROM docker.io/rust:1-alpine as builder

# Cache dependencies
RUN cargo new --bin /usr/src/polo
WORKDIR /usr/src/polo
COPY ./Cargo.toml ./Cargo.toml
COPY ./Cargo.lock ./Cargo.lock
RUN cargo build --release
RUN rm -r src/*.rs

# Build app
COPY ./src ./src
RUN cargo install --path .

# Package app
FROM docker.io/alpine:3
EXPOSE 80
COPY --from=builder /usr/local/cargo/bin/polo /usr/local/bin/polo
ENTRYPOINT ["polo"]
CMD ["start"]
