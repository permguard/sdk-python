# Copyright (c) 2022 Nitro Agility S.r.l.
# SPDX-License-Identifier: Apache-2.0

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
	python -m grpc_tools.protoc --proto_path=./proto \
		--python_out=. --pyi_out=. --grpc_python_out=. \
		./proto/permguard/data/v1/pdp.proto
	bash scripts/header-generated.sh \
		permguard/data/v1/pdp_pb2.py \
		permguard/data/v1/pdp_pb2.pyi \
		permguard/data/v1/pdp_pb2_grpc.py

# disallow any parallelism (-j) for Make. This is necessary since some
# commands during the build process create temporary files that collide
# under parallel conditions.
.NOTPARALLEL:

.PHONY: clean 
