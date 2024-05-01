
npx nx build financial-data-analysis
npx nx serve financial-data-analysis
npx nx serve forex-app --port=4300
nx g @nx/angular:library nav-ui --directory=libs/web/shared/nav/ui --standalone
npx nx g @nrwl/js:lib login-data-access --directory=libs/web/shared/auth/login/data-access
nx g rm login-data-access


* nx g @nx/angular:storybook-configuration myproject
* nx g @nx/angular:stories --project=myproject
* nx run myproject:storybook

cd C:\Users\agol\keycloak-23.0.7
bin\kc.bat start-dev --log-level=DEBUG
