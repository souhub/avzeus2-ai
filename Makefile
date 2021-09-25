REPO_NAME := ai-test
API_GATEWAY := https://rwn9ktytw7.execute-api.ap-northeast-1.amazonaws.com/Stage/img-rec

create-ecr-repo:
	aws ecr create-repository \
		--repository-name ${REPO_NAME} \
		--image-scanning-configuration \
		scanOnPush=true

# -u: --use-container コンテナ使った仮想環境をビルドに使用
# -c: --cache 前にビルドされたイメージをキャッシュとして使用
build:
	sam build -uc

api:
	sam local start-api

test-img-recommend:
	curl  -X POST \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d @tests/woman.txt  http://127.0.0.1:3000/img-rec

test-imgrec-prod:
	curl  -X POST \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d @tests/woman.txt  ${API_GATEWAY}

test-scorerec:
	curl -X POST \
		-H "Content-Type: application/json" \
		-d @tests/actresses.json http://127.0.0.1:3000/score-rec

test-scorerec-prod:
	curl -X POST \
		-H "Content-Type: application/json" \
		-d '{ "1043077": 0.1, "1064775": 0.3, "1052094": 0.1, "1038230": 0.1, "1061347": 0.1 }'  https://rwn9ktytw7.execute-api.ap-northeast-1.amazonaws.com/Stage/score-rec
