.EXPORT_ALL_VARIABLES:

OUTPUT=tests/data/predictions.json
INPUT=tests/data/input.json
PORT=8000
ENDPOINT=http://localhost:${PORT}/<SERVICE-PREFIX>/v1/predict
ENV-DEV=build/docker/env_dev.env
SERVICE_NAME=<SERVICE_NAME>
TAG=<TAG>


serve:
	python app/wsgi.py

request:
	curl -X POST ${ENDPOINT} -H "Content-Type: application/json" -H 'X-Request-ID: 1a8a3ca3-8a45-4cae-b165-43c962241e1a' -d @${INPUT} > ${OUTPUT}

build-image:
	docker build -f build/docker/Dockerfile -t ${SERVICE_NAME}:${TAG} .

run:
	docker run -p 8000:8000 -v ~/<MODEL_WEIGHTS_FILE>:/model --env-file ${ENV-DEV} ${SERVICE_NAME}:${TAG}
