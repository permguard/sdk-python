.DEFAULT_GOAL := build

brew:
	brew reinstall hatch

clean:
	pyenv global 3.7 3.8 3.9 3.10 3.11
	hatch -e lint run fmt
	hatch -e lint run all

envup:
	hatch run hello && hatch env find default

envdown:
	hatch env prune && hatch env remove

protoc:
	protoc proto/v1/*.proto \
		--go_out=internal/az/azreq/grpc/v1 --go_opt=paths=source_relative \
		--go-grpc_out=internal/az/azreq/grpc/v1 --go-grpc_opt=require_unimplemented_servers=false,paths=source_relative \
		--proto_path=proto/v1

# disallow any parallelism (-j) for Make. This is necessary since some
# commands during the build process create temporary files that collide
# under parallel conditions.
.NOTPARALLEL:

.PHONY: clean 
