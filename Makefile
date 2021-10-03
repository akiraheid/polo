image:
	podman build -t polo .

lock: Cargo.toml
	podman run \
		--name rust-tmp \
		-v ${PWD}/Cargo.toml:/usr/src/myapp/Cargo.toml:ro \
		-v ${PWD}/src/:/usr/src/myapp/src/:ro \
		-w /usr/src/myapp \
		docker.io/rust:1-alpine cargo build --release
	podman cp rust-tmp:/usr/src/myapp/Cargo.lock Cargo.lock
	podman rm rust-tmp
	
.PHONY: image lock
