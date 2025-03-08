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
	python -m grpc_tools.protoc --proto_path=./proto/v1 ./proto/v1/pdp.proto --python_out=. --grpc_python_out=./permguard/internal/az/azreq/grpc/v1

# disallow any parallelism (-j) for Make. This is necessary since some
# commands during the build process create temporary files that collide
# under parallel conditions.
.NOTPARALLEL:

.PHONY: clean 
