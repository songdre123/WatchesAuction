# WatchesAuction

## Front End
- To start the project:
  
- Step 1: npm install (always use node package manager)
  - If error try npm install --force 
  - Make sure you are in the front end project directory

- Step 2: npm run dev
  - If error try npm run dev --force (but npm run dev usually is sufficient)



## Back End

### Port Control
- Ensure all micro services have host="0.0.0.0" in app.run() parameter -> Last line

### Align User and Password Credentials
- Ensure that the credentials of the docker compose is following your own docker id and username / password in compose.yaml

  - dbURL: mysql+mysqlconnector://<username>:<password>@host.docker.internal:3306/{databasename}
  - image: <dockerID>/bids:esd

