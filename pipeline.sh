
# login docker
docker login

# build local image
docker build --platform=linux/amd64 -t otc .

# tag local to remote

# push docker hub(private repo)
docker push mgju/open-template-chatbot:latest