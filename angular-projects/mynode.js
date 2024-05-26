const fs = require('fs');
const path = require('path');
const successColor = '\x1b[32m%s\x1b[0m';
const checkSign = '\u{2705}';
const dotenv = require('dotenv').config({path: 'src/.env'}); ;

const envFile = `import { AppConfig } from '@angular-projects/app-config';
export const environment: AppConfig = {
    production: ${process.env.production},
    baseURL: '${process.env.baseURL}',
    clientId: '${process.env.clientId}',
    clientSecret: '${process.env.clientSecret}',
    webHost: ${process.env.webHost},
    keycloakHost: '${process.env.keycloakHost}',
    requireHttps: ${process.env.requireHttps},
    wsURL: '${process.env.wsURL}'
};
`;
const targetPath = path.join(__dirname, './apps/forex-app/src/environments/environment.ts');
fs.writeFile(targetPath, envFile, (err) => {
  if (err) {
    console.error(err);
    throw err;
  } else {
    console.log(successColor, `${checkSign} Successfully generated environment.ts`);
  }
});
