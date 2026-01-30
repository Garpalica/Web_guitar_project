FROM node:22-alpine as frontend-builder
WORKDIR /app
COPY Frontend/package*.json ./
RUN npm install
COPY Frontend/ ./
RUN npm run build
FROM python:3.10-slim
WORKDIR /app
COPY Backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY Backend/ .
COPY --from=frontend-builder /app/dist ./client
RUN mkdir -p instance
VOLUME /app/instance
EXPOSE 5000
CMD ["python", "app.py"]