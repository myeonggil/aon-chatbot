
# login docker
docker login

# build local image
docker build --platform=linux/amd64 -t otc .

# tag local to remote
docker tag otc mgju/open-template-chatbot:latest

# push docker hub(private repo)
docker push mgju/open-template-chatbot:latest