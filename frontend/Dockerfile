# Use node as the base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy the package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the Angular app code into the container
COPY . .

# Expose the port the Angular app will run on
EXPOSE 4200

# Command to run the Angular development server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
