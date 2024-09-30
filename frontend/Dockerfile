# Use the official Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if exists)
COPY package*.json ./

# Install dependencies
RUN npm install -g @angular/cli  # Install Angular CLI globally
RUN npm install  # Install local dependencies

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 4200

# Command to run the app in development mode
CMD ["ng", "serve", "--host", "0.0.0.0"]
