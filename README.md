# open-template-chatbot
test chatbot

- streamlit gui
- with slack interaction

## AON configuration
- ./open_template_chatbot/.env
```shell
# Add your API Token
GROQ_API_KEY="GROQ FOR FREE LLM MODEL"
SLACK_APP_TOKEN="SLACK API"
SLACK_BOT_TOKEN="SLACK API"
MONGO_URI="YOU CAN USE FREE INSTANCE"
HUGGINGFACE_TOKEN="HUGGINGFACE TOKEN"
NOMIC_API_TOKEN="NOMIC API TOKEN FOR EMBEDDING API"
USERNAME="MONGODB USERNAME"
PASSWORD="MONGODB PASSWORD"
```
- streamlit username/password
```yml
credentials:
  usernames:
    {identification}:
      email:
      name:
      password: # To be replaced with hashed password
cookie:
  expiry_days: 30
  key: random_signature_key # Must be string
  name: random_cookie_name
preauthorized:
  emails:
  - 

```

## service workflow
```shell
# run streamlit
aon streamlit run

# run slack socket mode
aon slack run
```
