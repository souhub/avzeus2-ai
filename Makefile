REPO_NAME := ai-test
REPO_URI := 535411933495.dkr.ecr.ap-northeast-1.amazonaws.com/ai-test
API_GATEWAY := https://rwn9ktytw7.execute-api.ap-northeast-1.amazonaws.com/Stage/img-rec

create-ecr-repo:
	aws ecr create-repository \
		--repository-name ${REPO_NAME} \
		--image-scanning-configuration \
			scanOnPush=true

# -u --use-container コンテナ使った仮想環境をビルドに使用
# -c --cache 前にビルドされたイメージをキャッシュとして使用
build:
	sam build -uc

api:
	sam local start-api

test:
	curl  -X POST \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d @woman.txt  http://127.0.0.1:3000/img-rec

prod-test:
	curl  -X POST \
		-H "Content-Type: application/x-www-form-urlencoded" \
		-d @woman.txt  ${API_GATEWAY}
