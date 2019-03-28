set -x

BRANCH=${BRANCH='master'}

export PROXY=${PROXY=''}

export TOKEN=${TOKEN=''}

export USERNAME=${USERNAME=''}

export PASSWORD=${PASSWORD=''}

export MONGO_HOST=${MONGO_HOST=''}

export PROC_COUNT=${PROC_COUNT=4}

export VK_USER_ID=${VK_USER_ID=''}

set +x

git pull && git checkout ${BRANCH} && git pull

pip3 install requests bs4 pymongo
pip3 install --upgrade --no-deps --force-reinstall -r requirements.txt
pip3 install requests python-dotenv

python3 app.py
