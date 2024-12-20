
node -r dotenv/config mynode.js && npx nx build financial-data-analysis
node -r dotenv/config mynode.js && npx nx build forex-app


node -r dotenv/config mynode.js
npx nx serve financial-data-analysis
npx nx serve forex-app --port=4300

nx g @nx/angular:library --directory=libs/web/shared/ui/header/multipanel --standalone
npx nx g @nrwl/js:lib login-data-access --directory=libs/web/shared/auth/login/data-access
nx g rm login-data-access


* nx g @nx/angular:storybook-configuration myproject
* nx run myproject:storybook

cd C:\Users\agol\keycloak-23.0.7
bin\kc.bat start-dev --log-level=DEBUG

cd C:\Users\andre\development\keycloak-23.0.7\
bin\kc.bat start-dev --log-level=DEBUG

# TODOS
* login does not work on cellphone


Vercel-Config

Build-Command:
node -r dotenv/config mynode.js && npx nx build forex-trades-analysis --prod

Output-Directory:
dist/apps/forex-trades-analysis

Development-Command:
npx nx serve forex-trades-analysis --port $PORT
