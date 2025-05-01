# frontend/Dockerfile

FROM node:20-alpine

WORKDIR /app

# Install dependencies first to optimize cache
COPY package*.json ./
RUN npm install

# Copy rest of the app
COPY . .

# Bygg Next.js
RUN npm run build

# Expose port
EXPOSE 3000

# Start Next.js
CMD ["npm", "run", "start"]
